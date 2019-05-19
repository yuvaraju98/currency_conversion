from django import forms
from .models import user_info

class RegisterForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '30px'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'special', 'size': '30px'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '30px'}))


class login_form(forms.Form):

    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'special', 'size': '30px'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '30px'}))

class chat(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'special', 'size': '80px'}))

