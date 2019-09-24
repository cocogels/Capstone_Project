from django import forms
from django.db import transaction
from django.shortcuts import redirect, render
#Using built in forms function in django
import re
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField, AuthenticationForm
from accounts.models import Profile,User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _ 
from django.contrib import messages
from multiselectfield import MultiSelectField


                
class MinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length


    def validate(self, password, user=None):
        if len(password)< self.min_length:
           
            raise ValidationError(
                _("Passsword Must Contain at least %(min_length)d characters."),
                code='password_too_short',
                params={
                    'min_length': self.min_length
                },
            )
    def get_help_text(self):
        return _(
            "Your password must contain atleast %(min_length)d characters"%
            {'min_length': self.min_length}
        ) 
        
class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=100, required=False)
    class Meta:
        model = User
        fields = [
            'email',
            'is_centermanager',
            'is_centerbusinessmanager',
            'is_marketinghead',
            'is_registrar',   
        ]
        
        def __init__(self, *args, **kwargs):
            self.request_user = kwargs.pop('request_user', None)
            super(UserForm, self).__init__(*args, **kwargs)
            self.fields['email'].required = True
            if not self.instance.pk:
                self.fields['password'].required=True
        
        def clean_email(self):
            email = self.cleaned_data.get('email')
            if self.instance.id:
                if self.instance.eamil != email:
                    if not User.objects.filter(
                        email=self.cleaned_data.get("email")
                        ).exists():
                        return self.cleaned-data.get('email')
                    raise forms.ValidationError('Email already exists')
                else:
                    return self.cleaned_data.get('email')
            else:
                if not User.objects.filter(
                    email=self.cleaned_data.get("email")).exists():
                    return self.cleaned_data.get("email")
                raise forms.ValidationError('User already exists with this email')
                
        def clean_password(self):
            password = self.cleaned_data.get('password')
            if password:
                if len(password) < 8:
                    raise forms.ValidationError(
                        'Password Must be At Least 8 Characters Long'
                    )
            

class MarketingAdminUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email', 
            'password',
            )
    
class EmployeeCreationForm(forms.ModelForm):
    
    email        = forms.EmailField()
    first_name   = forms.CharField(required=False)
    last_name    = forms.CharField(required=False)
    address      = forms.CharField(required=False)
    password     = forms.CharField(max_length=50,label='Password' , widget=forms.PasswordInput())
    is_budgetary = forms.BooleanField(required=False, label='BUDGETARY')
    is_ihe       = forms.BooleanField(required=False, label='IHE')
    is_shs       = forms.BooleanField(required=False, label='SHS')
    is_icl       = forms.BooleanField(required=False, label='ICL')
    
    class Meta:
        model = User
        fields = (
            'email',
        )
    

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        query_set = User.objects.filter(email__iexact=email)
        if query_set.exists():
            raise forms.ValidationError('This email Already Registered..!!')
        return email

    def save(self, commit=True):
        #This would save the provided password in hashed format
        user = super(EmployeeCreationForm, self).save(commit=False)
        user = User(
            email                       = self.cleaned_data['email'],
            is_budgetary                = self.cleaned_data['is_budgetary'],
            is_ihe                      = self.cleaned_data['is_ihe'],
            is_shs                      = self.cleaned_data['is_shs'],
            is_icl                      = self.cleaned_data['is_icl'],
        )
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
        
        
class UserUpdateForm(forms.ModelForm):
    
    email = forms.EmailField(required=False)
    
    class Meta:
        model   = User
        fields   = ['email']
        

class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['contact_no','birth_date']
