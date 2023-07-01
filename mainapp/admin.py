from django.contrib import admin
from .models import *


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "username",
        "email",
        "phone",
        "addressline1",
        "addressline2",
        "addressline3",
        "pin",
        "city",
        "state",
        "pic",
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "maincategory",
        "subcategory",
        "brand",
        "seller",
        "baseprice",
        "discount",
        "finalprice",
        "size",
        "color",
        "discription",
        "stock",
        "pic1",
    ]


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "username",
        "phone",
        "addressline1",
        "addressline2",
        "addressline3",
        "pin",
        "city",
        "state",
        "pic",
    ]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["id", "buyer", "product"]


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "total",
        "shipping",
        "final",
        "buyer",
        "mode",
        "orderstatus",
        "paymentstatus",
        "rppid",
        "rpoid",
        "rpsid",
        "date",
    ]


@admin.register(CheckoutProduct)
class CheckoutProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "size",
        "color",
        "price",
        "qyt",
        "total",
        "pic",
        "checkout",
    ]


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ["id", "email"]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "phone", "subject", "message", "status"]
