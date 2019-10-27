from django.db import models
import arrow
from datetime import date
from django.utils.translation import ugettext_lazy as _
    

        
class RequirementsModel(models.Model):
    require_id = models.AutoField(primary_key=True)
    requirements_name = models.CharField(max_length=150)
    date_created = models.DateField(_('Date Created'), auto_now_add=True)
    date_update = models.DateField(_('Date Updated'), auto_now=True)
    
    def __str__(self):
        return self.requirements_name
    
    @property
    def created_on_arrow(self):
         return arrow.get(self.date_created).humanize()
    
    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()

    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now
    
    class Meta:
        verbose_name_plural = 'Requirements'
        ordering = ['-date_created']


class RequirementsTransfereeModel(models.Model):
    require_trans_id = models.AutoField(primary_key=True)
    requirements_name = models.CharField(max_length=150)
    date_created = models.DateField(_('Date Created'), auto_now_add=True)
    date_update = models.DateField(_('Date Updated'), auto_now=True)
    
    def __str__(self):
        return self.requirements_name
    
    @property
    def created_on_arrow(self):
         return arrow.get(self.date_created).humanize()
    
    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()

    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now
    
    class Meta:
        verbose_name_plural = 'Requirements Transferee'
        ordering = ['-date_created']

class CourseModel(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=50)
    course_description = models.CharField(max_length=150)
    date_created = models.DateField(_('Date Created'), auto_now_add=True)
    date_update = models.DateField(_('Date Updated'), auto_now=True)
    
    def __str__(self):
        return self.course_name
    
    @property
    def created_on_arrow(self):
         return arrow.get(self.date_created).humanize()
    
    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()

    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now
    
    class Meta:
        verbose_name_plural = 'Course'
        ordering = ['-date_created']
        
    
  