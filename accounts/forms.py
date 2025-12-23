
from django.contrib.auth.forms import UserCreationForm
from django import forms
class UserCreateForm(UserCreationForm):
    address = forms.CharField(max_length=400)
    phone_number = forms.CharField(max_length=15)
    class Meta(UserCreationForm.Meta):
        fields = ["username","first_name","email","password1","password2"]