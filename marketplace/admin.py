from django.contrib import admin

from .models import (
    Category,
    Product,
    Order,
    Review,
    UserProfile,
    Cart
)


# =========================================
# CATEGORY
# =========================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name'
    )

    search_fields = (
        'name',
    )


# =========================================
# PRODUCT
# =========================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'seller',
        'category',
        'price',
        'stock',
        'created_at'
    )

    list_filter = (
        'category',
        'created_at'
    )

    search_fields = (
        'name',
        'description'
    )

    list_editable = (
        'price',
        'stock'
    )

    ordering = (
        '-created_at',
    )


# =========================================
# ORDER
# =========================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'buyer',
        'product',
        'quantity',
        'total_price',
        'status',
        'created_at'
    )

    list_filter = (
        'status',
        'created_at'
    )

    search_fields = (
        'buyer__username',
        'product__name'
    )

    list_editable = (
        'status',
    )


# =========================================
# REVIEW
# =========================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'product',
        'rating',
        'created_at'
    )

    list_filter = (
        'rating',
    )

    search_fields = (
        'user__username',
        'product__name'
    )


# =========================================
# USER PROFILE
# =========================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'role'
    )

    list_filter = (
        'role',
    )

    search_fields = (
        'user__username',
    )


# =========================================
# CART
# =========================================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'product',
        'quantity',
        'created_at'
    )

    search_fields = (
        'user__username',
        'product__name'
    )

    list_filter = (
        'created_at',
    )