from django.shortcuts import render, redirect, get_object_or_404
from django.forms import forms
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView 
from django.http import HttpResponseRedirect, Http404
from .forms import TargetSheetForm, PaymentDetailsForm, SanctionSettingForm, CommissionSettingForm, SchoolYearForm
from .models import TargetSheet, PaymentDetails, SanctionSetting, CommissionSetting, SchoolYear
from django.views.generic.dates import YearArchiveView
# Create your views here.




""" SCHOOL YEAR """


def create_school_year(request):

    if request.method == 'POST':
        form = SchoolYearForm(request.POST or None)
        if form.is_valid():
            
            start_year = form.cleaned_data['start_year']
            end_year   = form.cleaned_data['end_year']
            
            form = SchoolYear(
                start_year=start_year,
                end_year=end_year,
            )
            
            form.save()
            messages.success(request, 'You Have Successfully Set School Year')
            return redirect('centermanager:target_list')
    else:
        form = SchoolYearForm()  
    template_name = 'school_year/school_year.html'
    context = {
    'form': form,
    'title': "School Year",
    }

    return render(request, template_name, context)

# class SchoolYearArchiveView(YearArchiveView):
#     queryset            = SchoolYear.objects.all()
#     date_field          = 'start_date'
#     date_field          = 'end_date'
#     make_object_list    = True
#     allow_future        = True    
    
""" Target Sheet Details """
def create_target_sheet(request):  
    if request.method == 'POST':
        form = TargetSheetForm(request.POST or None)
        if form.is_valid():


            corporate    = form.cleaned_data['corporate']
            retail       = form.cleaned_data['retail']
            owwa         = form.cleaned_data['owwa']
            seniorhigh   = form.cleaned_data['seniorhigh']
            higher_ed    = form.cleaned_data['higher_ed']
            
            form = TargetSheet(

                                title=title,
                                start_date=start_date,
                                end_date=end_date,
                                corporate=corporate,
                                retail=retail,
                                owwa=owwa ,
                                seniorhigh=seniorhigh, 
                                higher_ed=higher_ed,
                                
                                )           
            
            form.save()
            messages.success(request, 'You Have Successfully Set New Target for Year')
            return redirect('centermanager:target_list')
    else:
        form = TargetSheetForm()  
    template_name = 'target_sheet/targetsheet_list.html'
    context = {
    'title': "Set New Target Details",

    }

    return render(request, template_name, context)


'''   Creating List of TargetSheet Added in Data Base  '''
class TargetListView(ListView):
    model = TargetSheet
    template_name = 'target_sheet/targetsheet_list.html'
    queryset = TargetSheet.objects.all()

    


''' Creating Target Detail View '''

class TargetDetailView(DetailView):
    model = TargetSheet
    template_name = 'target_sheet/target_details.html'

    

  
# def target_sheet_detail_view(request, target_slug):
#     obj = get_object_or_404(TargetSheet, target_slug=target_slug)
#     template_name = 'target_sheet/target_details.html'
#     context = {'object': obj }
    
#     return render(request, template_name, context)


''' Updating Target Details '''

class TargetUpdateView(UpdateView):
    model           = TargetSheet
    form_class      = TargetSheetForm
    template_name   = 'target_sheet/create_target._details.html'
    success_url     = reverse_lazy('centermanager:target_list')
  

    
    def form_valid(self, form):
        form.save()
        message_text = 'Your {} was Updated Successfully!'.format(form.instance)
        messages.success(self.request, message_text)
        if 'continue' in self.request.POST:
            return HttpResponseRedirect(
                reverse_lazy('centermanager:target_update',
                             kwargs={'pk': form.instance.pk}))
        else:
            return super().form_valid(form)
# def target_sheet_update_view(request, slug):
#     obj = get_object_or_404(TargetSheet, slug=slug)
#     form = TargetSheetForm(request.POST or None, instance=obj)
#     if form.is_valid():
#         form.save()
#     template_name =  'target_sheet/create_target._details.html'
#     context = {
#         'title': "Update Target Details",
#         "form": form
#     }
#     return render(request, template_name, context)




'''Payment Details '''
def create_payment(request):
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
                                ins_miscellaneous_fee=ins_miscellaneous_fee,
                                ins_lab_fee=ins_lab_fee,
            
                                )
        
        create.save()
        messages.success(request, 'You Have Successfully Added Payment Details')
        return redirect('centermanager:payment_list')
    else:
        form = PaymentDetailsForm()
    template_name = 'payment/create_payment.html'
    context = {
        'form': form
    }
        
    return render(request, template_name, context)



class PaymentListView(ListView):
    model           = PaymentDetails
    template_name   = 'payment/payment_list.html'
    queryset        = PaymentDetails.objects.all()



class PaymentDetailView(DetailView):
    model           = PaymentDetails
    template_name   ='payment/payment_details.html'
    

class PaymentUpdateView(UpdateView):
    model = PaymentDetails
    form_class = PaymentDetailsForm
    template_name = 'payment/create_payment.html'
    success_url = reverse_lazy('centermanager:payment_list')

    def form_valid(self, form):
        form.save()
        message_text = 'Your {} was Updated Successfully!'.format(
            form.instance)
        messages.success(self.request, message_text)
        if 'continue' in self.request.POST:
            return HttpResponseRedirect(
                reverse_lazy('centermanager:payment_update',
                             kwargs={'pk': form.instance.pk}))
        else:
            return super().form_valid(form)
        



'''  SANCTION SETTING '''
def create_sanction_setting(request):
    
    if request.method == 'POST':
        form = SanctionSettingForm(request.POST)
        
        if form.is_valid():
            first_sanction  = form.cleaned_data['first_sanction']
            second_sanction = form.cleaned_data['second_sanction']
            third_sanction  = form.cleaned_data['third_sanction']
            fourth_sanction = form.cleaned_data['fourth_sanction']
            fifth_sanction  = form.cleaned_data['fifth_sanction']

        create = SanctionSetting(
            first_sanction=first_sanction,
            second_sanction=second_sanction,
            third_sanction=third_sanction,
            fourth_sanction=fourth_sanction,
            fifth_sanction=fifth_sanction,
        )
        
        create.save()
        messages.success(request, 'You Have Successfully Added Sanction Details.!')
        return redirect('centermanager:sanction_list')
    
    else:
        form = SanctionSettingForm()
    template_name='sanction_setting/create_sanction.html'
    context = {
        'form': form
    }
    
    return render(request, template_name, context)


class SanctionListView(ListView):
    modal = SanctionSetting
    template_name = 'sanction_setting/sanction_list.html'
    queryset = SanctionSetting.objects.all()

class SanctionDetailView(DetailView):
    modal = SanctionSetting
    template_name = 'sanction_setting/sanction_detail.html'

class SanctionUpdateView(UpdateView):
    model = SanctionSetting
    form_class = SanctionSettingForm
    template_name = 'sanction_setting/create_sanction.html'
    success_url = reverse_lazy('centermanager:sanction_list')

    def form_valid(self, form):
        form.save()
        message_text = 'Your {} was Updated Successfully!'.format(form.instance)
        messages.success(self.request, message_text)
        if 'continue' in self.request.POST:
            return HttpResponseRedirect(
                reverse_lazy('centermanager:sanction_update',
                             kwargs={'pk': form.instance.pk}))
        else:
            return super().form_valid(form)
        
  
  
''' Comission Create View '''        
def create_commission_setting(request):
    
    if request.method == 'POST':
        form = CommissionSettingForm(request.POST)
        
        if form.is_valid():
            
            title              = form.cleaned_data['title']
            tuition_percentage = form.cleaned_data['tuition_percentage']
            misc_fee_status    = form.cleaned_data['misc_fee_status']
            reg_fee_status     = form.cleaned_data['reg_fee_status']
            stud_fee_status    = form.cleaned_data['stud_fee_status']
        
        create = CommissionSetting(
            
            title=title,
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
    template_name = 'com_setting/create_commission.html'
    context = {
        'form':form
    }
    
    return render(request, template_name, context)

class CommissionListView(ListView):
    model = CommissionSetting
    template_name = 'com_setting/commission_list.html'
    queryset = CommissionSetting.objects.all()

class CommissionDetailView(DetailView):
    model = CommissionSetting
    template_name = 'com_setting/commission_detail.html'



class CommissionUpdateView(UpdateView):
    model = CommissionSetting
    template_name='com_setting/create_commission.html'
    form_class = CommissionSettingForm
    success_url = reverse_lazy('centermanager:commission_list')

    def form_valid(self, form):
        form.save()
        messages_text = 'Your {} was Updated Successfully!'.format(form.instance)
        messages.success(self.request, messages_text)
        if 'continue' in self.request.POST:
            return HttpResponseRedirect(
               reverse_lazy( 'centermanager:commission_update',
                kwargs={'pk': form.instance.pk})
            )
        else:
            return super().form_valid(form)
