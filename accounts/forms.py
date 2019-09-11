from django import forms
from django.db import transaction
from django.shortcuts import redirect, render
#Using built in forms function in django
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, UserMarketingProfile
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
        

class MarketingAdminUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserMarketingProfile
        fields = (
            'email', 
            'password',
            )
    

# class RoleForm(forms.ModelForm):
    
#     class Meta:
#         model = Role
#         fields = (
#             '',
#         )

#         labels = {
#             'user_role': "UserType",
#         }
        

            
#     def save(self, commit=True):
#         user = super(RoleForm, self).save(commit=False)
#         user = Role(
#             user_role=self.cleaned_data['user_role']
#         )
#         if commit:
#             user.save()
#         return user

class EmployeeCreationForm(forms.ModelForm):
    
    email        = forms.EmailField()
    password     = forms.CharField(max_length=50,label='Password' , widget=forms.PasswordInput())
    is_budgetary = forms.BooleanField(required=False, label='BUDGETARY')
    is_ihe       = forms.BooleanField(required=False, label='IHE')
    is_shs       = forms.BooleanField(required=False, label='SHS')
    is_icl       = forms.BooleanField(required=False, label='ICL')
    
    class Meta:
        model = UserMarketingProfile
        fields = (
            'email',
        )
    

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        query_set = UserMarketingProfile.objects.filter(email__iexact=email)
        if query_set.exists():
            raise forms.ValidationError('This email Already Registered..!!')
        return email

    def save(self, commit=True):
        #This would save the provided password in hashed format
        user = super(EmployeeCreationForm, self).save(commit=False)
        user = UserMarketingProfile(
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
        model   = UserMarketingProfile
        fields   = ['email']
        

class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['first_name','last_name','address','contact_no','birth_date']
