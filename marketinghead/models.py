from django.db import models
from accounts.models import Profile
# Create your models here.




class Collateral(models.Model):
    
    c_id          = models.AutoField(primary_key=True)
    unit          = models.CharField(max_length=255, null=True) 
    quantity      = models.BigIntegerField(null=True)
    date_created  = models.DateTimeField(auto_now_add=True)
    date_updated  = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.unit
    
    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now

    class Meta:
        verbose_name_plural="Collateral"
        

class Budget(models.Model):
    
    b_id            = models.AutoField(primary_key=True)
    amount          = models.BigIntegerField(null=True)
    arrival    = models.DateField(null=True, blank=True)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)
    

    
    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now

    class Meta:
        verbose_name="Budget"
    




class AssignQuota(models.Model):

   
    user_profile          = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    start_month           = models.DateField(unique=True)
    end_month             = models.DateField(unique=True)
    a_senior_high         = models.BigIntegerField(null=True)
    a_higher_education    = models.BigIntegerField(null=True)
    a_retail              = models.BigIntegerField(null=True)
    a_corporate           = models.BigIntegerField(null=True)
    a_owwa                = models.BigIntegerField(null=True)
    date_created          = models.DateTimeField(auto_now_add=True)
    date_updated          = models.DateTimeField(auto_now=True)
    
    
    
 

    
        
class AssignTerritory(models.Model):
    
    territory_choices = (
        ('DISTRICT I', 'DISTRICT I'),
        ('DISTRICT II', 'DISTRICT II'),
        ('DISTRICT III', 'DISTRICT III'),
        ('DISTRICT IV', 'DISTRICT IV'),
        ('DISTRICT V', 'DISTRICT V'),
        ('DISTRICT VI', 'DISTRICT VI'),

    )
    user_profile         = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    territory_choices    = models.CharField(max_length=100, choices=territory_choices, null=True)
    date_created         = models.DateTimeField(auto_now_add=True)
    date_updated         = models.DateTimeField(auto_now=True)
