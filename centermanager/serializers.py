import datetime
from datetime import date, timedelta
from rest_framework.validators import UniqueForYearValidator
from django.db.models import Q
from rest_framework import serializers
from bootstrap_datepicker_plus import YearPickerInput
from .models import SchoolYear
from django.utils.translation import gettext as _



def present_or_future_date(value):
    if value < datetime.date.today():
        raise serializers.ValidationError("The date cannot be in the past!")
    return value

class SchoolYearSerializer(serializers.ModelSerializer):
    start_year = serializers.DateField(validators=[present_or_future_date])
    end_year    = serializers.DateField(validators=[present_or_future_date])


    class Meta:
        model= SchoolYear
        fields = [
            'start_year',
            'end_year',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_year'].label = "Start Year"
        self.fields['end_year'].label = "End Year"
        self.fields['start_year'].required= True
        self.fields['end_year'].required= True
    
        
    def validate(self, data):
        if data['start_year'] and data['end_year']:
            if data['start_year'] > data['end_year']:
                raise serializers.ValidationError('Please Enter A Valid Date')
        return data
        
