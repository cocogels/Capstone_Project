from centermanager.models import SchoolYear

from django import forms






class YearSelectForm(forms.Form):
    school_year = forms.ModelChoiceField(queryset=SchoolYear.objects.all())