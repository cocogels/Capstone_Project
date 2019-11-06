from django.db import models
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from accounts.models import User
import datetime
import arrow

from accounts.models import User




# class ActivityCalendar(models.Model): 
#     activity_id = models.AutoField(primary_key=True)
#     activity_name = models.CharField(max_length=100)
#     start_date = models.DateTimeField(null=True, blank=True)
#     end_date = models.DateTimeField(null=True, blank=True)
    
    
#     #created_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     date_created = models.DateField(_('Date Created'),auto_now_add=True)
#     revised = models.BooleanField(default=False)
#     rejected = models.BooleanField(default=False)
    
#     def __str__(self):
#         return self.activity_name
    
#     def created_on_arrow(self):
#         return arrow.get(self.date_created).humanize()
    
#     class Meta:
#         verbose_name = _('Activity Request')
#         verbose_name_plural = _('Activity Requests')
