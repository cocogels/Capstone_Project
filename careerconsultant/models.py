from django.db import models
from accounts.models import Profile
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField

class ICL_ContactCategoryModel(models.Model):
    name            = models.CharField(max_length=255)
    
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'ICL Contact Category'
        verbose_name_plural = 'ICL Contact Categories'

    def __str__(self):
        return self.name
    
class ICL_ContactModel(models.Model):
    
    icl_id          = models.AutoField(primary_key=True)
    name            = models.CharField(max_length=255)
    created_by      = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    org_type        = models.ForeignKey(ICL_ContactCategoryModel, on_delete=models.CASCADE, )
    telephone_number= models.BigIntegerField(null=True, blank=True, unique=True)
    phone_number    = models.BigIntegerField(null=True, unique=True)
    email           = models.CharField(max_length=255, null=True)
    c_person        = models.CharField(max_length=255, null=True)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateField(auto_now=True)
    
    class Meta:
        ordering            = ('-date_created',)
        verbose_name        = 'ICL Contact Detail'
        verbose_name_plural = 'ICL Contact Details'
    
    def __str__(self):
        return self.name
    
    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now




class SHS_ContactCategoryModel(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering            = ('name',)
        verbose_name        = 'SHS Contact Category'
        verbose_name_plural = 'SHS Contact Categories'
    
    def __str__(self):
        return self.name
    
    

class SHS_ContactModel(models.Model):
    
    shs_id          = models.AutoField(primary_key=True)
    shs_name        = models.CharField(max_length=255)
    shs_type        = models.ForeignKey(SHS_ContactCategoryModel, on_delete=models.CASCADE )
    c_number_tel    = models.BigIntegerField(null=True)
    c_number_cp     = models.BigIntegerField(null=True)
    email           = models.CharField(max_length=255, null=True)
    contact_person  = models.CharField(max_length=255, null=True)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateField(auto_now=True)
    

    class Meta:
        ordering            = ('-date_created',)
        verbose_name        = 'SHS Contact Detail'
        verbose_name_plural = 'SHS Contact Details'
    def __str__(self):
        return self.shs_name

        
    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now




class IHE_ContactCategoryModel(models.Model):

    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name = 'IHE Contact Category'
        verbose_name_plural = 'IHE Contact Categories'

    def __str__(self):
        return self.name


class IHE_ContactModel(models.Model):
    
    ihe_id          = models.AutoField(primary_key=True)
    ihe_name        = models.CharField(max_length=255)
    ihe_type        = models.ForeignKey(IHE_ContactCategoryModel, on_delete=models.CASCADE )
    c_number_tel    = models.BigIntegerField(null=True)
    c_number_cp     = models.BigIntegerField(null=True)
    email           = models.CharField(max_length=255, null=True)
    contact_person  = models.CharField(max_length=255, null=True)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateField(auto_now=True)
    

    class Meta:
        ordering            = ('-date_created',)
        verbose_name        = 'IHE Contact Detail'
        verbose_name_plural = 'IHE Contact Details'
    def __str__(self):
        return self.IHE_name

        
    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now


