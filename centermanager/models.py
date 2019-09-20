import datetime
#rom django.core.validators import MaxValueValidator, MinValueValidator
import calendar 


from django.db import models    
from django.utils import timezone
from django.utils.text import slugify

from django.utils.translation import ugettext_lazy as _
# Create your models here.

from django.core.exceptions import ValidationError





# def current_year():
#     return datetime.date.today().year
    
# def max_value_current_year(value):
#     return MaxValueValidator(current_year())(value)

# start_year  = models.IntegerField(_('start_year'), unique_for_year=True ,validators=[MinValueValidator(2017), max_value_current_year], null=True)

# class SchoolYearManager(models.Manager):
    
#     def validate_year(self, start_year, end_year):
#         errors =[]
#         if start_year and end_year:
#             if start_year < end_year:
#                 errors.append('End Year Cannot be Earlier Than Start Year')
            
#             if start_year < datetime.date.today().year+1:
#                 errors.append('Year Cannot be in Past..!')

#             if end_year > datetime.date.today().year+5:
#                 errors.append('Year Cannot be Six Years A Head..!')



class SchoolYear(models.Model):
    start_year   = models.DateField(unique=True)
    end_year     = models.DateField(unique=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    date_updated = models.DateField(auto_now=True, null=True)
    
 #   objects = SchoolYearManager()
    class Meta:
        verbose_name_plural = 'School Year'
        ordering = ['-date_created',]
        
    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now
        
    def __str__(self):
        return str("{0}-{1}".format(self.start_year, self.end_year))

class TargetSheet(models.Model):

    ts_id           = models.AutoField(primary_key=True)
    corporate       = models.BigIntegerField(null=True,)
    retail          = models.BigIntegerField(null=True,)
    owwa            = models.BigIntegerField(null=True,)
    seniorhigh      = models.BigIntegerField(null=True,)
    higher_ed       = models.BigIntegerField(null=True,)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)
  
    class Meta:      
        verbose_name_plural = 'Target Sheet'
        ordering = ['-date_created','-date_updated']
    
    def get_absolute_url(self):
        return reverse("centermanager:target_details", kwargs={"id": self.id})
    
    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now


class MatriculationStatusCategory(models.Model):

    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Matriculation Status Category'
        verbose_name_plural = 'Matriculation Status Categories'

    def __str__(self):
        return self.name
        
 
class MatriculationCourseCategory(models.Model):
    
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Matriculation Course Category'
        verbose_name_plural = 'Matriculation Course Categories'

    def __str__(self):
        return self.name
        

class PaymentDetails(models.Model):
 
    status_choices =(
        ('regular', 'RegularClass'),
        ('nightclass', 'NightClass')
    )
    status = models.CharField(
        max_length=50,
        choices=status_choices,
        default='regular'
    )
    
    course_choices = (
        ('bsit','BSIT'),
        ('bsba','BSBA'),
        ('shs','SHS'),
    )
    
    course = models.CharField(
        max_length=50,
        choices=course_choices,
        default='bsit',
    )
    payment_details_id      = models.AutoField(primary_key=True)
    cash_amount_per_unit    = models.BigIntegerField(null=True)
    cash_miscellaneous_fee  = models.BigIntegerField(null=True)
    cash_lab_fee            = models.BigIntegerField(null=True)
    cash_registration_fee   = models.BigIntegerField(null=True)
    ins_amount_unit         = models.BigIntegerField(null=True)
    ins_miscellaneous_fee   = models.BigIntegerField(null=True)
    ins_lab_fee             = models.BigIntegerField(null=True)
    ins_registration_fee    = models.BigIntegerField(null=True)
    date_created            = models.DateTimeField(auto_now_add=True)
    date_updated            = models.DateTimeField(auto_now=True)
    
    
    
    class Meta:
        verbose_name_plural ='Payment Details'


    def get_absolute_url(self):
        return f'{self.slug}'
    
    def get_update_url(self):
        self.slug = slugify(self.title)
        super(Paymentdetails, self).save(*args,**kwargs)
        
    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now


class SanctionSetting(models.Model):

    ss_id = models.AutoField(primary_key=True)
    first_sanction  = models.CharField(max_length=255, blank=False, default="Verbal Warning")
    second_sanction = models.CharField(max_length=255, blank=False, default="Written Explanation")
    third_sanction  = models.CharField(max_length=255, blank=False, default="Three Days Suspension")
    fourth_sanction = models.CharField(max_length=255, blank=False, default="Six Days Suspension")
    fifth_sanction  = models.CharField(max_length=255, blank=False, default="Termination")
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)
    

    
    def date_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_added <= now
    
    class Meta:
        verbose_name_plural ='Sanction Settings'
        
    


# def valid_pct(val):
#     if val.endwith("%"):
#         return float(val[:-1])/100
#     else:
#         try:
#             return float(val)
#         except ValueError:
#             raise ValidationError(
#                 _('%(value)s is not a valid pct'),
#                 params={'value': value},
#             )
class CommissionSetting(models.Model):
    fee_choices = (
                    (True, 'PAID'), 
                    (False ,'UNPAID'),
                    )
    stud_choices    = (
                    (True, 'ENROLLED'), 
                    (False,'DROP'), 
                    )
    
    
    cs_id              = models.AutoField(primary_key=True)
    tuition_percentage = models.SmallIntegerField(null=True)
    misc_fee_status    = models.BooleanField(choices=fee_choices,)
    reg_fee_status     = models.BooleanField(choices=fee_choices,)
    stud_fee_status    = models.BooleanField(choices=stud_choices,)
    date_created       = models.DateTimeField(auto_now_add=True)
    date_updated       = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def date_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_added <= now
    
    class Meta:
        
        verbose_name_plural = 'Commission Settings'
