from activity.models import Activity

from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    )


''' User Activity Request '''
class CreateActivitySerializer(ModelSerializer):
    
    class Meta:
        model = Activity
        fields = [       
            'start_date',
            'end_date',
            'activity_name',
            'location',
            'description',
            'status',
            #budget
            #collateral
        ] 
        read_only_fields = ['status',]

 
        
class ListActivitySerializer(ModelSerializer):

    user = SerializerMethodField()
    class Meta:
        model = Activity
        fields = [
            'user',        
            'start_date',
            'end_date',
            'activity_name',
            'location',
            'description',
            'status',
            #budget
            #collateral
        ]
        read_only_fields = fields
    
    def get_user(self, object):
        return "{}".format(object.user.email)

class DetailActivitySerializer(ModelSerializer):
    user = SerializerMethodField()
    class Meta:
        model = Activity
        fields = [
            'user',        
            'start_date',
            'end_date',
            'activity_name',
            'location',
            'description',
            #budget
            #collateral
        ]
        read_only_fields = fields

    
    def get_user(self, object):
            return "{}".format(object.user.email)
        
class UpdateActivitySerializer(ModelSerializer):
    
    class Meta:
        model = Activity    
        fields = [      
            'start_date',
            'end_date',
            'activity_name',
            'location',
            'description',
            'status',
            #budget
            #collateral
        ]
        read_only_fields = ['status']



''' Changing Status Serialziation  '''

class PendingActivitySerialization(ModelSerializer):
    
    class Meta:
        model = Activity    
        fields = [      
            'start_date',
            'end_date',
            'activity_name',
            'location',
            'description',
            #budget
            #collateral
        ]
        