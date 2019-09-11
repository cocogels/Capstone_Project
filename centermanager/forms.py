from django import forms
import datetime
from .models import TargetSheet, PaymentDetails, SanctionSetting, CommissionSetting, SchoolYear
import pytz
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus import YearPickerInput
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin




"""  TargetSheet Validation Form """


def current_year():
    return datetime.date.today().year

def year_choices():
    return[(r, r) for r in range(2017, datetime.date.today().year+4)]

class SchoolYearForm(forms.ModelForm):
    
   
    class Meta:
        model = SchoolYear
        fields = (
            'start_year',
            'end_year',
        )
        widgets = {
            'start_year': YearPickerInput(format='%Y').start_of('school year'),
            'end_year': YearPickerInput(format='%Y').end_of('school year'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_year'].label = "Start Year"
        self.fields['end_year'].label = "End Year"
        self.fields['start_year'].required= True
        self.fields['end_year'].required= True
        
    
    # def clean(self):
    #     cleaned_data = super(SchoolYearForm, self).clean()
    #     start_year = self.cleaned_data.get('start_year')
    #     end_year   = self.cleaned_data.get('end_year')
        
        
    #     if start_year and end_year:
    #         start_year = datetime.strpdate(start_year, '%Y-%m-%d')
    #         end_year = datetime.strpdate(end_year, '%Y-%m-%d')
            
            
    #         if start_year < end_year:
    #             raise forms.ValidationError('Start Year Cannot Be Greater than End Year Try Again..!')
            
    #         if  datetime.date.today().year < start_year:
    #             raise forms.ValidationError('Start Year Cannot be on Past')

    
    #         if  datetime.date.today().year+5 < end_year:
    #             raise forms.ValidationError('Year Cannot More Than This.. Try Again.!')     
        
    #     return cleaned_data
    
    
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
    first_sanction      = forms.CharField(label='First Sanction',max_length=255,)
    second_sanction     = forms.CharField(label='Second Sanction',max_length=255,)
    third_sanction      = forms.CharField(label='Third Sanction',max_length=255,)
    fourth_sanction     = forms.CharField(label='Fourth Sanction',max_length=255,)
    fifth_sanction      = forms.CharField(label='Fifth Sanction',max_length=255,)

    class Meta:
        model = SanctionSetting
        fields = (
            'first_sanction',
            'second_sanction',
            'third_sanction',
            'fourth_sanction',
            'fifth_sanction',
        )
    

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
    
