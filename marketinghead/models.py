
import arrow
from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import User
# Create your models here.

from taggit.managers import TaggableManager


from django.conf import settings


class Collateral(models.Model):
    
    c_id          = models.AutoField(primary_key=True)
    name          = models.CharField(max_length=255, blank=True)
    unit          = models.CharField(max_length=255, null=True) 
    quantity      = models.BigIntegerField(null=True)
    date_created  = models.DateTimeField(_("Date Created"),auto_now_add=True)
    date_updated  = models.DateTimeField(_("Date Updated"),auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def created_on_arrow(self):
        return arrow.get(self.date_created).humanize()
    
    @property
    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()
    
    @property
    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now

    class Meta:
        verbose_name_plural="Collateral"
        

class Budget(models.Model):
    
    b_id            = models.AutoField(primary_key=True)
    amount          = models.BigIntegerField(null=True)
    arrival         = models.DateField(null=True, blank=True) 
    created_by      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_created    = models.DateTimeField(_("Date Created"),auto_now_add=True)
    date_updated    = models.DateTimeField(_("Date Updated"),auto_now=True)
    

    def __str__(self):
        return self.assigned_to
    
    @property
    def created_on_arrow(self):
        return arrow.get(self.date_created).humanize()
    
    @property
    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()
    
    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now

    class Meta:
        verbose_name="Budget"
    




class AssignQuota(models.Model):

   
    assigned_to           = models.ManyToManyField(User, related_name="assign_user")
    created_by            = models.ForeignKey(User, related_name='assign_created_by', on_delete=models.SET_NULL, null=True)
    start_month           = models.DateField(validators = settings.DATE_VALIDATORS)
    end_month             = models.DateField(validators = settings.DATE_VALIDATORS)
    a_senior_high         = models.BigIntegerField(null=True)
    a_higher_education    = models.BigIntegerField(null=True)
    a_retail              = models.BigIntegerField(null=True)
    a_corporate           = models.BigIntegerField(null=True)
    a_owwa                = models.BigIntegerField(null=True)
    is_active             = models.BooleanField(default=False)
    date_created          = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated          = models.DateTimeField(_("Date Updated"),auto_now=True)

    def __str__(self):
        return self.assigned_to
    
    @property
    def created_on_arrow(self):
        return arrow.get(self.date_created).humanize()
    
    @property
    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()
    
    
    class Meta:
        ordering = ['-date_created']    
 

    
        
class AssignTerritory(models.Model):
    
    territory_choices = (
        ('DISTRICT I', 'DISTRICT I'),
        ('DISTRICT II', 'DISTRICT II'),
        ('DISTRICT III', 'DISTRICT III'),
        ('DISTRICT IV', 'DISTRICT IV'),
        ('DISTRICT V', 'DISTRICT V'),
        ('DISTRICT VI', 'DISTRICT VI'),

    )
    user_profile         = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    assigned_to          = models.ManyToManyField(User, related_name="assign_territory_user")
    territory_choices    = models.CharField(max_length=100, choices=territory_choices, null=True)
    date_created         = models.DateTimeField(_("Date Created"),auto_now_add=True)
    date_updated         = models.DateTimeField(_("Date Updated"),auto_now=True)

    
    
    def __str__(self):
        return self.user_profile
    @property
    def created_on_arrow(self):
        return arrow.get(self.date_created).humanize()

    @property
    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()
    
    
    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now
    
    class Meta:
        ordering = ['-date_created']
