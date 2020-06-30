from django.forms import ModelForm
import django.forms as forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ['user', 'category']

class UpdateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['profile_pic']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
    label=("Password"),
    strip=False,
    widget=forms.PasswordInput,
    # help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
        help_texts = {
            'username': None,
            'email': None,
        }

