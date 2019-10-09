from django import forms
import pytz
import datetime
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus import YearPickerInput
from accounts.models import User
from django.utils import timezone
from centermanager.models import SchoolYearModel, TargetSheet, MatriculationStatusCategory, MatriculationCourseCategory, Matriculation, SanctionSetting, CommissionSetting


''' School Year Form '''


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
            'is_marketinghead',
            'is_centerbusinessmanager',
            'is_registrar',
        ]

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        queryset = User.objects.fitler(email__iexact=email)
        if queryset.exists():
            raise forms.ValidationError('This Email Already Registered')
        return email

    def save(self, commit=True):
        user = super(EmployeeRegistrationForm, self).save(commit=False)
        user = User(
            email                       = self.cleaned_data['email'],
            first_name                  = self.cleaned_data['first_name'],
            last_name                   = self.cleaned_data['last_name'],
            is_centerbusinessmanager    = self.cleaned_data['is_centerbusinessmanager'],
            is_marketinghead            = self.cleaned_data['is_marketinghead'],
            is_registrar                = self.cleaned_data['is_register']
        )
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
    

class SchoolYearForm(forms.ModelForm):
    class Meta:
        model = SchoolYearModel
        fields = [
            'start_year',
            'end_year',
        ]

        widgets = {
            'start_year': YearPickerInput().start_of('school year'),
            'end_year': YearPickerInput().end_of('school year'),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_year'].label = "Start Year"
        self.fields['end_year'].label = "End Year"
        self.fields['start_year'].required = True
        self.fields['end_year'].required = True

    def clean_start_year(self):
        return int(self.cleaned_data['start_year'])
    
    def clean_end_year(self):
        return int(self.cleaned_data['end_year'])

''' Target Sheet Form '''


class TargetSheetForm(forms.ModelForm):

    corporate = forms.CharField(widget=forms.NumberInput(
        attrs={'placeholder': 'Amount'}), label='Corporate', required=False,)
    retail = forms.CharField(widget=forms.NumberInput(
        attrs={'placeholder': 'Amount'}), label='Retail', required=False, )
    owwa = forms.CharField(widget=forms.NumberInput(
        attrs={'placeholder': 'Amount'}), label='OWWA', required=False, )
    seniorhigh = forms.CharField(widget=forms.NumberInput(
        attrs={'placeholder': 'Student'}), label='Senior High', required=False, )
    higher_ed = forms.CharField(widget=forms.NumberInput(
        attrs={'placeholder': 'Student'}), label='Higher Education', required=False, )

    class Meta:
        model = TargetSheet
        fields = [
            'corporate',
            'retail',
            'school_year',
            'owwa',
            'seniorhigh',
            'higher_ed',
        ]

    def clean(self):
        years = school_year.cleaned_data.get('school_year')
        queryset = SchoolYear.objects.filter(start_year__gte=school_year, end_year__lte=school_year)
        if queryset.exists():
            raise forms.ValidationError('Target Sheet Already Have This Date')
        super(TargetSheetForm, self).clean()
             

''' Matriculation Form '''



class MatriculationForm(forms.ModelForm):

    cash_amount_per_unit = forms.CharField(
        label='Cash Amount Per Unit', widget=forms.NumberInput(),)
    cash_miscellaneous_fee = forms.CharField(
        label='Cash Miscellaneous Fee', widget=forms.NumberInput(),)
    cash_lab_fee = forms.CharField(
        label='Cash Laboratory Fee', widget=forms.NumberInput(),)
    cash_registration_fee = forms.CharField(
        label='Cash Registration Fee', widget=forms.NumberInput(),)
    ins_amount_unit = forms.CharField(
        label='Installment Amount Per Unit', widget=forms.NumberInput(),)
    ins_miscellaneous_fee = forms.CharField(
        label='Installment Miscellaneous Fee', widget=forms.NumberInput(),)
    ins_lab_fee = forms.CharField(
        label='Installment Laboratory Fee', widget=forms.NumberInput(),)

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
    first_sanction = forms.CharField(label='First Sanction')
    second_sanction = forms.CharField(label='Second Sanction')
    third_sanction = forms.CharField(label='Third Sanction')
    fourth_sanction = forms.CharField(label='Fourth Sanction')
    fifth_sanction = forms.CharField(label='Fifth Sanction')

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
        self.fields['second_sanction'].label = 'First Month Sanction'
        self.fields['third_sanction'].label = 'First Month Sanction'
        self.fields['fourth_sanction'].label = 'First Month Sanction'
        self.fields['fifth_sanction'].label = 'Student Type'

        if instance and instance.pk:
            self.fields['first_sanction'].widget.attrs['readonly'] = True
            self.fields['second_sanction'].widget.attrs['readonly'] = True
            self.fields['third_sanction'].widget.attrs['readonly'] = True
            self.fields['fourth_sanction'].widget.attrs['readonly'] = True
            self.fields['fifth_sanction'].widget.attrs['readonly'] = True


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
