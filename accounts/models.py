#Importing models to create database schema
from django.db import models
#importing AbstractUser to create custom user 
from django.utils.timezone import timezone

from django.contrib.auth.models import BaseUserManager, AbstractUser, User, Group
from django.utils.translation import gettext, gettext_lazy as _
from multiselectfield import MultiSelectField
from taggit.managers import TaggableManager
import arrow    
from django import forms

''' 
    We Creating or own User model in admin
    Creates and save user with the given email and password
'''
#Handling UserManager and overriding some stuffs in built function



class MarketingUserManager(BaseUserManager):
    def _create_user(self, email, password=None):
        
        
        if not email:
            raise ValueError("The Given Email Must Be Set")

        if not password:
            raise ValueError("User Must Have a Password")
       
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_centermanager_user(self, email, password=None):
        user_obj = self._create_user(
            email,
            password=password,
        )
        user_obj.is_staff = True
        user_obj.is_centermanager=True
        user_obj.save(using=self._db)
        return user_obj

    def create_centerbusinessmanager_user(self, email, password=None):
        user_obj = self._create_user(
            email,
            password=password,
    
        )
        user_obj.is_staff = True
        user_obj.is_centerbusinessmanager=True
        user_ob.save(using=self._db)
        return user_obj

    def create_marketinghead_user(self, email, password=None):
        user_obj = self._create_user(
            email,
            password=password,
        )
        user_obj.is_staff = True
        user_obj.is_marketinghead=True
        user_obj.save(using=self._db)
        return user_obj
    
    def create_budgetary_user(self, email, password=None):
        user_obj = self._create_user(
            email,
            password=password,
        )
        user_obj.is_budgetary= True
        user_obj.save(using=self._db)
        return user_obj
    
    def create_ihe_user(self, email,  password=None):
        user_obj = self._create_user(
            email,
            password=password,
        )
        user_obj.is_ihe=True
        user_obj.save(using=self._db)
        return user_obj
    
    def create_icl_user(self, email, password=None):
        user_obj = self._create_user(
            email,
            password=password,
        )
        user_obj.is_icl=True
        user_obj.save(using=self._db)
        return user_obj
    
    def create__shs__user(self, email, password=None):
        user_obj = self._create_user(
            email,
            password=password,
        )
        user_obj.is_shs= True
        user_obj.save(using=self._db)
        return user_obj
   
    def create_registrar_user(self, email, password=None):
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



class User(AbstractUser):
    username=None
    email                           = models.EmailField(verbose_name='Email Address',max_length=50, unique=True) 
    first_name                      = models.CharField(verbose_name="First Name", max_length=50, blank=True)                                   
    last_name                       = models.CharField(verbose_name="Last Name", max_length=50, blank=True)                                    
    address                         = models.CharField(verbose_name="Address", max_length=50, blank=True)        
    is_centermanager                = models.BooleanField(verbose_name='CenterManagerStatus', default=False)
    is_centerbusinessmanager        = models.BooleanField(verbose_name='CBM_Status', default=False) 
    is_marketinghead                = models.BooleanField(verbose_name='MarketingHeadStatus', default=False)
    is_registrar                    = models.BooleanField(verbose_name='Registrar Status', default=False)
    is_budgetary                    = models.BooleanField(verbose_name='BUDGETARY', default=False)
    is_ihe                          = models.BooleanField(verbose_name='IHE', default=False)
    is_shs                          = models.BooleanField(verbose_name='SHS', default=False)
    is_icl                          = models.BooleanField(verbose_name='ICL', default=False)        
    date_joined                     = models.DateTimeField(_('Date Joined'),auto_now_add=True)

    
    
    #redefining username change to aemail value
    USERNAME_FIELD = 'email'
    #Required Fields Optional
    REQUIRED_FIELDS = []
    
    tags = TaggableManager()
    objects = MarketingUserManager()

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        full_name = None
        if self.first_name or self.last_name:
            full_name = self.first_name + " " + self.last_name

        else:
            full_name = self.email

        return full_name

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-is_active']

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
    return self.is_budgetary


@property
def is_staff(self):
    return self.is_ihe


@property
def is_staff(self):
    return self.is_shs


@property
def is_staff(self):
    return self.is_icl


@property
def is_staff(self):
    return self.is_registrar


'''------------------------------------------------------------------------------'''


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    contact_no = models.BigIntegerField(null=True)
    birth_date = models.DateField(max_length=100, null=False, blank=False)
    
    activation_key = models.CharField(max_length=50)
    key_expires    = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        self.key_expires = timezone.now() + datetime.timedelta(hours=2)
        super(Profile, self).save(*args, **kwargs)
