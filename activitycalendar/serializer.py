from rest_framework import serializers
from activitycalendar.models import ActivityCalendar



class ActivityCalendarSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ActivityCalendar
        fields = [
            'activity_name',
            'start_date',
            'end_date',
            'created_by',
            'approved',
            'revised',
            'rejected',
        ]