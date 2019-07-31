from django import forms

class DataForm(forms.Form):
    base= forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '30px'}))
    target = forms.EmailField(widget=forms.TextInput(attrs={'class':'special', 'size': '30px'}))
    date = forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '30px'}))
    maxdays = forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '30px'}))



