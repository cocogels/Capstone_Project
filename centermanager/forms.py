from django import forms
import datetime
from .models import TargetSheet, PaymentDetails, SanctionSetting, CommissionSetting, SchoolYear
import pytz
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus import YearPickerInput
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from .serializers import SchoolYearSerializer
from accounts.models import UserMarketingProfile

"""  TargetSheet Validation Form """


def current_year():
    return datetime.date.today().year

def year_choices():
    return[(r, r) for r in range(2017, datetime.date.today().year+4)]


def present_or_future_date(value):
    if value < datetime.date.today():
        raise forms.ValidationError("The date cannot be in the past!")
    return value


class SchoolYearForm(forms.ModelForm):
    class Meta:
        model  = SchoolYear
        fields = [
            'start_year',
            'end_year'
        ]
        
        widgets = {
            'start_year': YearPickerInput(format='%Y').start_of('school year'),
            'end_year': YearPickerInput(format='%Y').end_of('school year'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_year'].label = "Start Year"
        self.fields['end_year'].label = "End Year"
        self.fields['start_year'].required = True
        self.fields['end_year'].required = True

    def clean(self):
        cleaned_data = super(SchoolYearForm, self).clean()
        start_year   = cleaned_data.get("start_year")
        end_year     = cleaned_data.get("end_year")
        
        if start_year and end_year: 
            if start_year > end_year:
                    raise forms.ValidationError('Please Enter A Valid Date')
                
            if start_year < datetime.date.today():
                raise forms.ValidationError('The Date Cannot be in the Past')
            
            if end_year < datetime.date.today():
                raise forms.ValidationError('The Date Cannot be in the Past')
        
    
    
    
class TargetSheetForm(forms.ModelForm):
  
    corporate           = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Amount'}), label='Corporate', required=False,)
    retail              = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Amount'}), label='Retail', required=False, )
    owwa                = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Amount'}), label='OWWA', required=False, )
    seniorhigh          = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Student'}), label='Senior High', required=False, )
    higher_ed           = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Student'}), label='Higher Education', required=False, )
   
    class Meta:
        model = TargetSheet
        fields = ( 
           'corporate',
           'retail',
           'owwa',
           'seniorhigh',
           'higher_ed',
       )
    

   
   
class PaymentDetailsForm(forms.ModelForm):
    

    cash_amount_per_unit     = forms.CharField(label='Cash Amount Per Unit', widget=forms.NumberInput(),)
    cash_miscellaneous_fee   = forms.CharField(label='Cash Miscellaneous Fee', widget=forms.NumberInput(),)
    cash_lab_fee             = forms.CharField(label='Cash Laboratory Fee', widget=forms.NumberInput(),)
    cash_registration_fee    = forms.CharField(label='Cash Registration Fee', widget=forms.NumberInput(),)
    ins_amount_unit          = forms.CharField(label='Installment Amount Per Unit', widget=forms.NumberInput(),)
    ins_miscellaneous_fee    = forms.CharField(label='Installment Miscellaneous Fee', widget=forms.NumberInput(),)
    ins_lab_fee              = forms.CharField(label='Installment Laboratory Fee', widget=forms.NumberInput(),)

    
    class Meta:
        model   = PaymentDetails
        fields  = (
            'cash_amount_per_unit',
            'cash_miscellaneous_fee',
            'cash_lab_fee',
            'cash_registration_fee',
            'ins_amount_unit',
            'ins_miscellaneous_fee',
            'ins_lab_fee'
        )
        

    


class SanctionSettingForm(forms.ModelForm):
    first_sanction      = forms.CharField(label='First Sanction')
    second_sanction     = forms.CharField(label='Second Sanction')
    third_sanction      = forms.CharField(label='Third Sanction')
    fourth_sanction     = forms.CharField(label='Fourth Sanction')
    fifth_sanction      = forms.CharField(label='Fifth Sanction')

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
        if instance and instance.pk:
            self.fields['first_sanction'].widget.attrs['readonly']  = True
            self.fields['second_sanction'].widget.attrs['readonly'] = True
            self.fields['third_sanction'].widget.attrs['readonly']  = True
            self.fields['fourth_sanction'].widget.attrs['readonly'] = True
            self.fields['fifth_sanction'].widget.attrs['readonly']  = True

class CommissionSettingForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(),max_length=255, label='Title')
    class Meta:
        model = CommissionSetting
        fields = {  
            'title',
            'tuition_percentage',
            'misc_fee_status',
            'reg_fee_status',
            'stud_fee_status',
        }
        
        labels = {

            'tuition_percentage': 'Tuition Percentage',
            'misc_fee_status': 'Miscellaneous Fee Status',
            'reg_fee_status': 'Registration Fee Status',
            'stud_fee_status': 'Student Fee Status',
        }
    def clean_title(self, *args, **kwargs):
        
        title = self.cleaned_data.get('title')
        qs   = TargetSheet.objects.filter(atitle=title)
        if qs.exists():
            raise forms.ValidationError('This Title Has Already Been used')
        return title
    

class AddEmployeeForm(forms.ModelForm):

    email = forms.EmailField()
    password = forms.CharField(
        max_length=50, label='Password', widget=forms.PasswordInput())
    is_budgetary = forms.BooleanField(required=False, label='BUDGETARY')
    is_ihe = forms.BooleanField(required=False, label='IHE')
    is_shs = forms.BooleanField(required=False, label='SHS')
    is_icl = forms.BooleanField(required=False, label='ICL')
    is_marketinghead = forms.BooleanField(required=False, label='Marketing Head')
    is_centerbusinessmanager = forms.BooleanField(required=False, label='Center Business Manager')
    
    class Meta:
        model = UserMarketingProfile
        fields = (
            'email',
        )

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        query_set = UserMarketingProfile.objects.filter(email__iexact=email)
        if query_set.exists():
            raise forms.ValidationError('This email Already Registered..!!')
        return email

    def save(self, commit=True):
        #This would save the provided password in hashed format
        user = super(AddEmployeeForm, self).save(commit=False)
        user = UserMarketingProfile(
            email=self.cleaned_data['email'],
            is_budgetary=self.cleaned_data['is_budgetary'],
            is_ihe=self.cleaned_data['is_ihe'],
            is_shs=self.cleaned_data['is_shs'],
            is_icl=self.cleaned_data['is_icl'],
            is_marketinghead=self.cleaned_data['is_marketinghead'],
            is_centerbusinessmanager=self.cleaned_data['is_centerbusinessmanager'],
        )
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
