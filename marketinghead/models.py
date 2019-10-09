
import arrow
from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import User
# Create your models here.
import datetime
from datetime import date
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
        return str(self.arrival)
    
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
    

class SchoolDays(models.Model):
    active      = models.BooleanField(default=False)
    start_date  = models.DateField(validators=settings.DATE_VALIDATORS)
    end_date    = models.DateField(validators=settings.DATE_VALIDATORS)
    show_reports= models.BooleanField(default=True)
    #school_year = models.ForeignKey(SchoolYear, on_delete=models.SET_NULL, null=True)
    school_days = models.BooleanField(default=False, blank=True, null=True, help_text='if set this will ne the number of school days is in session. if unset, the value is calculated by the days off.')
    monday      = models.BooleanField(default=True)
    tuesday     = models.BooleanField(default=True)
    wenesday    = models.BooleanField(default=True)
    thursday    = models.BooleanField(default=True)
    friday      = models.BooleanField(default=True)
    saturday    = models.BooleanField(default=False)
    sunday      = models.BooleanField(default=False)
    
    
    
    def get_number_days(self, date=datetime.date.today()):
        '''Get The Number of School Days '''

        if self.school_days or self.school_days == 0 and date >= self.end_date:
            return self.school_days

        day = 0
        current_date = self.start_date
        while current_day <= date:
            is_day = False
            if current_date >= self.start_date and current_date <= self.end_date:
                days_off = []
                for d in self.daysoff_set.all().values_list('date'):
                    days_off.append(d[0])
                if not current_date in days_off:
                    if self.monday and current_day.isoweekday() == 1:
                        is_day = True
                    elif self.tuesday and current_day.isoweekday() == 2:
                        is_day = True
                    elif self.wenesday and current_day.isoweekday() == 3:
                        is_day = True
                    elif self.thursday and current_day.isoweekday() == 4:
                        is_day = True
                    elif self.friday and current_day.isoweekday() == 5:
                        is_day = True
                    elif self.saturday and current_day.isoweekday() == 6:
                        is_day = True
                    elif self.sunday and current_day.isoweekday() == 7:
                        is_day = True
            if is_day:
                day += 1
            current_dae += datetime.timedelta(days=1)
            return day

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
        (1 , 'DISTRICT I'),
        (2 , 'DISTRICT II'),
        (3 , 'DISTRICT III'),
        (4 , 'DISTRICT IV'),
        (5 , 'DISTRICT V'),
        (6 , 'DISTRICT VI'),

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
