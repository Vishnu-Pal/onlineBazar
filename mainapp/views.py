from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import razorpay
from django.conf import settings
from onlineBazar.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
import os
from .models import *
from requests import session
from random import randint
from django.core.mail import send_mail
import re

# Create your views here.


# def home use for go to home page
def home(request):
    # All product show home page
    products = Product.objects.all()
    products = products[::-1]
    if request.method == "POST":
        try:
            email = request.POST.get("email")
            n = Newsletter()
            n.email = email
            n.save()
            subject = "Thanks For Subscribe : Team Online Bazar"
            message = """
                    Thanks For Subscribing
                    Team : Online Bazar
                    Contact Us : 9990495419
                    http://localhost:8000
                    """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [
                n.email,
            ]
            send_mail(subject, message, email_from, recipient_list)

            # messages.success(
            #     request,
            #     "Thanks For Subscribing",
            # )
        except:
            pass
        return HttpResponseRedirect("/")
    # Show index means home page
    return render(request, "index.html", {"Products": products})


# def shop use for go to shop page  mc sc br parameter use for Maincategory Subcategory and Brand
def shop(request, mc, sc, br):
    # show for category
    maincategory = MainCategory.objects.all()
    subcategory = SubCategory.objects.all()
    brand = Brand.objects.all()

    # initialise category
    if request.method == "POST":
        search = request.POST.get("search")
        products = Product.objects.filter(Q(name__icontains=search))
    else:
        if mc == "All" and sc == "All" and br == "All":
            products = Product.objects.all()
        elif mc != "All" and sc == "All" and br == "All":
            products = Product.objects.filter(
                maincategory=MainCategory.objects.get(name=mc)
            )
        elif mc == "All" and sc != "All" and br == "All":
            products = Product.objects.filter(
                subcategory=SubCategory.objects.get(name=sc)
            )
        elif mc == "All" and sc == "All" and br != "All":
            products = Product.objects.filter(brand=Brand.objects.get(name=br))

        elif mc != "All" and sc != "All" and br == "All":
            products = Product.objects.filter(
                maincategory=MainCategory.objects.get(name=mc),
                subcategory=SubCategory.objects.get(name=sc),
            )
        elif mc != "All" and sc == "All" and br != "All":
            products = Product.objects.filter(
                maincategory=MainCategory.objects.get(name=mc),
                brand=Brand.objects.get(name=br),
            )
        elif mc == "All" and sc != "All" and br != "All":
            products = Product.objects.filter(
                subcategory=SubCategory.objects.get(name=sc),
                brand=Brand.objects.get(name=br),
            )
        else:
            products = Product.objects.filter(
                maincategory=MainCategory.objects.get(name=mc),
                subcategory=SubCategory.objects.get(name=sc),
                brand=Brand.objects.get(name=br),
            )

    # show first new product
    products = products[::-1]

    # go to shop and dics use product and category show
    return render(
        request,
        "shop.html",
        {
            "Products": products,
            "Maincategory": maincategory,
            "Subcategory": subcategory,
            "Brand": brand,
            "mc": mc,
            "sc": sc,
            "br": br,
        },
    )


def login(request):
    # data base se data get karne ke liye
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/profile/")

        else:
            messages.error(request, "Invalid User Name or Password")
    return render(request, "login.html")


def signup(request):
    # database se data get krne or bejne ke liye
    if request.method == "POST":
        actype = request.POST.get("actype")
        if actype == "seller":
            u = Seller()
        else:
            u = Buyer()
        u.name = request.POST.get("name")
        u.username = request.POST.get("username")
        u.email = request.POST.get("email")
        u.phone = request.POST.get("phone")

        def isValid(name):
            # 1) Begins with 0 or 91
            # 2) Then contains 6,7 or 8 or 9.
            # 3) Then contains 9 digits
            Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
            return Pattern.match(name)

        # Driver Code
        if isValid(u.phone):
            pass
        else:
            messages.error(request, "Invalid Number !!!")
            print("Invalid Num")
            return render(request, "signup.html")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")

        def isValidpass(password):
            Pattern = re.compile(
                "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
            )
            return Pattern.match(password)

        # Driver Code
        if isValidpass(password):
            pass
        else:
            messages.error(request, "Please make sure strong password !!!")
            print("Invalid Num")
            return render(request, "signup.html")
        if password == cpassword:
            try:
                user = User.objects.create_user(
                    username=u.username, password=password, email=u.email
                )
                user.save()
                u.save()
                subject = "Thanks to create Account With Us : Team Online Bazar"
                message = """
                        Thank %s to create Account
                        With Us
                        Team : Online Bazar
                        Contact Us : 9990495419
                        http://localhost:8000 
                        """ % (
                    u.name
                )
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [
                    u.email,
                ]
                send_mail(subject, message, email_from, recipient_list)

                messages.success(
                    request,
                    "Your Account has been creat.!!!!!",
                )
            except:
                messages.error(request, "User already taken !!!")
                return render(request, "signup.html")
            return HttpResponseRedirect("/login/")
        else:
            messages.error(
                request, "Password and Confirm Password does not mathed !!!!"
            )

    return render(request, "signup.html")


@login_required(login_url="/login/")
def profilePage(request):
    user = User.objects.get(username=request.user)
    if user.is_superuser:
        return HttpResponseRedirect("/admin/")
    else:
        try:
            seller = Seller.objects.get(username=request.user)
            product = Product.objects.filter(seller=seller)
            product = product[::-1]

            return render(
                request, "sellerProfile.html", {"User": seller, "Product": product}
            )
        except:
            buyer = Buyer.objects.get(username=request.user)
            wishlist = Wishlist.objects.filter(buyer=buyer)
            checkouts = Checkout.objects.filter(buyer=buyer)
            checkouts = checkouts[::-1]
            return render(
                request,
                "buyerProfile.html",
                {"User": buyer, "Wishlist": wishlist, "Orders": checkouts},
            )


@login_required(login_url="/login/")
def updateProfilePage(request):
    user = User.objects.get(username=request.user)
    if user.is_superuser:
        return HttpResponseRedirect("/admin/")
    else:
        try:
            user = Seller.objects.get(username=request.user)
        except:
            user = Buyer.objects.get(username=request.user)
        if request.method == "POST":
            user.name = request.POST.get("name")
            user.email = request.POST.get("email")
            user.phone = request.POST.get("phone")
            user.addressline1 = request.POST.get("addressline1")
            user.addressline2 = request.POST.get("addressline2")
            user.addressline3 = request.POST.get("addressline3")
            user.pin = request.POST.get("pin")
            user.city = request.POST.get("city")
            user.state = request.POST.get("state")
            if request.FILES.get("pic"):
                if user.pic:
                    os.remove("media/" + str(user.pic))
                user.pic = request.FILES.get("pic")
            user.save()
            return HttpResponseRedirect("/profile/")
        return render(request, "updateProfile.html", {"User": user})


@login_required(login_url="/login/")
def addProduct(request):
    maincategory = MainCategory.objects.all()
    subcategory = SubCategory.objects.all()
    brand = Brand.objects.all()
    if request.method == "POST":
        p = Product()
        p.name = request.POST.get("name")
        p.maincategory = MainCategory.objects.get(name=request.POST.get("maincategory"))
        p.subcategory = SubCategory.objects.get(name=request.POST.get("subcategory"))
        p.brand = Brand.objects.get(name=request.POST.get("brand"))
        p.baseprice = int(request.POST.get("baseprice"))
        p.discount = int(request.POST.get("discount"))
        p.finalprice = p.baseprice - p.baseprice * p.discount / 100
        color = ""
        if request.POST.get("Red"):
            color += "Red "
        if request.POST.get("Green"):
            color += "Green "
        if request.POST.get("Yellow"):
            color += "Yellow "
        if request.POST.get("Pink"):
            color += "Pink "
        if request.POST.get("White"):
            color += "White "
        if request.POST.get("Black"):
            color += "Black "
        if request.POST.get("Blue"):
            color += "Blue "
        if request.POST.get("Brown"):
            color += "Brown "
        if request.POST.get("SkyBlue"):
            color += "SkyBlue "
        if request.POST.get("Orange"):
            color += "Orange "
        if request.POST.get("Navy"):
            color += "Navy "
        if request.POST.get("Gray"):
            color += "Gray "

        size = ""
        if request.POST.get("S"):
            size += "S "
        if request.POST.get("SM"):
            size += "SM "
        if request.POST.get("M"):
            size += "M "
        if request.POST.get("L"):
            size += "L "
        if request.POST.get("XL"):
            size += "XL "
        if request.POST.get("XXL"):
            size += "XXL "
        p.color = color
        p.size = size
        p.stock = request.POST.get("stock")
        p.discription = request.POST.get("discription")
        p.pic1 = request.FILES.get("pic1")
        p.pic2 = request.FILES.get("pic2")
        p.pic3 = request.FILES.get("pic3")
        p.pic4 = request.FILES.get("pic4")
        try:
            p.seller = Seller.objects.get(username=request.user)
        except:
            return HttpResponseRedirect("/profile/")
        p.save()
        subject = "Checkout Our Letest Product On Online Bazar : Team Online Bazar"
        message = """
                hey!!!
                We Upload some more letest product 
                with best offer
                Please Checkout
                Team : Online Bazar
                Contact Us : 9990495419
                http://localhost:8000/singleProduct/%d
                """ % (
            p.id
        )
        email_from = settings.EMAIL_HOST_USER
        subscriber = Newsletter.objects.all()
        recipient_list = subscriber
        send_mail(subject, message, email_from, recipient_list)

        messages.success(
            request,
            "Your Account has been creat.!!!!!",
        )
        return HttpResponseRedirect("/profile/")
    return render(
        request,
        "addProduct.html",
        {"MainCategory": maincategory, "SubCategory": subcategory, "Brand": brand},
    )


@login_required(login_url="/login/")
def deleteProduct(request, num):
    try:
        p = Product.objects.get(id=num)
        seller = Seller.objects.get(username=request.user)
        if p.seller == seller:
            p.delete()
        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")


@login_required(login_url="/login/")
def editProductPage(request, num):
    try:
        p = Product.objects.get(id=num)
        seller = Seller.objects.get(username=request.user)
        if p.seller == seller:
            maincategory = MainCategory.objects.exclude(name=p.maincategory)
            subcategory = SubCategory.objects.exclude(name=p.subcategory)
            brand = Brand.objects.exclude(name=p.brand)
            if request.method == "POST":
                p.name = request.POST.get("name")
                p.maincategory = MainCategory.objects.get(
                    name=request.POST.get("maincategory")
                )
                p.subcategory = SubCategory.objects.get(
                    name=request.POST.get("subcategory")
                )
                p.brand = Brand.objects.get(name=request.POST.get("brand"))
                p.baseprice = int(request.POST.get("baseprice"))
                p.discount = int(request.POST.get("discount"))
                p.finalprice = p.baseprice - p.baseprice * p.discount / 100
                color = ""
                if request.POST.get("Red"):
                    color += "Red "
                if request.POST.get("Green"):
                    color += "Green "
                if request.POST.get("Yellow"):
                    color += "Yellow "
                if request.POST.get("Pink"):
                    color += "Pink "
                if request.POST.get("White"):
                    color += "White "
                if request.POST.get("Black"):
                    color += "Black "
                if request.POST.get("Blue"):
                    color += "Blue "
                if request.POST.get("Brown"):
                    color += "Brown "
                if request.POST.get("SkyBlue"):
                    color += "SkyBlue "
                if request.POST.get("Orange"):
                    color += "Orange "
                if request.POST.get("Navy"):
                    color += "Navy "
                if request.POST.get("Gray"):
                    color += "Gray "
                size = ""
                if request.POST.get("S"):
                    size += "S "
                if request.POST.get("SM"):
                    size += "SM "
                if request.POST.get("M"):
                    size += "M "
                if request.POST.get("L"):
                    size += "L "
                if request.POST.get("XL"):
                    size += "XL "
                if request.POST.get("XXL"):
                    size += "XXL "
                p.color = color
                p.size = size
                p.stock = request.POST.get("stock")
                p.discription = request.POST.get("discription")
                if request.FILES.get("pic1"):
                    if p.pic1:
                        os.remove("media/" + str(p.pic1))
                    p.pic1 = request.FILES.get("pic1")
                if request.FILES.get("pic2"):
                    if p.pic2:
                        os.remove("media/" + str(p.pic2))
                    p.pic2 = request.FILES.get("pic2")
                if request.FILES.get("pic3"):
                    if p.pic3:
                        os.remove("media/" + str(p.pic3))
                    p.pic3 = request.FILES.get("pic3")
                if request.FILES.get("pic4"):
                    if p.pic4:
                        os.remove("media/" + str(p.pic4))
                    p.pic4 = request.FILES.get("pic4")
                p.save()
                return HttpResponseRedirect("/profile/")
            return render(
                request,
                "editProduct.html",
                {
                    "Product": p,
                    "MainCategory": maincategory,
                    "SubCategory": subcategory,
                    "Brand": brand,
                },
            )
        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")


def singleProduct(request, num):
    p = Product.objects.get(id=num)

    color = p.color.strip().split(" ")
    print(color)
    # color = p.color[:-1]
    size = p.size.strip().split(" ")
    print(size)
    # size = p.size[:-1]

    return render(
        request, "singleProduct.html", {"Product": p, "color": color, "size": size}
    )


def addToWishlist(request, num):
    try:
        buyer = Buyer.objects.get(username=request.user)
        wishlist = Wishlist.objects.filter(buyer=buyer)
        p = Product.objects.get(id=num)
        flag = False
        for i in wishlist:
            if i.product == p:
                flag = True
                break
        if flag == False:
            w = Wishlist()
            w.buyer = buyer
            w.product = p
            w.save()
        return HttpResponseRedirect("/profile/")
    except:
        HttpResponseRedirect("/profile/")


@login_required(login_url="/login/")
def deleteWishlist(request, num):
    try:
        w = Wishlist.objects.get(id=num)
        buyer = Buyer.objects.get(username=request.user)
        if w.buyer == buyer:
            w.delete()
        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")


def addToCart(request):
    pid = request.POST.get("pid")
    color = request.POST.get("color")
    size = request.POST.get("size")
    cart = request.session.get("cart", None)
    if cart:
        if pid in cart.keys() and color == cart[pid][1] and size == cart[pid][2]:
            pass
        else:
            count = len(cart.keys())
            count += 1
            cart.setdefault(str(count), [pid, 1, color, size])
    else:
        cart = {"1": [pid, 1, color, size]}
    request.session["cart"] = cart
    return HttpResponseRedirect("/cart/")


def Cart(request):
    cart = request.session.get("cart", None)
    total = 0
    shipping = 0
    final = 0
    if cart:
        for values in cart.values():
            p = Product.objects.get(id=int(values[0]))
            total += p.finalprice * values[1]
        if len(cart.values()) >= 1 and total < 1000:
            shipping = 150
        final = total + shipping
    return render(
        request,
        "cart.html",
        {"Cart": cart, "Total": total, "Shipping": shipping, "Final": final},
    )


def updateCart(request, id, num):
    cart = request.session.get("cart", None)
    if cart:
        if num == "-1":
            if cart[id][1] > 1:
                q = cart[id][1]
                q -= 1
                cart[id][1] = q
        else:
            q = cart[id][1]
            q += 1
            cart[id][1] = q
        request.session["cart"] = cart
    return HttpResponseRedirect("/cart/")


def deleteCart(request, id):
    cart = request.session.get("cart", None)
    if cart:
        cart.pop(id)
        request.session["cart"] = cart
    return HttpResponseRedirect("/cart/")


client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))


@login_required(login_url="/login/")
def checkOut(request):
    cart = request.session.get("cart", None)
    total = 0
    shipping = 0
    final = 0
    if cart:
        for values in cart.values():
            p = Product.objects.get(id=int(values[0]))
            total += p.finalprice * values[1]
        if len(cart.values()) >= 1 and total < 1000:
            shipping = 150
        final = total + shipping
    try:
        buyer = Buyer.objects.get(username=request.user)
        if request.method == "POST":
            mode = request.POST.get("mode")
            check = Checkout()
            check.buyer = buyer
            check.total = total
            check.shipping = shipping
            check.final = final
            check.save()
            for value in cart.values():
                cp = CheckoutProduct()
                p = Product.objects.get(id=int(value[0]))
                cp.name = p.name
                cp.pic = p.pic1.url
                cp.size = value[3]
                cp.color = value[2]
                cp.price = p.finalprice
                cp.qyt = value[1]
                cp.total = p.finalprice * value[1]
                cp.checkout = check
                cp.save()
            request.session["cart"] = {}
            if mode == "COD":
                return HttpResponseRedirect("/confirmation/")
            else:
                orderAmount = check.final * 100
                orderCurrency = "INR"
                paymentOrder = client.order.create(
                    {
                        "amount": orderAmount,
                        "currency": orderCurrency,
                        "payment_capture": 1,
                    }
                )
                paymentId = paymentOrder["id"]
                check.mode = "Net Banking"
                check.save()
                return render(
                    request,
                    "pay.html",
                    {
                        "amount": orderAmount,
                        "api_key": RAZORPAY_API_KEY,
                        "order_id": paymentId,
                        "User": buyer,
                    },
                )

        return render(
            request,
            "checkOut.html",
            {
                "Cart": cart,
                "Total": total,
                "Shipping": shipping,
                "Final": final,
                "User": buyer,
            },
        )
    except:
        return HttpResponseRedirect("/profile/")


@login_required(login_url="/login/")
def paymentSuccess(request, rppid, rpoid, rpsid):
    buyer = Buyer.objects.get(username=request.user)
    check = Checkout.objects.filter(buyer=buyer)
    check = check[::-1]
    check = check[0]
    check.rppid = rppid
    check.rpoid = rpoid
    check.rpsid = rpsid
    check.paymentstatus = 2
    check.save()
    return HttpResponseRedirect("/confirmation/")


@login_required(login_url="/login/")
def paynow(request, num):
    try:
        buyer = Buyer.objects.get(username=request.user)
    except:
        return HttpResponseRedirect("/profile/")
    check = Checkout.objects.get(id=num)
    orderAmount = check.final * 100
    orderCurrency = "INR"
    paymentOrder = client.order.create(
        dict(
            amount=orderAmount,
            currency=orderCurrency,
            payment_capture=1,
        )
    )
    paymentId = paymentOrder["id"]
    check.save()
    return render(
        request,
        "pay.html",
        {
            "amount": orderAmount,
            "api_key": RAZORPAY_API_KEY,
            "order_id": paymentId,
            "User": buyer,
        },
    )


def Confirmation(request):
    subject = "Thanks to Shop With Us : Team Online Bazar"
    buyer = Buyer.objects.get(username=request.user)
    message = """
            Thank %s Shopping With Us
            Team : Online Bazar
            Contact Us : 9990495419
            http://localhost:8000 
            """ % (
        buyer.name
    )
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [
        buyer.email,
    ]
    send_mail(subject, message, email_from, recipient_list)

    messages.success(
        request,
        "Your Account has been creat.!!!!!",
    )
    return render(request, "confirmation.html")


def contactPage(request):
    if request.method == "POST":
        c = Contact()
        c.name = request.POST["name"]
        c.email = request.POST["email"]
        c.phone = request.POST["phone"]
        c.subject = request.POST["subject"]
        c.message = request.POST["message"]
        c.save()
        subject = "Your Query has been submitted : Team Online Bazar"
        message = """
                   Thanks to share your query with Us
                   Our Team will contact You soon
                   Team : Online Bazar
                   Contact Us : 9990495419
                   http://localhost:8000 
                """
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            c.email,
        ]
        send_mail(subject, message, email_from, recipient_list)

        messages.success(
            request, "Your Query has been submited !!! Our Team will be Contact Soon"
        )
    return render(request, "contact.html")


def forgetUsername(request):
    if request.method == "POST":
        username = request.POST["username"]
        user = User.objects.get(username=username)
        if user is not None:
            try:
                user = Buyer.objects.get(username=username)
            except:
                user = Seller.objects.get(username=username)
            num = randint(100000, 999999)
            request.session["otp"] = num
            request.session["user"] = username
            subject = "OTP for reset Password : Team Online Bazar"
            message = (
                """
                    OTP : %d
                    Team : Online Bazar
                    http://localhost:8000 
                    """
                % num
            )
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [
                user.email,
            ]
            send_mail(subject, message, email_from, recipient_list)
            messages.success(
                request,
                "Otp send Your Email",
            )
            return HttpResponseRedirect("/forget-otp/")
        else:
            messages.error(request, "User name Not Found")
    return render(request, "forget-username.html")


def forgetOTP(request):
    if request.method == "POST":
        otp = int(request.POST["otp"])
        sessionOTP = request.session.get("otp", None)
        if otp == sessionOTP:
            return HttpResponseRedirect("/forget-password/")
        else:
            messages.error(request, "Invalid OTP")
    return render(request, "forget-otp.html")


def forgetPassword(request):
    if request.method == "POST":
        password = request.POST["password"]
        cpassword = request.POST["cpassword"]
        if password == cpassword:
            user = User.objects.get(username=request.session.get("user"))
            user.set_password(password)
            user.save()
            return HttpResponseRedirect("/login/")
        else:
            messages.error(request, "Password and Confirm Password doesn't match !!!")
    return render(request, "forget-password.html")


def about(request):
    return render(request, "about.html")
