from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from .models import Product, Review


class RegisterForm(UserCreationForm):

    ROLE_CHOICES = (
        ('buyer', 'Pembeli'),
        ('seller', 'Penjual'),
    )

    email = forms.EmailField()

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'role'
        ]


class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = [
            'category',
            'name',
            'price',
            'stock',
            'description',
            'image'
        ]


class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review

        fields = [
            'rating',
            'comment'
        ]