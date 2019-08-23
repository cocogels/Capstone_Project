from django.shortcuts import render, redirect, get_object_or_404
from django.forms import forms
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import TargetSheetForm, PaymentDetailsForm, SanctionSettingForm, CommissionSettingForm


from .models import TargetSheet, PaymentDetails, SanctionSetting, CommissionSetting
# Create your views here.

""" Target Sheet Details """


def create_target_sheet(request):  
 
   if request.method == 'POST':
       form = TargetSheetForm(request.POST)
       if form.is_valid():

            
           school_year  = forms.cleaned_data['school_year']
           corporate    = form.cleaned_data['corporate']
           retail       = form.cleaned_data['retail']
           owwa         = form.cleaned_data['owwa']
           seniorhigh   = form.cleaned_data['seniorhigh']
           higher_ed    = form.cleaned_data['higher_ed']
           
           create = TargetSheet(

                            school_year=school_year,
                            corporate=corporate,
                            retail=retail,
                            owwa=owwa ,
                            seniorhigh=seniorhigh, 
                            higher_ed=higher_ed,
                            
                            )           
           
           create.save()
           messages.success(request, 'You Have Successfully Set New Target for Year')
           return redirect('centermanager:target')
   else:
       form = TargetSheetForm()  
       template_name = 'target_sheet/create_target._details.html'
   context = {  
       'form': form
   }
   return render(request, template_name, context)


def list_target_sheet(request):
    context = {}
    targetsheet= TargetSheet.objects.all()
    context['targetsheet'] = targetsheet
    template_name = 'target_sheet/view_target_details.html'
    return render(request, template_name, context)



    
def update_target_sheet(request, ts_id=None):
    
    
    template_name = 'target_sheet/update_target_details.html'
    return render(request, template_name, context)








'''Payment Details '''
def create_payment_details(request):
    if request.method == 'POST':
        form = PaymentDetailsForm(request.POST)
    
        if form.is_valid():

            cash_amount_per_unit    = form.cleaned_data['cash_amount_per_unit']
            cash_miscellaneous_fee  = form.cleaned_data['cash_miscellaneous_fee']
            cash_lab_fee            = form.cleaned_data['cash_lab_fee']
            cash_registration_fee   = form.cleaned_data['cash_registration_fee']
            ins_amount_unit         = form.cleaned_data['ins_amount_unit']
            ins_miscellaneous_fee   = form.cleaned_data['ins_miscellaneous_fee']
            ins_lab_fee             = form.cleaned_data['ins_lab_fee']
             
        create = PaymentDetails(
                                cash_amount_per_unit=cash_amount_per_unit,
                                cash_miscellaneous_fee=cash_miscellaneous_fee,
                                cash_lab_fee=cash_lab_fee,
                                cash_registration_fee=cash_registration_fee,
                                ins_amount_unit=ins_amount_unit,
                                ins_lab_fee=ins_lab_fee,
                                ins_miscellaneous_fee=ins_miscellaneous_fee,
            
                                )
        
        create.save()
        messages.success(request, 'You Have Successfully Added Payment Details')
        return redirect('centermanager:payment')
    else:
        form = PaymentDetailsForm()
    template_name = 'payment_details/payment_details.html'
    context = {
        'form': form
    }
        
    return render(request, template_name, context)
            




'''  SANCTION SETTING '''
def create_sanction_setting(request):
    
    if request.method == 'POST':
        form = SanctionSettingForm(request.POST)
        
        if form.is_valid():
            quota_status = form.cleaned_data['quota_status']
            first_sanction = form.cleaned_data['first_sanction']
            second_sanction = form.cleaned_data['second_sanction']
            third_sanction = form.cleaned_data['third_sanction']
            fourth_sanction = form.cleaned_data['fourth_sanction']
            fifth_sanction = form.cleaned_data['fifth_sanction']

        create = SanctionSetting(
            quota_status=quota_status,
            first_sanction=first_sanction,
            second_sanction=second_sanction,
            third_sanction=third_sanction,
            fourth_sanction=fourth_sanction,
            fifth_sanction=fifth_sanction,
        )
        
        create.save()
        messages.success(request, 'You Have Successfully Added Sanction Details.!')
        return redirect('centermanager:sanction')
    
    else:
        form = SanctionSettingForm()
    template_name='sanction_setting/sanction_setting.html'
    context = {
        'form': form
    }
    
    return render(request, template_name, context)



def create_commission_setting(request):
    
    if request.method == 'POST':
        form = CommissionSettingForm(request.POST)
        
        if form.is_valid():
            
            tuition_percentage = form.cleaned_data['tuition_percentage']
            misc_fee_status    = form.cleaned_data['misc_fee_status']
            reg_fee_status     = form.cleaned_data['reg_fee_status']
            stud_fee_status    = form.cleaned_data['stud_fee_status']
        
        create = CommissionSetting(
            
            tuition_percentage=tuition_percentage,
            misc_fee_status=misc_fee_status,   
            reg_fee_status=reg_fee_status,    
            stud_fee_status=stud_fee_status,
        
        )
        create.save()
        messages.success(request, 'You Have Successfully Added Commission Details..!')
        return redirect('centermanager:commission')
    else:
        form = CommissionSettingForm()
    template_name='com_setting/commission_setting.html'
    context = {
        'form':form
    }
    
    return render(request, template_name, context)
