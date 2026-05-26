from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('add-product/', views.add_product, name='add_product'),

    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),

    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),

    path('checkout/<int:pk>/', views.checkout, name='checkout'),

    path('my-orders/', views.my_orders, name='my_orders'),
    
    path(
    'product/<int:pk>/',
    views.product_detail,
    name='product_detail'
    ),

]