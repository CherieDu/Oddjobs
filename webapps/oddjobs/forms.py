from django import forms
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.models import User
from models import *
from forms import *

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length = 42 , widget=forms.TextInput(attrs={'class':'form-control','type':'email','id':'email','placeholder':'Email'}))
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__exact=email):
            raise forms.ValidationError("No such user exists.")
        return email

class ResetForgotPasswordForm(forms.Form):
    # password1 = forms.CharField(max_length = 200, 
    #                             label='Password', 
    #                             widget=forms.PasswordInput(attrs={'class':'input-block-level form-control', 'placeholder':'Enter new password'}))
    # password2 = forms.CharField(max_length = 200,
    #                             label='Confirm Password',
    #                             widget=forms.PasswordInput(attrs={'class':'input-block-level form-control', 'placeholder':'Confirm Password'})) 
    password1 = forms.CharField(max_length = 42, 
                                label='Password', 
                                widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter new password'}))
    password2 = forms.CharField(max_length = 42,
                                label='Confirm Password',
                                widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}))

    def clean(self):
        cleaned_data = super(ResetForgotPasswordForm,self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

class ResetPasswordForm(forms.Form):
    user = User()
    old_password = forms.CharField(max_length = 200, 
                                label='Old Password', 
                                widget=forms.PasswordInput(attrs={'class':'form-control','type':'password','id':'password1','placeholder':'Old password'}))
    new_password = forms.CharField(max_length = 200,
                                label='New Password',
                                widget=forms.PasswordInput(attrs={'class':'form-control','type':'password','id':'password1','placeholder':'New password'}))   
    new_password_confirm = forms.CharField(max_length = 200,
                                label='Confirm New Password',
                                widget=forms.PasswordInput(attrs={'class':'form-control','type':'password','id':'password1','placeholder':'Confirm new password'}))
    
    def __init__(self, user=None, data=None):
        self.user = user
        super(ResetPasswordForm, self).__init__(data=data)
        
    def clean(self):
        cleaned_data = super(ResetPasswordForm,self).clean()
        user = User.objects.get(id = self.user.id)
        if  not user.check_password(cleaned_data.get('old_password')):
            raise forms.ValidationError("Old Password is incorrect.")
        password1 = cleaned_data.get('new_password')
        password2 = cleaned_data.get('new_password_confirm')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data
      
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 42,
                                 widget=forms.TextInput(attrs={'class':'form-control','type':'text','id':'username','placeholder':'Username'}))
    email = forms.CharField(max_length = 42,
                                 widget=forms.TextInput(attrs={'class':'form-control','type':'email','id':'email','placeholder':'Email'}))
    password1 = forms.CharField(max_length = 42, 
                                label='Password', 
                                 widget=forms.PasswordInput(attrs={'class':'form-control','type':'password','id':'password1','placeholder':'Password'}))
    password2 = forms.CharField(max_length = 42, 
                                label='Confirm password',  
                                widget=forms.PasswordInput(attrs={'class':'form-control','type':'password','id':'password2','placeholder':'Confirm Password'}))
    def clean(self):
        # Calls the parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # It must return the cleaned data it got from our parent.
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("This Email has already registered.")
        return email

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # It must return the cleaned data it got from the cleaned_data
        # dictionary
        return username