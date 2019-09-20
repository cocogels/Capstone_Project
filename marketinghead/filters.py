import django_filters
from .models import AssignQuota



class AssignQuotaFilters(django_filters.FilterSet):
    class Meta:
        model = AssignQuota
        fields={
            'user_profile',
        }
