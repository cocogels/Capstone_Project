import django_filters

from centermanager.models import TargetSheet,SchoolYear
from django.db.models import Q
from datetime import date


class SchoolYearFilter(django_filters.FilterSet):
    
    now=date.today()
    school_year = django_filters.ModelChoiceFilter(queryset=SchoolYear.objects.all())
    
    class Meta:
        model = SchoolYear
        fields = [
            'start_year',
            'end_year',
        ]