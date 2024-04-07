from .models import Stock, Order
from django.forms import ModelForm, EmailField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = ("name","interval","upper_limit","lower_limit")