
from rest_framework.validators import UniqueForYearValidator

from .models import SchoolYear



class SchoolYearSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= SchoolYear
        fields = [
            'start_year',
            'end_year',
        ]
        
        
        
    def validate(self, data):
        
        if data['start_year'] < data['end_year']:
            raise serializers.ValidationError('Start Year Cannot be Greater than end Year Try Again..!')
        
        
        if data['start_year'] < datetime.date.today().year:
            raise serializers.ValidationError('Start Year Cannot be on Past')


        if data['end_year'] > datetime.date.today().year+5:
            raise serializers.ValidationError('End Year Canoot Exceed Five Years')
        return data
        
