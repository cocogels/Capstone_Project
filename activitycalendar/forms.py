from activitycalendar.models import ActivityCalendar
from django import forms
from django.forms import ModelForm
from bootstrap_datepicker_plus import DateTimePickerInput



class ActivityCalendarForm(ModelForm):
    
    class Meta:
        model = ActivityCalendar
        fields = [
            'activity_name',
            'start_date',
            'end_date',
        ]
        
        widgets = {
            'start_date': DateTimePickerInput().start_of('activity days'),
            'end_date': DateTimePickerInput().end_of('activity days')
        }

    
