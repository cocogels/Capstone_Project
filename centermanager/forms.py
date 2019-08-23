from django import forms
from .models import TargetSheet, PaymentDetails, SanctionSetting, CommissionSetting
import pytz

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class DateInput(forms.DateInput):
    input_type = 'date'


""" TargetSheet Validation Form"""

class TargetSheetForm(forms.Form):
    start_date          = forms.DateTimeField()
    end_date            = forms.DateField(widget=forms.DateInput, required=True)
    corporate           = forms.CharField(widget=forms.NumberInput(), label='Corporate', required=False)
    retail              = forms.CharField(widget=forms.NumberInput(), label='Retail', required=False, )
    owwa                = forms.CharField(widget=forms.NumberInput(), label='OWWA', required=False, )
    seniorhigh          = forms.CharField(widget=forms.NumberInput(), label='Senior High', required=False, )
    higher_ed           = forms.CharField(widget=forms.NumberInput(), label='Higher Education', required=False, )
   
   
   
   
   
   
class PaymentDetailsForm(forms.Form):
    
    cash_amount_per_unit     = forms.CharField(label='Cash Amount Per Unit', widget=forms.NumberInput(),)
    cash_miscellaneous_fee   = forms.CharField(label='Cash Miscellaneous Fee', widget=forms.NumberInput(),)
    cash_lab_fee             = forms.CharField(label='Cash Laboratory Fee', widget=forms.NumberInput(),)
    cash_registration_fee    = forms.CharField(label='Cash Registration Fee', widget=forms.NumberInput(),)
    ins_amount_unit          = forms.CharField(label='Installment Amount Per Unit', widget=forms.NumberInput(),)
    ins_miscellaneous_fee    = forms.CharField(label='Installment Miscellaneous Fee', widget=forms.NumberInput(),)
    ins_lab_fee              = forms.CharField(label='Installment Laboratory Fee', widget=forms.NumberInput(),)



class SanctionSettingForm(forms.Form):
    first_sanction      = forms.CharField(label='First Sanction',max_length=255,)
    second_sanction     = forms.CharField(label='Second Sanction',max_length=255,)
    third_sanction      = forms.CharField(label='Third Sanction',max_length=255,)
    fourth_sanction     = forms.CharField(label='Fourth Sanction',max_length=255,)
    fifth_sanction      = forms.CharField(label='Fifth Sanction',max_length=255,)
    


class CommissionSettingForm(forms.ModelForm):
    class Meta:
        model = CommissionSetting
        fields = {
            'tuition_percentage',
            'misc_fee_status',
            'reg_fee_status',
            'stud_fee_status',
        }
