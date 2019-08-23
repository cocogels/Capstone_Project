#Importing models to create database schema
from django.db import models
#importing AbstractUser to create custom user 
from django.utils.timezone import timezone

from django.contrib.auth.models import BaseUserManager, AbstractUser, User
from django.utils.translation import gettext, gettext_lazy as _

from django import forms

''' 
    We Creating or own User model in admin
    Creates and save user with the given email and password
'''
#Handling UserManager and overriding some stuffs in built function



class MarketingUserManager(BaseUserManager):
    def _create_user(self, email, password=None,):
        
        
        if not email:
            raise ValueError("The Given Email Must Be Set")

        if not password:
            raise ValueError("User Must Have a Password")

        user_obj = self.model(
            email=self.normalize_email(email),
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_centermanager_user(self, email, password=None,):
        user_obj = self._create_user(
            email,
            password=password,
            status=status,
        )
        user_obj.is_centermanager=True
        user_obj.save(using=self._db)
        return user_obj

    def create_centerbusinessmanager_user(self, email, password=None,):
        user_obj = self._create_user(
            email,
            password=password,
        )
        user_obj.is_centerbusinessmanager=True
        user_ob.save(using=self._db)
        return user_obj

    def create_marketinghead_user(self, email, password=None,):
        user_obj = self._create_user(
            email,
            password=password,
        )
        user_obj.is_marketinghead=True
        user_obj.save(using=self._db)
        return user_obj
   
    def create_registrar_user(self, email, password=None,):
        user_obj = self._create_user(
            email,
            password=password,
        )
        user_obj.is_registrar=True
        user_obj.save(using=self._db)
        return user_obj
    
    def create_superuser(self, email, password):
        user_obj = self._create_user(
            email,
            password=password,
        )
        user_obj.is_staff=True
        user_obj.is_superuser=True
        user_obj.save(using=self._db)
        return user_obj



''' -----------------------------------------------------------------------------------------'''


    
class UserMarketingProfile(AbstractUser):
    role_choices = (
        ('Budgetary','Budgetary'),
        ('ICL', 'ICL'),
        ('SHS', 'SHS'),
        ('IHE', 'IHE'),
    )
    username=None
    email                           = models.EmailField(verbose_name='Email Address',max_length=50, unique=True) 
    is_centermanager                = models.BooleanField(verbose_name='CenterManagerStatus', default=False)
    is_centerbusinessmanager        = models.BooleanField(verbose_name='CBM_Status', default=False)
    is_marketinghead                = models.BooleanField(verbose_name='MarketingHeadStatus', default=False)
    is_careerconsultant             = models.BooleanField(verbose_name='Career Consultant', default=False)
    is_registrar                    = models.BooleanField(verbose_name='Registrar Status', default=False)
    status                          = models.CharField(max_length=50, choices=role_choices, null=True, blank=True)
    timestamp                       = models.DateTimeField(auto_now_add=True)

    
    
    #redefining username change to email value
    USERNAME_FIELD = 'email'
    #Required Fields Optional
    REQUIRED_FIELDS = []
    
    objects = MarketingUserManager()
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.email   
    
    def get_short_name(self):
        return self.email    

''' Additional Properties Method that will give same result .admin or something else '''
@property
def is_staff(self):
    return self.is_centermanager
    
    
@property
def is_staff(self):
    return self.is_centerbusinessmanager
    
@property
def is_staff(self):
    return self.is_marketinghead

@property
def is_staff(self):
    return self.is_careerconsultant
    
@property
def is_staff(self):
    return self.is_registrar


'''------------------------------------------------------------------------------'''


    
class Profile(models.Model):
    
    emp_id       = models.AutoField(primary_key=True)
    user         = models.OneToOneField(UserMarketingProfile, on_delete=models.CASCADE,)
    first_name   = models.CharField(max_length=100, null=False, blank=False, )
    last_name    = models.CharField(max_length=100, null=False, blank=False, )
    address      = models.CharField(max_length=100, null=False, blank=False, )
    contact_no   = models.BigIntegerField(null=True)
    birth_date   = models.DateField(max_length=100, null=False, blank=False)

    def __str__(self):
        return 
    
   
    
