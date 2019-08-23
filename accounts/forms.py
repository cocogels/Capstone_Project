from django import forms
from django.db import transaction
from django.shortcuts import redirect, render
#Using built in forms function in django
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField, AuthenticationForm
from .models import Profile, UserMarketingProfile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _ 
from django.contrib import messages
from django.contrib.auth.models import Group


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    def __init__(self, request, *args, **kwargs):
        
        self.request = request
        
        super().__init__(*args,**kwargs)
        
    def clean(self):
        request     = self.request
        user_data   = self.cleaned_data
        
        email       = user_data.get("email")
        password    = user_data.get("password")
        
        #queryset = UserMarketingProfile.objects.filter(email=email)
        
        user = authenticate(
            email=email,
            password=password
        )
        
        if user is None:
            raise forms.ValidationError('Invalid Email/Password Try Again...!!')
        login(request, user)
        self.user = user
        return user_data
                
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
        
        
class UserRegistrationForm(forms.ModelForm):
    
    password   = forms.CharField(widget=forms.PasswordInput(),label='Password')
    role      = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label='Select Role')
    class Meta:
        model = UserMarketingProfile
        fields = [
            'email',
            'role',
            'password',
        ]
    
    '''
        using __init__ method to overwrrite and pass the parameters of 
        *args and **kwargs to help the instance method to validate the
        choices of role
    '''
    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            '''
           we getting the initial value as a key arguement to initialize
           the data
            '''
            initial = kwargs.setdefault('initial', {})
            '''
            This would check if the role has empty or already assign
            to specific user
            '''
            if kwargs['instance'].group.all():
                initial['role'] = kwargs['instance'].groups.all()[0]
            else:
                initial['role'] = None
                
        forms.ModelForm.__init__(self, *args, **kwargs)
    
    
  
    def save(self, commit=True):
        
        user.email  = self.cleaned_data('email')
        password    = self.cleaned_data.get('password')
        role        = self.cleaned_data.get('role')
        
        email_qs    = Employee.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('This email already used!')
        
        user.set_password(self.cleaned_data['password'])
        user.groups.ser([role])
        
        
        user = super(UserRegistrationForm, self).save(commit=False)
        if commit:
            user.save()
        return user
    
