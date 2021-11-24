from captcha.widgets import ReCaptchaV2Invisible
from django import forms
from captcha.fields import ReCaptchaField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm

class SignupForm(UserCreationForm):
    username = forms.SlugField(required=True, min_length=5, max_length=10, help_text='Your Username should be Unique.', widget=forms.TextInput(attrs={
        'class' : 'form-control my-input lower',
        'placeholder' : 'Username',
        'type' : 'text'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class' : 'form-control my-input',
        'placeholder' : 'Email Address'
    }))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class' : 'form-control my-input',
        'placeholder' : 'Your Password'
    }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class' : 'form-control my-input',
        'placeholder' : 'Confirm Password'
    }))
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True , widget=forms.TextInput(attrs={
        'class' : 'form-control my-input capitalize',
        'placeholder' : 'First Name'
    }))
    last_name = forms.CharField(max_length=30, required=True , widget=forms.TextInput(attrs={
        'class' : 'form-control my-input capitalize',
        'placeholder' : 'Last Name'
    }))
    email = forms.EmailField(required=True , widget=forms.EmailInput(attrs={
        'class' : 'form-control my-input',
        'placeholder' : 'Email Address'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class' : 'form-control my-input',
        'placeholder' : 'Confirm Password'
    }))
    
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, error_messages={'required' : "You can't left this Empty"}, required=True , widget=forms.TextInput(attrs={
        'class' : 'form-control my-input lower',
        'placeholder' : 'Username'

    }))
    password = forms.CharField(required=True,error_messages={'required' : "Please Provide Password for Authentication"}, widget=forms.PasswordInput(attrs={
        'class' : 'form-control my-input',
        'placeholder' : 'Password',
        'errors' : 'Pleas'
    }))

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(required=True , widget=forms.EmailInput(attrs={
        'class' : 'form-control my-input',
        'placeholder' : 'Email Address'
    }))

class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(required=True, help_text="Provide a Strong Password", widget=forms.PasswordInput(attrs={
        'class' : 'form-control my-input',
        'placeholder' : 'Your New Password'
    }))
    new_password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class' : 'form-control my-input',
        'placeholder' : 'Confirm Your Password'
    }))

class PasswordChangeCustomForm(PasswordChangeForm):
    old_password =  forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class' : 'form-control my-input',
        'placeholder' : 'Old Password'
    }))
    new_password1 =  forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class' : 'form-control my-input',
        'placeholder' : 'New Password'
    }))
    new_password2 =  forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class' : 'form-control my-input',
        'placeholder' : 'Confirm New Password'
    }))
     