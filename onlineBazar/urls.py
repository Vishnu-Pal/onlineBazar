"""onlineBazar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainapp import views


admin.site.site_header = "Online Bazar"
admin.site.site_title = "Online Bazar"
admin.site.site_url = "OnlineBazar"
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="index"),
    path("login/", views.login, name="login"),
    path("shop/<str:mc>/<str:sc>/<str:br>/", views.shop),
    path("logout/", views.logout),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profilePage),
    path("updateProfile/", views.updateProfilePage, name="updateProfile"),
    path("addProduct/", views.addProduct, name="addProduct"),
    path("deleteProduct/<int:num>/", views.deleteProduct),
    path("deleteWishlist/<int:num>/", views.deleteWishlist),
    path("deleteCart/<str:id>/", views.deleteCart),
    path("editProduct/<int:num>/", views.editProductPage, name="editProduct"),
    path("singleProduct/<int:num>/", views.singleProduct, name="singleProduct"),
    path("addToWishlist/<int:num>/", views.addToWishlist),
    path("cart/", views.Cart, name="cart"),
    path("update-cart/<str:id>/<str:num>/", views.updateCart),
    path("add-to-cart/", views.addToCart),
    path("checkOut/", views.checkOut, name="checkOut"),
    path("confirmation/", views.Confirmation, name="confirmation"),
    path("paynow/<int:num>/", views.paynow),
    path("paymentSuccess/<str:rppid>/<str:rpoid>/<str:rpsid>/", views.paymentSuccess),
    path("contact/", views.contactPage, name="contact"),
    path("forget-username/", views.forgetUsername, name="forget-username"),
    path("forget-otp/", views.forgetOTP, name="forget-otp"),
    path("forget-password/", views.forgetPassword, name="forget-password"),
    path("about/", views.about, name="about"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
