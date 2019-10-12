import datetime
#rom django.core.validators import MaxValueValidator, MinValueValidator
import calendar 
from datetime import date
import arrow
import re
from django.urls import reverse
from django.db import models    
from django.utils import timezone
from django.utils.text import slugify

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from django.conf import settings


# def validate_year(year):
#     pattern = re.compile('^\d{8}%')
#     if not pattern.match(year):
#         raise ValidationError("{year} is not a valid year".format(year=year))
    
# def validate_start_year(start_year):
#     latest_start_year = SchoolYear.objects.aggregate(Max('start_year'))["start_year__max"]
#     latest_start_year = int(latest_start_year or 0)
    
#     if start_year <= latest_start_year:
#         raise ValidationError(
#             'Start year {start_year} must be greater than most recent'
#             'School Year start year{latest_start_year}'.format(
#                 start_year=start_year, latest_start_year=latest_start_year
#             )
#         )
# def validate_end_year(end_year):
#     latest_end_year = SchoolYear.objects.aggregate(Max('end_year'))["end_year__max"]
#     latest_end_year = int(latest_end_year or 1)
#     if end_year <= latest_end_year:
#         raise ValidationError(
#             'End year {end_year} must be grater than most recent'
#             'School Year end year {latest_end_year}'.format(
#                 end_year=end_year, latest_end_year=latest_end_year
#             )
#         )
    

class SchoolYearQuerySet(models.QuerySet):
    
    def start_year(self):
        return self.filter(start_year__gte=start_year)
    
    def end_year(self):
        return self.filter(end_year__lte=end_year)
    
    def school_year_range(self):
        return self.filter(school_year__range=(start_year(datetime.date.today().year-1, end_year(datetime.date.today().year+1 ))))
        
class SchoolYearManager(models.Manager):

    def get_queryset(self):
        return SchoolYearQuerySet(self.model, using=self._db)

    
class SchoolYearModel(models.Model):
    start_year      = models.DateField(unique=True)
    end_year        = models.DateField(unique=True)
    active_year     = models.BooleanField(default=False, help_text="This is Current School Year. There Can Only be one.")
    date_created    = models.DateField(_("Date Created"), auto_now_add=True,)
    
    school_year = SchoolYearManager()
    

    @property
    def created_on_arrow(self):
        return arrow.get(self.date_created).humanize()

    @property
    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now

    def __str__(self):
        return str("{0}-{1}".format(self.start_year, self.end_year))



    def save(self, *args, **kwargs):
        super(SchoolYearModel, self).save(*args, **kwargs)
        if self.active_year:
            all = SchoolYear.objects.exclude(id=self.id).update(active_year=False)
    
    class Meta:
        verbose_name_plural = 'School Year'
        ordering = ['-date_created', ]
        
        
        

''' Target Sheet Database Table '''

class TargetSheet(models.Model):
    
    corporate       = models.BigIntegerField(null=True,)
    retail          = models.BigIntegerField(null=True,)
    owwa            = models.BigIntegerField(null=True,)
    seniorhigh      = models.BigIntegerField(null=True,)
    higher_ed       = models.BigIntegerField(null=True,)
    school_year     = models.ForeignKey(SchoolYearModel, on_delete=models.CASCADE, null=True)
    active          = models.BooleanField(default=False)
    date_created    = models.DateTimeField(_("Date Created"),auto_now_add=True)
    date_updated    = models.DateTimeField(_("Date Updated"),auto_now=True)
    
    
    
    
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
        verbose_name_plural = 'Target Sheet'
        ordering = ['-date_created', '-date_updated']


''' Matriculation Database Table '''

''' Status Category '''


class MatriculationStatusCategory(models.Model):

    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Matriculation Status Category'
        verbose_name_plural = 'Matriculation Status Categories'

    def __str__(self):
        return self.name


''' Course Category'''


class MatriculationCourseCategory(models.Model):

    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Matriculation Course Category'
        verbose_name_plural = 'Matriculation Course Categories'

    def __str__(self):
        return self.name


''' ICL Category '''


class MatriculationICLCategory(models.Model):

    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Matriculation ICL Category'
        verbose_name_plural = 'Matriculation ICL Categories'

    def __str__(self):
        return self.name


class Matriculation(models.Model):

    payment_details_id = models.AutoField(primary_key=True)
    status = models.ForeignKey(
        MatriculationStatusCategory, on_delete=models.CASCADE)
    course = models.ForeignKey(
        MatriculationCourseCategory, on_delete=models.CASCADE)
    cash_amount_per_unit = models.BigIntegerField(null=True)
    cash_miscellaneous_fee = models.BigIntegerField(null=True)
    cash_lab_fee = models.BigIntegerField(null=True)
    cash_registration_fee = models.BigIntegerField(null=True)
    ins_amount_unit = models.BigIntegerField(null=True)
    ins_miscellaneous_fee = models.BigIntegerField(null=True)
    ins_lab_fee = models.BigIntegerField(null=True)
    ins_registration_fee = models.BigIntegerField(null=True)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True)

    @property
    def created_on_arrow(self):
        return arrow.get(self.date_created).humanize()

    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()

    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now

    class Meta:
        verbose_name_plural = 'Payment Details'
        ordering = ['-date_created']


''' Sanction Settings Database Table '''
class SanctionSetting(models.Model):

    first_sanction = models.CharField(
        max_length=255, blank=False, default="Verbal Warning")
    second_sanction = models.CharField(
        max_length=255, blank=False, default="Written Explanation")
    third_sanction = models.CharField(
        max_length=255, blank=False, default="Three Days Suspension")
    fourth_sanction = models.CharField(
        max_length=255, blank=False, default="Six Days Suspension")
    fifth_sanction = models.CharField(
        max_length=255, blank=False, default="Termination")
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True)

    @property
    def created_on_arrow(self):
        return arrow.get(self.date_created).humanize()

    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()

    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now

    class Meta:
        verbose_name_plural = 'Sanction Details'
        ordering = ['-date_created']


''' Commission Setting Database Table '''



class CommissionSetting(models.Model):
    student_choices = (
    (1, 'SHS'),
    (2, 'RegularClass'),
    (3, 'NightCLass'),
    )
    fee_choices = (
        (True, 'PAID'),
        (False, 'UNPAID'),
    )
    stud_choices = (
        (True, 'ENROLLED'),
        (False, 'DROP'),
    )
    student_type = models.BooleanField(choices=student_choices)
    tuition_percentage = models.SmallIntegerField(null=True)
    misc_fee_status = models.BooleanField(choices=fee_choices,)
    reg_fee_status = models.BooleanField(choices=fee_choices,)
    stud_fee_status = models.BooleanField(choices=stud_choices,)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def __str__(self):
        return self.student_type

    def created_on_arrow(self):
        return arrow.get(self.date_created).humanize()

    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()

    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now

    class Meta:
        verbose_name_plural = 'Commision Details'
        ordering = ['-date_created']
