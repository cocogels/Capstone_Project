# rom django.core.validators import MaxValueValidator, MinValueValidator
import calendar
import datetime
import re
from datetime import timedelta

import arrow
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import BooleanField, Case, F, Q, Value, When
from django.db.models.functions import TruncYear
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

# def validate_year(year):
#     pattern = re.compile('^\d{8}%')
#     if not pattern.match(year):
#         raise ValidationError("{year} is not a valid year".format(year=year))

#   all = TargetSheet.objects.exclude(id=self.id).update(active_year=False)


class SchoolYearQuerySet(models.QuerySet):

    def start_year(self):
        return self.filter(start_year__gte=start_year)

    def end_year(self):
        return self.filter(end_year__lte=end_year)


    def date_trunc_year(self):
        SchoolYear.objects.annonate(
            year=TruncYear(Q('start_year') | Q('end_year')).values('year')
        )

class SchoolYearManager(models.Manager):

    def get_queryset(self):
        return SchoolYearQuerySet(self.model, using=self._db)

def get_end_year():
    return datetime.date.today() + timedelta(days=365)

def get_start_year():
    return datetime.date.today()
class SchoolYear(models.Model):
    
    
<<<<<<< HEAD
    start_year = models.DateField(unique=True, default=get_start_year)
    end_year = models.DateField(unique=True, default=get_end_year)
    active_year = models.BooleanField(default=False, help_text="This is Current School Year. There Can Only be one.")
    date_created = models.DateField(_('Date Created'), auto_now_add=True)
   
    @property
    def start_date(self):
        return self.start_year + timedelta(days=365)
    
    
    def end_date(self):
        return datetime.date.today() < end_year
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.active_year=(self.start_date <= self.end_year)
        super(SchoolYear, self).save(*args, **kwargs)        
        if self.id:
            if self.active_year:
                SchoolYear.objects.filter(end_year__lte=self.start_year).exclude(id=self.id).update(active_year=False)
=======
    school_year = SchoolYearManager()
  
>>>>>>> 180452339520ca24726b23483e4e66d43307c895

    def __str__(self):
        return '{}'.format(self.active_year)
    
    def get_absolute_url(self):
        return reverse("create_school_year", kwargs={"pk": self.pk})
    
    @property
    def created_on_arrow(self):
        return arrow.get(self.date_created).humanize
    
    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now
    
        class Meta:
            verbose_name_plural = 'School Year'
            ordering = ['date_created']

            school_year = SchoolYearManager()

''' Target Sheet Database Table '''


class TargetSheet(models.Model):
    corporate = models.BigIntegerField(null=False, blank=False)
    retail = models.BigIntegerField(null=False, blank=False)
    owwa = models.BigIntegerField(null=False, blank=False)
    seniorhigh = models.BigIntegerField(null=False, blank=False)
    higher_ed = models.BigIntegerField(null=False, blank=False)
    active_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    date_created = models.DateField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateField(_("Date Updated"), auto_now=True)

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


# class MatriculationInstallement(models.Model):
#     status = models.ForeignKey(
#         MatriculationStatusCategory, on_delete=models.CASCADE)
#     course = models.ForeignKey(
#         MatriculationCourseCategory, on_delete=models.CASCADE)
#     ins_amount_unit = models.BigIntegerField(null=True)
#     ins_miscellaneous_fee = models.BigIntegerField(null=True)
#     ins_lab_fee = models.BigIntegerField(null=True)
#     ins_registration_fee = models.BigIntegerField(null=True)
#     date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
#     date_updated = models.DateTimeField(_("Date Updated"), auto_now=True)

#     @property
#     def created_on_arrow(self):
#         return arrow.get(self.date_created).humanize()

#     def updated_on_arrow(self):
#         return arrow.get(self.date_updated).humanize()

#     def date_created_recently(self):
#         now = timezone.now()
#         return now - datetime.timedelta(days=1) <= self.date_created <= now

#     class Meta:
#         verbose_name_plural = 'Payment Cash Details'
#         ordering = ['-date_created']

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
        verbose_name_plural = 'Payment Cash Details'
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
