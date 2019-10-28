# rom django.core.validators import MaxValueValidator, MinValueValidator
import calendar
import datetime
import re
from datetime import timedelta, date

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
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
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


    # def date_trunc_year(self):
    #     SchoolYear.objects.annonate(
    #         year=TruncYear(Q('start_year') | Q('end_year')).values('year')
    #     )

class SchoolYearManager(models.Manager):
    def active(self):
        return super().get_queryset().filter(active_year=True)
    
    def inactive(self):
        return super().get_queryset().filter(active_year=False)
    
    
    def get_queryset(self):
        return SchoolYearQuerySet(self.model, using=self._db)


class SchoolYear(models.Model):
    
    
    start_year = models.DateField(unique=True)
    end_year = models.DateField(unique=True)
    active_year = models.BooleanField(default=False, help_text="This is Current School Year. There Can Only be one.")
    date_created = models.DateField(_('Date Created'), auto_now_add=True)
   
    @property
    def start_date(self):
        return self.start_year + timedelta(days=365)


    def save(self, *args, **kwargs):
        if self.id is None:
            self.active_year = self.start_year <= self.end_year
        super(SchoolYear, self).save(*args, **kwargs)        
        if self.pk is not None:
            if self.active_year == True:
                SchoolYear.objects.filter(end_year__lte=date.today()).exclude(id=self.id).update(active_year=False)    
            elif self.active_year == False:
                SchoolYear.objects.filter(start_year__gte=date.today()).update(active_year=True)
            else:
                self.active_year=False
                
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

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})
    
    class Meta:
        verbose_name_plural = 'Target Sheet'
        ordering = ['-date_created', '-date_updated']


''' Matriculation Database Table '''
class MatriculationSeniorHighSchool(models.Model):
    matriculation_shs       = models.AutoField(primary_key=True)
    registration_fee        = models.BigIntegerField(null=False, blank=False)
    miscellaneous_fee       = models.BigIntegerField(null=False, blank=False)
    laboratry_fee           = models.BigIntegerField(null=False, blank=False)
    id_fee                  = models.BigIntegerField(null=False, blank=False)
    unit_fee_cash           = models.BigIntegerField(null=False, blank=False)
    unit_fee_installment    = models.BigIntegerField(null=False, blank=False)
    date_updated            = models.DateField(_('Date Updated'), auto_now=True)
        
    @property
    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()
    
    class Meta:
        verbose_name_plural = 'Matriculation Senior High School'
        ordering = ['-date_updated']

class MatriculationHigherEducationNC(models.Model):
    higher_educ_nc          = models.AutoField(primary_key=True)
    registration_fee        = models.BigIntegerField(null=False, blank=False)
    miscellaneous_fee       = models.BigIntegerField(null=False, blank=False)
    laboratry_fee           = models.BigIntegerField(null=False, blank=False)
    id_fee                  = models.BigIntegerField(null=False, blank=False)
    unit_fee_cash           = models.BigIntegerField(null=False, blank=False)
    unit_fee_installment    = models.BigIntegerField(null=False, blank=False)
    date_updated            = models.DateField(_('Date Updated'), auto_now=True)

    
    
    @property
    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()
    
    class Meta:
        verbose_name_plural = 'Matriculation Higher Education Night Class'
        ordering = ['-date_updated']

    
class MatriculationHigherEducationRC(models.Model):
    higher_educ_rc          = models.AutoField(primary_key=True)
    registration_fee        = models.BigIntegerField(null=False, blank=False)
    miscellaneous_fee       = models.BigIntegerField(null=False, blank=False)
    laboratry_fee           = models.BigIntegerField(null=False, blank=False)
    id_fee                  = models.BigIntegerField(null=False, blank=False)
    unit_fee_cash           = models.BigIntegerField(null=False, blank=False)
    unit_fee_installment    = models.BigIntegerField(null=False, blank=False)
    date_updated            = models.DateField(_('Date Updated'), auto_now=True)
    
    @property
    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()
    
    class Meta:
        verbose_name_plural = 'Matriculation Senior High School'
        ordering = ['-date_updated']

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


class CommissionSettingSHS(models.Model):
    stud_choices = (
        (True, 'ENROLLED'),
        (False, 'DROP')        
    )
    commission_shs  = models.AutoField(primary_key=True)
    student         = models.IntegerField(null=False, blank=False)
    student_choices = models.BooleanField(choices=stud_choices)
    tuition_regex   = RegexValidator(regex='^\d+.\d+%+$')
    tuition_fee     = models.CharField(max_length=4, validators=[tuition_regex])
    date_updated    = models.DateField(_('Date Updated'), auto_now=True)
    
    
    @property
    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()
    
    class Meta:
        verbose_name_plural = 'Commission Setting SHS'



class CommissionSettingHENC(models.Model):
    stud_choices = (
        (True, 'ENROLLED'),
        (False, 'DROP')        
    )
    commission_shs  = models.AutoField(primary_key=True)
    student         = models.IntegerField(null=False, blank=False)
    student_choices = models.BooleanField(choices=stud_choices)
    tuition_regex   = RegexValidator(regex='^\d+.\d+%+$')
    tuition_fee     = models.CharField(max_length=4, validators=[tuition_regex])
    date_updated    = models.DateField(_('Date Updated'), auto_now=True)
    
    
    @property
    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()
    
    class Meta:
        verbose_name_plural = 'Commission Setting Higher Education Night Class'


class CommissionSettingHERC(models.Model):
    stud_choices = (
        (True, 'ENROLLED'),
        (False, 'DROP')
    )
    commission_shs = models.AutoField(primary_key=True)
    student = models.IntegerField(null=False, blank=False)
    student_choices = models.BooleanField(choices=stud_choices)
    tuition_regex = RegexValidator(regex='^\d+.\d+%+$')
    tuition_fee = models.CharField(max_length=4, validators=[tuition_regex])
    date_updated = models.DateField(_('Date Updated'), auto_now=True)

    @property
    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()

    class Meta:
        verbose_name_plural = 'Commission Setting Higher Education Regular Class'



class CommissionSettingICL(models.Model):
    total_regex      = RegexValidator(regex='^\d+.\d+%+$')
    total_collection = models.CharField(max_length=4, validators=[total_regex])
    date_update      = models.DateField(_('Date Updated'), auto_now=True)
    
    @property
    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()
    
    class Meta:
        verbose_name_plural = 'Commission Setting ICl'    
    
    
    
    
    
    
    
    # tuition_fee     = models.FloatField(validators = [
    #     MinValueValidator(0.0), MaxValueValidator(100.0)
    # ])

# class CommissionSetting(models.Model):
#     student_choices = (
#         (1, 'SHS'),
#         (2, 'RegularClass'),
#         (3, 'NightCLass'),
#     )
#     fee_choices = (
#         (True, 'PAID'),
#         (False, 'UNPAID'),
#     )
#     stud_choices = (
#         (True, 'ENROLLED'),
#         (False, 'DROP'),
#     )
#     student_type = models.BooleanField(choices=student_choices)
#     tuition_percentage = models.SmallIntegerField(null=True)
#     misc_fee_status = models.BooleanField(choices=fee_choices,)
#     reg_fee_status = models.BooleanField(choices=fee_choices,)
#     stud_fee_status = models.BooleanField(choices=stud_choices,)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)

#     @property
#     def __str__(self):
#         return self.student_type

#     def created_on_arrow(self):
#         return arrow.get(self.date_created).humanize()

#     def updated_on_arrow(self):
#         return arrow.get(self.date_updated).humanize()

#     def date_created_recently(self):
#         now = timezone.now()
#         return now - datetime.timedelta(days=1) <= self.date_created <= now

#     class Meta:
#         verbose_name_plural = 'Commision Details'
#         ordering = ['-date_created']
