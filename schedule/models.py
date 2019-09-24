# from django.db import models
# from django.contrib import messages
# from django.conf import settings
# from django.core.urlresolvers import reverse
# from django.core.exceptions import ValidationError
# from components.models import SchoolYear

# import datetime
# import arrow



# class MarkingPeriod(models.Model):
#     name        = models.CharField(max_length=255)
#     start_date  = models.DateField(validators=settings.DATE_VALIDATORS)
#     end_date    = models.DateField(validators=settings.DATE_VALIDATORS)
#     school_year = models.ForegnKey(SchoolYear, on_delete=models.SET_NULL, null=True)
#     active      = models.BooleanField(default=False, help_text='Marketing Head May Only Assign Quota For Active Marking Periods.')
#     school_days = models.IntegerField(blank=True, null=True, help_text='If Set, This will be the number of days school in session.If unset, the value is calculated by the days off.')
#     monday      = models.BooleanField(default=True)
#     tuesday     = models.BooleanField(default=True)
#     wednesday   = models.BooleanField(default=True)
#     thursday    = models.BooleanField(default=True)
#     friday      = models.BooleanField(default=True)
#     saturday    = models.BooleanField(default=True)
#     sunday      = models.BooleanField(default=True)
    
#     class Meta:
#         ordering = ['-start_date',]
        
#     def __unicode__(self):
#         return unicode(self.name)

#     def clean(self):
#         # Don't allow draft entries to have a pub_date.
#         if self.start_date > self.end_date:
#             raise ValidationError('Cannot end before starting!')
        
  