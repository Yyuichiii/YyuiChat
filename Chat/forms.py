from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate

class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control",'placeholder': 'Enter the Password'}))
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput(attrs={"class": "form-control",'placeholder': 'Enter the Confirm Password'})
    )
    class Meta:
        model=User
        fields=('username','password1','password2')
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter the UserName'})}
        

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter the UserName'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }
        

    error_messages = {
        "invalid_login": _(
            "Please enter the correct email/password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),}
    def get_invalid_login_error(self):
        return ValidationError(self.error_messages["invalid_login"],code="invalid_login",)
        
        
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        self.user_cache = authenticate(username=username, password=password)
            
        if self.user_cache is None:
            raise self.get_invalid_login_error()
        

 