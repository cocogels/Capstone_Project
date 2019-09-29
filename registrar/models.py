from django.db import models
import arrow
from datetime import date
from django.utils.translation import ugettext_lazy as _
    

class RequirementsCategory(models.Model):
    name = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Requirements Category'
        verbose_name_plural = 'Requirements Categories'

    def __str__(self):
        return self.name

class RequirementsModel(models.Model):
    
    req_id              = models.AutoField(primary_key=True)
    category            = models.ForeignKey(RequirementsCategory, on_delete=models.CASCADE, null=True)
    requirements_name   = models.CharField(max_length=255, null=True)
    date_created        = models.DateField(_("Date Created"),auto_now_add=True)
    date_updated        = models.DateField(_("Date Update"),auto_now=True)

    def __str__(self):
        return self.category
    
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
        verbose_name_plural = 'Requirements'
        



class AvailableCourseCategory(models.Model):
    name = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Course Category'
        verbose_name_plural = 'Course Categories'

    def __str__(self):
        return self.name

class AvailableCourseModel(models.Model):
    
    ac_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(AvailableCourseCategory, on_delete=models.CASCADE, null=True)
    number_unit = models.SmallIntegerField(null=True)
    date_created = models.DateField(_("Date Created"),auto_now_add=True)
    date_updated = models.DateField(_("Date Updated"),auto_now=True)
    
    def __str__(self):
        return self.course_name
    
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
        verbose_name_plural = 'Available Course'
