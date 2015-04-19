from django import forms
from django.contrib.auth.models import User
from lionstracksapp.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'password': forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'})
        }
        exclude = ('last_login', 'date_joined')