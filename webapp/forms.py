from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from .models import Ratings, UserProfile,Product

# CreateProductForm 
class CreateProductForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    price = forms.IntegerField()
    desc = forms.CharField(max_length=500)

    class Meta:
        model = Product
        fields = [
            'name',
            'desc',
            'price'
        ]

# CreateRatingForm
class CreateRatingForm(forms.ModelForm):
    text = forms.CharField(max_length=200)
    rating_num = forms.IntegerField()

    class Meta:
        model = Ratings
        fields =[
            'text',
            'rating_num'
        ]

# RegisterForm 
class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50,label="Username")
    email = forms.CharField(max_length=200,label="Email")

    class Meta:
        model = UserProfile
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
