from django import template
from mainapp.models import *

register = template.Library()


@register.filter("checkColor")
def checkColor(color, item):
    return item in color


@register.filter("checkSize")
def checkSize(size, item):
    return item in size


@register.filter("orderStatus")
def checkorderStatus(request, num):
    if num == 0:
        return "Cancelled"
    elif num == 1:
        return "Not Packed"
    elif num == 2:
        return "Packed"
    elif num == 3:
        return "Out For Delivery"
    else:
        return "Delevered"


@register.filter("paymentStatus")
def paymentStatus(request, num):
    if num == 1:
        return "Pendding"
    else:
        return "Done"


@register.filter("paymentStatusCon")
def paymentStatusCon(request, num):
    if num == 1:
        return True
    else:
        return False


@register.filter("orderItem")
def orderItem(request, num):
    check = Checkout.objects.get(id=num)
    p = CheckoutProduct.objects.filter(checkout=check)
    return p


@register.filter("stock")
def stock(request, data):
    if data == "In Stock":
        return True
    else:
        return False
