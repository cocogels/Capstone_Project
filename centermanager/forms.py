import datetime
from datetime import date, timedelta
import pytz
from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q
from accounts.models import User
from centermanager.models import (
    CommissionSetting, Matriculation, MatriculationCourseCategory,
    MatriculationStatusCategory, SanctionSetting, TargetSheet, SchoolYear)

from django.views.generic.dates import YearMixin


class EmployeeRegistrationForm(forms.ModelForm):
    
    email                       = forms.EmailField()
    password                    = forms.CharField(max_length=50,label='Password' , widget=forms.PasswordInput())    
    is_marketinghead            = forms.BooleanField(required=False, label='Marketing Head')
    is_centerbusinessmanager    = forms.BooleanField(required=False, label='Center Business Manager')
    is_registrar                = forms.BooleanField(required=False, label='Registrar')  
    first_name                  = forms.CharField(required=False)
    last_name                   = forms.CharField(required=False)
    class Meta:
        model = User
        fields = [
            'email',
        ]

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        queryset = fitler(email__iexact=email)
        if queryset.exists():
            raise forms.ValidationError('This Email Already Registered')
        return email

    def save(self, commit=True):
        user = super(EmployeeRegistrationForm, self).save(commit=False)
        user = UserMarketing(
            email                       = self.cleaned_data['email'],
            first_name                  = self.cleaned_data['first_name'],
            last_name                   = self.cleaned_data['last_name'],
            is_centerbusinessmanager    = self.cleaned_data['is_centerbusinessmanager'],
            is_marketinghead            = self.cleaned_data['is_marketinghead'],
            is_registrar                = self.cleaned_data['is_registrar']
        )
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
    
class SchoolYearForm(forms.ModelForm):
    
    class Meta:
        model = SchoolYear
        fields = [
            'start_year',
            'end_year'
        ]
        widgets = {
            'start_year': DatePickerInput().start_of('school year'),
            'end_year': DatePickerInput().end_of('school year'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_year'].label = "Start Year"
        self.fields['end_year'].label = "End Year"
        self.fields['start_year'].required = True
        self.fields['end_year'].required = True

    def clean(self, *args, **kwargs):
        start_year  = self.cleaned_data.get('start_year')
        end_year    = self.cleaned_data.get('end_year')
        
        year = date.today() + timedelta(days=365)
        _start_year = SchoolYear.objects.filter(start_year__lte=year)
        
        today = datetime.date.today() + timedelta(days=365*1)
        
        if start_year and end_year:
            if start_year >= end_year:
                raise forms.ValidationError('Invalid Date Input')
            
            if start_year < datetime.date.today():
                raise forms.ValidationError('Date Cannot Be on Past Try Again!!')
        
            if end_year < datetime.date.today():
                raise forms.ValidationError('Date Cannot Be on Past Try Again!!')
                
            if end_year >= today:
                raise forms.ValidationError('Cannot Accept Future Dates More Than 1 Year A Head')
            
            if _start_year.exists():
                raise forms.ValidationError('Current Year Already Have A Value!')
            
        return super(SchoolYearForm, self).clean(*args, **kwargs)


class TargetSheetForm(forms.ModelForm):

    corporate = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Amount'}), label='Corporate', required=False,)
    retail = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Amount'}), label='Retail', required=False, )
    owwa = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Amount'}), label='OWWA', required=False, )
    seniorhigh = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Student'}), label='Senior High', required=False, )
    higher_ed = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Student'}), label='Higher Education', required=False, )

    class Meta:
        model = TargetSheet
        fields = [
            'school_year',
            'corporate',
            'retail',
            'owwa',
            'seniorhigh',
            'higher_ed',
            'active_year',
        ]

<<<<<<< HEAD
       
        widgets = {
            'active_year': forms.HiddenInput(),
        }
=======
    #def clean(self):
    #    years = school_year.cleaned_data.get('school_year')
    #    queryset = SchoolYear.objects.filter(start_year__gte=school_year, end_year__lte=school_year)
    #    if queryset.exists():
    #        raise forms.ValidationError('Target Sheet Already Have This Date')
    #    super(TargetSheetForm, self).clean()
             

''' Matriculation Form '''
>>>>>>> 180452339520ca24726b23483e4e66d43307c895

    def clean(self, *args, **kwargs):
        now = date.today() + timedelta(days=365)
        querysets = TargetSheet.objects.filter(date_created__lte=now)
            
        if querysets.exists():
            raise forms.ValidationError('Target Sheet Already Been Set for This Year!!')
        
        return super(TargetSheetForm, self).clean(*args, **kwargs)
        

''' Matriculation Form '''

class MatriculationForm(forms.ModelForm):

    cash_amount_per_unit = forms.CharField(label='Cash Amount Per Unit', widget=forms.NumberInput(),)
    cash_miscellaneous_fee = forms.CharField(label='Cash Miscellaneous Fee', widget=forms.NumberInput(),)
    cash_lab_fee = forms.CharField(label='Cash Laboratory Fee', widget=forms.NumberInput(),)
    cash_registration_fee = forms.CharField(label='Cash Registration Fee', widget=forms.NumberInput(),)
    ins_amount_unit = forms.CharField(label='Installment Amount Per Unit', widget=forms.NumberInput(),)
    ins_miscellaneous_fee = forms.CharField(label='Installment Miscellaneous Fee', widget=forms.NumberInput(),)
    ins_lab_fee = forms.CharField(label='Installment Laboratory Fee', widget=forms.NumberInput(),)

    class Meta:
        model = Matriculation
        fields = (
            'status',
            'course',
            'cash_amount_per_unit',
            'cash_miscellaneous_fee',
            'cash_lab_fee',
            'cash_registration_fee',
            'ins_amount_unit',
            'ins_miscellaneous_fee',
            'ins_lab_fee'
        )

        def __init__(self, *args, **kwargs):
            super(MatriculationForm, self).__init__(*args, **kwargs)
            self.fields['status'].label = 'Student Type'
            self.fields['course'].label = 'Course'
            self.fields['cash_amount_per_unit'].label = 'Cash Amount Per Unit'
            self.fields['cash_lab_fee'].label = 'Cash Laboratory Fee'
            self.fields['cash_miscellaneous_fee'].label = 'Cash Miscellaneous Fee'
            self.fields['cash_registration_fee'].label = 'Cash Registration Fee'
            self.fields['ins_amount_unit'].label = 'Installment Amount Per Unit'
            self.fields['ins_miscellaneous_fee'].label = 'Installment Miscellaneous Fee'
            self.fields['ins_lab_fee'].label = 'Installment Laboratory Fee'


class MatriculationStatusCategoryForm(forms.ModelForm):
    class Meta:
        models = MatriculationStatusCategory
        fields = (
            'name',
        )

        def clean_name(self, *args, **kwargs):
            name = self.cleaned_data.get('name')
            qs = MatriculationStatusCategory.objects.filter(name=name)
            if qs.exists():
                raise forms.ValidationError('This Name Has Already Been used')
            return name


class MatriculationCourseCategory(forms.ModelForm):
    class Meta:
        models = MatriculationCourseCategory
        fields = (
            'name',
        )

        def clean_name(self, *args, **kwargs):
            name = self.cleaned_data.get('name')
            qs = MatriculationStatusCategory.objects.filter(name=name)
            if qs.exists():
                raise forms.ValidationError('This Name Has Already Been used')
            return name


''' SANCTION SETTING FORM '''


class SanctionSettingForm(forms.ModelForm):
    class Meta:
        model = SanctionSetting
        fields = (
            'first_sanction',
            'second_sanction',
            'third_sanction',
            'fourth_sanction',
            'fifth_sanction',
        )

    def __init__(self, *args, **kwargs):
        super(SanctionSettingForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['first_sanction'].label = 'First Month Sanction'
        self.fields['second_sanction'].label = 'Second Month Sanction'
        self.fields['third_sanction'].label = 'Third Month Sanction'
        self.fields['fourth_sanction'].label = 'Fourth Month Sanction'
<<<<<<< HEAD
        self.fields['fifth_sanction'].label = 'Fifth Month Sanction'
=======
        self.fields['fifth_sanction'].label = 'Fifth Month'
>>>>>>> 180452339520ca24726b23483e4e66d43307c895

        if instance and instance.pk:
            self.fields['first_sanction'].widget.attrs['readonly'] = True
            self.fields['second_sanction'].widget.attrs['readonly'] = True
            self.fields['third_sanction'].widget.attrs['readonly'] = True
            self.fields['fourth_sanction'].widget.attrs['readonly'] = True
            self.fields['fifth_sanction'].widget.attrs['readonly'] = True


    def clean(self, *args, **kwargs):
        once = date.today() + timedelta(days=365*365)
    
        
        queryset = SanctionSetting.objects.all()
  
         
        if queryset.exists():
            raise forms.ValidationError('You Can Only Create Once ')
        
        return super(SanctionSettingForm, self).clean(*args, **kwargs)
''' Commission Setting Form '''

class CommissionSettingForm(forms.ModelForm):
    
    class Meta:
        model = CommissionSetting
        fields = {
            'student_type',
            'tuition_percentage',
            'misc_fee_status',
            'reg_fee_status',
            'stud_fee_status',
        }

    def __init__(self, *args, **kwargs):
        super(CommissionSettingForm, self).__init__(*args, **kwargs)
        self.fields['student_type'].label = 'Student Type'
        self.fields['tuition_percentage'].label = 'Tuition Percentage'
        self.fields['misc_fee_status'].label = 'Miscellaneuos Fee Status'
        self.fields['reg_fee_status'].label = 'Regular Fee Status'
        self.fields['stud_fee_status'].label = 'Student Fee Status'
