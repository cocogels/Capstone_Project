
import json

from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from centermanager.models import SchoolYear, TargetSheet, MatriculationStatusCategory, MatriculationCourseCategory, Matriculation, SanctionSetting, CommissionStudentType, CommissionSetting
from centermanager.forms import SchoolYearForm, TargetSheetForm, MatriculationForm, SanctionSettingForm, CommissionSettingForm
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, ListView)
from django.urls import reverse
from django.db.models import Q
from django.template.loader import render_to_string
from accounts.models import User

''' School Year Views '''    
class SchoolYearCreateView(CreateView):
    model = SchoolYear
    form_class = SchoolYearForm
    template_name = 'school_year/create_school_year.html'
    success_url = reverse_lazy('centermanager:school_year_list')

    def get_context_data(self, **kwargs):
        context = super(SchoolYearCreateView, self).get_context_data(**kwargs)
        context['school_year_form'] = context['form']
        return context

class SchoolYearListView(ListView):
    model = SchoolYear
    paginated_by = 1
    context_object_name = 'school_year_record'
    template_name = 'school_year/school_year.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['school_year_record'] = context['object_list']
        return context


class SchoolYearDetailView(DetailView):
    model = SchoolYear
    context_object_name = 'school_year_record'
    template__name = 'school_year/school_year_detail.html'
   # paginated_by = 1

    def get_queryset(self):
        queryset = super(SchoolYearDetailView, self).get_queryset()

''' Target Sheet View '''
class TargetSheetCreateView(CreateView):
    model = TargetSheet
    form_class = TargetSheetForm
    template_name = 'target/create_target.html'
    success_url = reverse_lazy('centermanager:add_target')

    def get_context_data(self, **kwargs):
        context = super(TargetSheetCreateView, self).get_context_data(**kwargs)
        context['target_form'] = context['form']
        return context


class TargetSheetListView(ListView):
    model = TargetSheet
    paginated_by = 1
    context_object_name = 'target_sheet_record'
    template_name = 'school_year/school_year_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_sheet_record'] = context['object_list']
        return context


class SchoolYearDetailView(DetailView):
    model = SchoolYear
    context_object_name = 'school_year_record'
    template__name = 'school_year/target.html'
   # paginated_by = 1

    def get_queryset(self):
        queryset = super(SchoolYearDetailView, self).get_queryset()


class TargetUpdateView(UpdateView):
    model = TargetSheet
    form_class = TargetSheetForm
    template_name = 'target_sheet/create_target.html'
    success_url = reverse_lazy('centermanager:target_list')

    def form_valid(self, form):
        form.save()
        message_text = 'Your {} was Updated Successfully!'.format(
            form.instance)
        messages.success(self.request, message_text)
        if 'continue' in self.request.POST:
            return HttpResponseRedirect(
                reverse_lazy('centermanager:update_target',
                             kwargs={'pk': form.instance.pk}))
        else:
            return super().form_valid(form)


def emp_registration(request):
    
    if request.method == 'POST':
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            form  = form.save()
            messages.success(request, 'You Have Successfuly Registered User Account..!!')
            return redirect('centermanager:register-emp')
        else:
            messages.error(request, 'Account Registration Failed Try Again..!!!')
            return redirect('centermanager:register-emp')
    else:
        form = AddEmployeeForm()

    template_name = 'addemployer/create_employee.html'
    context = {
        "form":form,  
    }
    return render(request, template_name, context)
    

class EmployeeListView(ListView):
    model = User
    context_object_name = 'employee_list'
    template_name = 'addemployer/add_cc_list.html'
    queryset = User.objects.all()



# class SchoolYearList(TemplateView):
#     model = SchoolYear
#     template_name = 'school_year/school_year.html'
#     context_object_name = 'school_year_list'
 
#     def get_queryset(self):
#         queryset = self.model.objects.all()
#         if(self.request.user.is_centermanager):

#             request_post = self.request.POST
#             if request_post:
#                 if request_post.get('start_year'):
#                     queryset = queryset.filter(
#                         start_year__icontains=request_post.get('start_year'))

#                 if request_post.get('end_year'):
#                     queryset = queryset.filter(
#                         start_year__icontains=request_post.get('end_year'))
#         return queryset.distinct()

#     def get_context_data(self, **kwargs):
#         context = super(SchoolYearList, self).get_context_data(**kwargs)
#         context['school_year_list'] = self.get_queryset()
#         search = False
#         if(
#             self.request.POST.get('start_year') or
#             self.request.POST.get('end_year')
#         ):
#             search = True
#         context['search'] = search
#         return context

#     def post(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return self.render_to_response(context)





""" Target Sheet Details """
def create_target_sheet(request):
    if request.method == 'POST':
        form = TargetSheetForm(request.POST or None)
        if form.is_valid():

            corporate = form.cleaned_data['corporate']
            retail = form.cleaned_data['retail']
            owwa = form.cleaned_data['owwa']
            seniorhigh = form.cleaned_data['seniorhigh']
            higher_ed = form.cleaned_data['higher_ed']

            form = TargetSheet(
                corporate=corporate,
                retail=retail,
                owwa=owwa,
                seniorhigh=seniorhigh,
                higher_ed=higher_ed,
            )

            form.save()
            messages.success(
                request, 'You Have Successfully Set New Target for Year')
            return redirect('centermanager:target_list')
    else:
        form = TargetSheetForm()
    template_name = 'target_sheet/create_target._details.html'
    context = {
        'form': form,

    }

    return render(request, template_name, context)


'''   Creating List of TargetSheet Added in Data Base  '''


class TargetListView(ListView):
    model = TargetSheet
    context_object_name = 'target_sheet_list'
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
    model = TargetSheet
    form_class = TargetSheetForm
    template_name = 'target_sheet/create_target._details.html'
    success_url = reverse_lazy('centermanager:target_list')

    def form_valid(self, form):
        form.save()
        message_text = 'Your {} was Updated Successfully!'.format(
            form.instance)
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
            status= form.cleaned_data['status']
            course= form.cleaned_data['course']
            cash_amount_per_unit = form.cleaned_data['cash_amount_per_unit']
            cash_miscellaneous_fee = form.cleaned_data['cash_miscellaneous_fee']
            cash_lab_fee = form.cleaned_data['cash_lab_fee']
            cash_registration_fee = form.cleaned_data['cash_registration_fee']
            ins_amount_unit = form.cleaned_data['ins_amount_unit']
            ins_miscellaneous_fee = form.cleaned_data['ins_miscellaneous_fee']
            ins_lab_fee = form.cleaned_data['ins_lab_fee']

        create = PaymentDetails(
            status=status,
            course=course,
            cash_amount_per_unit=cash_amount_per_unit,
            cash_miscellaneous_fee=cash_miscellaneous_fee,
            cash_lab_fee=cash_lab_fee,
            cash_registration_fee=cash_registration_fee,
            ins_amount_unit=ins_amount_unit,
            ins_miscellaneous_fee=ins_miscellaneous_fee,
            ins_lab_fee=ins_lab_fee,

        )

        create.save()
        messages.success(
            request, 'You Have Successfully Added Payment Details')
        return redirect('centermanager:payment_list')
    else:
        form = PaymentDetailsForm()
    template_name = 'payment/create_payment.html'
    context = {
        'form': form
    }

    return render(request, template_name, context)




'''  SANCTION SETTING '''


def create_sanction_setting(request):

    if request.method == 'POST':
        form = SanctionSettingForm(request.POST)

        if form.is_valid():
            first_sanction = form.cleaned_data['first_sanction']
            second_sanction = form.cleaned_data['second_sanction']
            third_sanction = form.cleaned_data['third_sanction']
            fourth_sanction = form.cleaned_data['fourth_sanction']
            fifth_sanction = form.cleaned_data['fifth_sanction']

        create = SanctionSetting(
            first_sanction=first_sanction,
            second_sanction=second_sanction,
            third_sanction=third_sanction,
            fourth_sanction=fourth_sanction,
            fifth_sanction=fifth_sanction,
        )

        create.save()
        messages.success(
            request, 'You Have Successfully Added Sanction Details.!')
        return redirect('centermanager:sanction_list')

    else:
        form = SanctionSettingForm()
    template_name = 'sanction_setting/create_sanction.html'
    context = {
        'form': form
    }

    return render(request, template_name, context)


class SanctionListView(ListView):
    modal = SanctionSetting
    template_name = 'sanction_setting/sanction_list.html'
    context_object_name = 'sanction_list'
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
        message_text = 'Your {} was Updated Successfully!'.format(
            form.instance)
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

            tuition_percentage = form.cleaned_data['tuition_percentage']
            misc_fee_status = form.cleaned_data['misc_fee_status']
            reg_fee_status = form.cleaned_data['reg_fee_status']
            stud_fee_status = form.cleaned_data['stud_fee_status']

        create = CommissionSetting(

            tuition_percentage=tuition_percentage,
            misc_fee_status=misc_fee_status,
            reg_fee_status=reg_fee_status,
            stud_fee_status=stud_fee_status,

        )
        create.save()
        messages.success(
            request, 'You Have Successfully Added Commission Details..!')
        return redirect('centermanager:commission')
    else:
        form = CommissionSettingForm()
    template_name = 'com_setting/create_commission.html'
    context = {
        'form': form
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
    template_name = 'com_setting/create_commission.html'
    form_class = CommissionSettingForm
    success_url = reverse_lazy('centermanager:commission_list')

    def form_valid(self, form):
        form.save()
        messages_text = 'Your {} was Updated Successfully!'.format(
            form.instance)
        messages.success(self.request, messages_text)
        if 'continue' in self.request.POST:
            return HttpResponseRedirect(
                reverse_lazy('centermanager:commission_update',
                             kwargs={'pk': form.instance.pk})
            )
        else:
            return super().form_valid(form)
