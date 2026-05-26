from django.contrib import admin

from .models import (
    Category,
    Product,
    Order,
    Review,
    UserProfile
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ['id', 'name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'name',
        'price',
        'stock',
        'seller'
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'buyer',
        'product',
        'quantity',
        'total_price',
        'status',
        'created_at'
    ]

    list_filter = ['status']

    list_editable = ['status']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'product',
        'user',
        'rating'
    ]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'user',
        'role'
    ]