from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Product, Category
from django.contrib import messages

from .forms import RegisterForm, ProductForm, ReviewForm
from .models import (
    Product,
    UserProfile,
    Order,
    Review
)


# =========================================
# AUTO GET ROLE
# =========================================

def get_user_role(user):

    # JIKA ADMIN
    if user.is_superuser:

        return 'admin'

    # JIKA USER BIASA
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'role': 'buyer'
        }
    )

    return profile.role


# =========================================
# HOME
# =========================================

def home(request):

    products = Product.objects.all().order_by('-id')

    categories = Category.objects.all()

    category_id = request.GET.get('category')

    if category_id:

        products = products.filter(category_id=category_id)

    context = {

        'products': products,
        'categories': categories

    }

    return render(request, 'home.html', context)


# =========================================
# REGISTER
# =========================================

def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            UserProfile.objects.create(
                user=user,
                role=request.POST.get('role')
            )

            return redirect('login')

    else:

        form = RegisterForm()

    return render(request, 'register.html', {
        'form': form
    })


# =========================================
# LOGIN
# =========================================

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

    return render(request, 'login.html')


# =========================================
# LOGOUT
# =========================================

def logout_view(request):

    logout(request)

    return redirect('login')


# =========================================
# DASHBOARD
# =========================================

@login_required
def dashboard(request):

    role = get_user_role(request.user)

    # =========================================
    # DASHBOARD ADMIN
    # =========================================

    if role == 'admin':

        total_products = Product.objects.count()

        total_orders = Order.objects.count()

        total_users = User.objects.count()

        pending_orders = Order.objects.filter(
            status='pending'
        ).count()

        paid_orders = Order.objects.filter(
            status='paid'
        ).count()

        rejected_orders = Order.objects.filter(
            status='rejected'
        ).count()

        return render(
            request,
            'admin_dashboard.html',
            {
                'total_products': total_products,
                'total_orders': total_orders,
                'total_users': total_users,
                'pending_orders': pending_orders,
                'paid_orders': paid_orders,
                'rejected_orders': rejected_orders,
            }
        )

    # =========================================
    # DASHBOARD SELLER
    # =========================================

    elif role == 'seller':

        products = Product.objects.filter(
            seller=request.user
        )

        total_products = products.count()

        total_orders = Order.objects.filter(
            product__seller=request.user
        ).count()

        pending_orders = Order.objects.filter(
            product__seller=request.user,
            status='pending'
        ).count()

        paid_orders = Order.objects.filter(
            product__seller=request.user,
            status='paid'
        ).count()

        return render(
            request,
            'seller_dashboard.html',
            {
                'products': products,
                'total_products': total_products,
                'total_orders': total_orders,
                'pending_orders': pending_orders,
                'paid_orders': paid_orders,
            }
        )

    # =========================================
    # DASHBOARD BUYER
    # =========================================

    else:

        products = Product.objects.all()

        total_orders = Order.objects.filter(
            buyer=request.user
        ).count()

        pending_orders = Order.objects.filter(
            buyer=request.user,
            status='pending'
        ).count()

        completed_orders = Order.objects.filter(
            buyer=request.user,
            status='completed'
        ).count()

        return render(
            request,
            'buyer_dashboard.html',
            {
                'products': products,
                'total_orders': total_orders,
                'pending_orders': pending_orders,
                'completed_orders': completed_orders,
            }
        )

# =========================================
# ADD PRODUCT
# =========================================

@login_required
def add_product(request):

    role = get_user_role(request.user)

    # HANYA SELLER
    if role != 'seller':

        return render(
            request,
            'access_denied.html'
        )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            product = form.save(commit=False)

            product.seller = request.user

            product.save()

            return redirect('dashboard')

    else:

        form = ProductForm()

    return render(request, 'add_product.html', {
        'form': form
    })


# =========================================
# EDIT PRODUCT
# =========================================

@login_required
def edit_product(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    role = get_user_role(request.user)

    if role != 'seller':

        return render(
            request,
            'access_denied.html'
        )

    if request.user != product.seller:

        return HttpResponse(
            "Akses ditolak"
        )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            return redirect('dashboard')

    else:

        form = ProductForm(
            instance=product
        )

    return render(request, 'edit_product.html', {
        'form': form
    })


# =========================================
# DELETE PRODUCT
# =========================================

@login_required
def delete_product(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    role = get_user_role(request.user)

    if role != 'seller':

        return render(
            request,
            'access_denied.html'
        )

    if request.user != product.seller:

        return HttpResponse(
            "Akses ditolak"
        )

    product.delete()

    return redirect('dashboard')


# =========================================
# PRODUCT DETAIL
# =========================================

@login_required
def product_detail(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    reviews = Review.objects.filter(
        product=product
    )

    if request.method == 'POST':

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.product = product

            review.user = request.user

            review.save()

            return redirect(
                'product_detail',
                pk=pk
            )

    else:

        form = ReviewForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form
    })


# =========================================
# CHECKOUT
# =========================================

@login_required
def checkout(request, pk):

    product = get_object_or_404(Product, pk=pk)

    # hanya pembeli yang bisa checkout
    if request.user.userprofile.role != 'buyer':

        messages.error(
            request,
            'Hanya pembeli yang bisa checkout!'
        )

        return redirect('home')

    if request.method == 'POST':

        quantity = int(request.POST.get('quantity', 1))

        # cek stok
        if quantity > product.stock:

            messages.error(
                request,
                'Stok tidak mencukupi!'
            )

            return redirect('checkout', pk=pk)

        # hitung total harga
        total_price = product.price * quantity

        # kurangi stok
        product.stock -= quantity
        product.save()

        # simpan order
        Order.objects.create(
            buyer=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price,

            # STATUS AWAL
            status='Pending'
        )

        messages.success(
            request,
            'Pesanan berhasil dibuat dan sedang menunggu konfirmasi admin.'
        )

        return redirect('my_orders')

    return render(request, 'checkout.html', {
        'product': product
    })

# =========================================
# MY ORDERS
# =========================================

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        buyer=request.user
    ).order_by('-created_at')

    return render(request, 'my_orders.html', {
        'orders': orders
    })