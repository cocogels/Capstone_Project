from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group 
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserMarketingProfile, Profile
#from .forms import UserCreationForm, UserChangeForm
#Register your models here.
from django import forms





''' Handling User Creation Form include all Required '''
class MarketingAdminUserCreationForm(UserCreationForm):
    
    email       = forms.EmailField(max_length=50,required=True)
    password1   = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2   = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
    
    class Meta:
        model = UserMarketingProfile
     
        fields = (
                'email',
                'status',
                  )
        
        
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
            if kwargs['instance'].UserMarketingProfile.all():
                initial['status'] = kwargs['instance'].status.all()[0]
            else:
                initial['stauts'] = None
                
        UserCreationForm.__init__(self, *args, **kwargs)   
    '''-------------------------------------------------------------'''    
    def clean_password2(self):
        #Checking if the user password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match.!")
        return password2
    
    
    '''-------------------------------------------------------------'''
    def save(self, commit=True):
        #This would save the provided password in hashed format
        user = super(MarketingAdminUserCreationForm, self).save(commit=False)
        user.status = self.cleaned_data['status']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class MarketingAdminUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = UserMarketingProfile
        fields = ('email','password',)
        
    def clean_password(self):
        #what ever the user provides it will return the initial value
        return self.initial['password']




class UserAdmin(BaseUserAdmin):
    form =  MarketingAdminUserChangeForm
    add_form = MarketingAdminUserCreationForm
    fieldsets = (
        (
            None,
            {
                "fields": ('email','password','status'),
            },
        ),
        (
            "Permissions",
            {
                "fields":
                    (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_centermanager",
                    "is_centerbusinessmanager",
                    "is_marketinghead",
                    "is_registrar",
                    "user_permissions",
                    )
            },
        ),
        (
            "Important dates",
            {
                "fields":
                    (
                        "last_login",
                        "date_joined"
                    )
            },
        ),
    )
    
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields":
                    (
                        "email",
                        'status',
                        "password1",
                        "password2",
                        
                    ),
            },
        ),
    )
    
    list_display = (
        "email",
        "is_staff",
        "is_active"
    )
    
    search_fields = (
        "email",
    )
    
    ordering = (
        "email",
    )
    
    filter_horizontal = ()

admin.site.register(UserMarketingProfile, UserAdmin,)
admin.site.register(Profile)





"""-----------------------------------------------------"""



class MarketingHeadAdminSite(AdminSite):
    site_header = 'MarketingHead Administration'

    def has_permission(self, request):
        return(
            request.user.is_active and request.user.is_marketinghead
        )
    
   

admin_marketinghead_site = MarketingHeadAdminSite(name='marketinghead')
admin_marketinghead_site.register(Profile)











    
admin.site.site_header = 'Marketing Administration'
admin.site.site_title = 'Marketing Administration'


