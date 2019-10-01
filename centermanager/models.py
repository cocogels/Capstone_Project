import datetime
#rom django.core.validators import MaxValueValidator, MinValueValidator
import calendar 

import arrow
from django.urls import reverse
from django.db import models    
from django.utils import timezone
from django.utils.text import slugify

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from django.conf import settings

 
''' School Year Database Table '''


class SchoolYear(models.Model):
    start_year      = models.DateField(unique=True, validators=settings.DATE_VALIDATORS)
    end_year        = models.DateField(unique=True, validators=settings.DATE_VALIDATORS)
    active_year     = models.BooleanField(default=False, help_text="This is Current School Year. There Can Only be one.")
    date_created    = models.DateField(_("Date Created"), auto_now_add=True,)
    

    @property
    def created_on_arrow(self):
        return arrow.get(self.date_created).humanize()

    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now

    def __str__(self):
        return str("{0}-{1}".format(self.start_year, self.end_year))

    def get_absolute_url(self):
        return reverse('view_year', kwargs={
            'pk': self.pk
        })

    def get_update_url(self):
        return reverse('update_year', kwargs={
            'pk': self.pk
        })

    def save(self, *args, **kwargs):
        super(SchoolYear, self).save(*args, **kwargs)
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
    date_created    = models.DateTimeField(_("Date Created"),auto_now_add=True)
    date_updated    = models.DateTimeField(_("Date Updated"),auto_now=True)
    
    
    @property
    def created_on_arrow(self):
        return arrow.get(self.date_created).humanize()
    
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


class CommissionStudentType(models.Model):

    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Student Type'

    def __str__(self):
        return self.name



class CommissionSetting(models.Model):

    student_type = models.ForeignKey(CommissionStudentType, on_delete=models.CASCADE)
    
    fee_choices = (
        (True, 'PAID'),
        (False, 'UNPAID'),
    )
    stud_choices = (
        (True, 'ENROLLED'),
        (False, 'DROP'),
    )
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
