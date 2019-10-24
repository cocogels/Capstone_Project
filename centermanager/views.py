
import json

from datetime import date, timedelta
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from centermanager.models import SchoolYear, MatriculationStatusCategory, MatriculationCourseCategory, Matriculation, SanctionSetting, CommissionSetting
from centermanager.forms import MatriculationForm, SanctionSettingForm, CommissionSettingForm , SchoolYearForm
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, ListView)
from django.urls import reverse
from django.db.models import Q
from django.template.loader import render_to_string
from accounts.models import User
from django.views.generic.dates import YearMixin, DateMixin
from centermanager.forms import EmployeeRegistrationForm



         
class EmployeeListView(TemplateView):
    model = User
    context_object_name = "employee_obj_list"
    template_name = 'employer/employee_list.html'
    
    def get_queryset(self):
        queryset = self.model.objects.all()
        
        request_post = self.request.POST
        if request_post:
            if request_post.get('first_name'):
                queryset = queryset.filter(
                    first_name__icontains=request_post.get('first_name')
                )
                
            if request_post.get('last_name'):
                queryset = queryset.filter(
                    last_name___icontains=request_post.get('last_name')
                )
            
            if request_post.get('email'):
                queryset = queryset.filter(
                    email__icontains=request_post.get('email')
                )
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        context['employee_obj_list'] = self.get_queryset()
        context['per_page'] = self.request.POST.get('per_page')    
        context['users'] = User.objects.filter(is_active=True).order_by('email')
        
        search = False
        if (
            self.request.POST.get('first_name') or
            self.request.POST.get('last_name') or
            self.request.POST.get('email')
        ):
            search = True
        context['search'] = search
        return context
    
    def post(self, request, *args ,**kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    



class EmployeeRegistration(CreateView):
    model = User
    form_class = EmployeeRegistrationForm
    template_name = 'employer/create_employee.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_centermanager:
            self.users = User.objects.filter(is_active=True).order_by('email')
        else:
            self.users = User.objects.filter(is_centermanager=True).order_by('email')
        return super(EmployeeRegistration, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            employee_obj = form.save(commit=False)
            employee_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        employee_obj = form.save(commit=False)

        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':False,
                }
            )

        if self.request.POST.get("savenewform"):
            return redirect("centermanager:add_employee")
        return redirect("centermanager:employee_list")


    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'employee_errors': form.errors,
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
    
    def get_context_data(self, **kwargs):
        context = super(EmployeeRegistration, self).get_context_data(**kwargs)
        context['employee_form'] = context["form"]
        context['employee_list'] = User.objects.all() #can be used in any page
        context['users'] = self.users
        return context
    

class EmployeeDetailView(DetailView):
    model = User
    context_object_name = "employee_record"
    template_name = 'employer/employee_detail.html'
    
    def get_queryset(self):
        queryset = super(EmployeeDetailView, self).get_queryset(**kwargs)
        return queryset.select_related('email')

    
    def get_context_data(self, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)
        return context
    
    
class EmployeeUpdateView(UpdateView):
    model = User
    form_class = EmployeeRegistrationForm
    template_name = "employer/create_empoyee.html"
    
    def dispatch(self, request, *args, **kwargs):
        if (self.request.user.is_centerbusinessmanager or
            self.request.user.is_marketinghead or
            self.request.user.is_registrar
            ):
            self.users = User.objects.filter(is_active=True).order_by('email')
        else:
            self.users = User.objects.filter(is_centerbusinessmanager=True,
                                             is_marketinghead=True,
                                             is_registrar=True
                                             )    
        return super(EmployeeUpdateView, self).dispatch(request, *args, **kwargs)
    
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            employee_obj = form.save(commit=False)
            employee_obj.save()

            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        employee_obj = form.save(commit=False)
        if self.request.is_ajax():
            return JsonResponse({
                'error':False,
            })    
        return redirect('centermanager:employee_list')
    
    
    def form_invalid(self, form):
        
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'employee_errors': form.errors
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
    
    def get_context_data(self, **kwargs):
        context = super(EmployeeUpdateView, self).get_context_data(**kwargs)
        context['employee_obj'] = self.object
        context['employee_form'] = context['form']
        
        return context
    
 


'''Payment Details '''

class PaymentListView(TemplateView):
    model = Matriculation
    context_object_name = 'payment_obj_list'
    template_name = 'payment/payment_list.html'
    
    def get_queryset(self):
        queryset = self.model.objects.all()

        
        request_post = self.request.POST
        if request_post:
            if request_post.get('status'):
                queryset = queryset.filter(
                    status__icontains=request_post.get('status')
                )
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super(PaymentListView, self).get_context_data(**kwargs)
        context['payment_obj_list'] = self.get_queryset()
        context['per_page'] = self.request.POST.get('per_page')
        
        search = False
        if (
            self.request.POST.get('status')
        ):
            search = True
        context['search'] = search
        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    

class PaymentCreateView(CreateView):
    model = Matriculation
    form_class = MatriculationForm
    template_name = 'payment/create_payment.html'
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_centermanager:
            self.users = User.objects.filter(is_active=True).order_by('email')
        else:
            self.users = User.objects.filter(is_centermanager=True).order_by('email')
        return super(PaymentCreateView, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            payment_obj = form.save(commit=False)
            payment_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def from_valid(self, form):
        payment_obj = form.save(commit=False)
        
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':False
                }
            )
        if self.request.POST.get("savenewform"):
            return redirect('centermanager:create_payment')
    
        return redirect('centermanager:payment_list')
    
    def form_invalid(self, form):
        
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'payment_errors':form.errors,
                }
            )        

    def get_context_data(self, **kwargs):
        context = super(PaymentCreateView, self).get_context_data(**kwargs)
        context['payment_form'] = context['form']
        return context


class PaymentDetailView(DetailView):
    model = Matriculation
    context_object_name = 'payment_record'
    template_name = 'payment/payment_details.html'
    
    def get_queryset(self):
        queryset =  super(PaymentDetailView, self).get_queryset()
        return queryset.select_related('status')
    
    def get_context_data(self, **kwargs):
        context = super(PaymentDetailView, self).get_context_data(**kwargs)
        return context


class PaymentUpdateView(UpdateView):
    model = Matriculation
    form_class = MatriculationForm
    template_name = 'payment/create_payment.html'
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_centermanger:
            self.users = User.objects.filter(is_active=True).order_by('email')
        else:
            self.users = User.objects.filter(is_centermanager=True).order_by('email')
        return super(PaymentUpdateView, self).dispatch(request, *args, **kwargs)
    
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            payment_obj = form.save(commit=False)
            payment_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    
    def form_valid(self, form):
        payment_obj = form.save(commit=False)
        
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True
                }
            )
        return redirect('centermanager:payment_list')
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error': True,
                    'payment_errors': form.errors,
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
            
    def get_context_data(self, **kwargs):
        context = super(PaymentUpdateView, self).get_context_data(**kwargs)
        context['payment_obj'] = self.object
        context['payment_form'] = context=['form']
        
        return context  
    
    


''' Comission Create View '''

class CommissionSettingListView(TemplateView):
    model = CommissionSetting
    context_object_name = 'commission_obj_list'
    template_name = 'commission/commission_list.html'
    
    
    def get_queryset(self):
        queryset = self.model.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super(CommissionSettingListView, self).get_context_data(**kwargs)
        context['commission_obj_list'] = self.get_queryset()
        context['per_page'] = self.request.POST.get('per_page')
        
        return context
    



class CommissionSettingCreateView(CreateView):
    model = CommissionSetting
    form_class = CommissionSettingForm
    template_name = 'commission/create_commission.html' 
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_centermanager:
            self.users = User.objects.filter(is_active=True).order_by('email')
        else:
            self.users = User.objects.filter(is_centermanager=True).order_by('email')
        return super(CommissionSettingCreateView, self).dispatch(
            request, *args, **kwargs
        )
        
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            commission_obj = form.save(commit=False)
            commission_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True
                }
            )
        return redirect('centermanager:create_commission')
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'commission_errors': form.errors
                }
            )

        return self.render_to_response(
            self.get_context_data(form=form)
        )
        
        
    def get_context_data(self, **kwargs):
        context = super(CommissionSettingCreateView, self).get_context_data(**kwargs)
        context['commission_form'] = context['form']
        return context
    
    
        
        

class CommissionDetailView(DetailView):
    model = CommissionSetting
    context_object_name = 'commission_obj'
    template_name = 'commission/commission_detail.html'

    
    def get_context_data(self, **kwargs): 
        context = super(CommissionDetailView, self).get_context_data(**kwargs)
        return context
    
    
    
    
class CommissionUpdateView(UpdateView):
    model = CommissionSetting
    form_class = CommissionSettingForm
    template_name = 'commission/create_commission.html'    
    
    
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_centermanager:
            self.users = User.objects.filter(is_active=True).order_by('email')
        else:
            self.users = User.objects.filter(is_centermanager=True).order_by('email')
        return super(CommissionUpdateView, self).dispatch(
            request, *args, **kwargs
        )    
            
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            commission_obj = form.save(commit=False)
            commission_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        if self.request.is_akax():
            return JsonResponse(
                {
                    'error':True,
                }
            )
        return redirect('centermanager:commission_update')
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'commission_error': form.errors
                }
            )
        return redirect('centermanager:create_commission')
                        
    def get_context_data(self, **kwargs):
        context = super(CommissionUpdateView, self).get_context_data(**kwargs)
        context['commission_obj'] = self.get_object
        context['commission_form'] = context['form']
        
        return context    
    
    
    
    
    
    
    
# class CommissionUpdateView(UpdateView):
#     model = CommissionSetting
#     template_name = 'com_setting/create_commission.html'
#     form_class = CommissionSettingForm
#     success_url = reverse_lazy('centermanager:commission_list')

#     def form_valid(self, form):
#         form.save()
#         messages_text = 'Your {} was Updated Successfully!'.format(
#             form.instance)
#         messages.success(self.request, messages_text)
#         if 'continue' in self.request.POST:
#             return HttpResponseRedirect(
#                 reverse_lazy('centermanager:commission_update',
#                              kwargs={'pk': form.instance.pk})
#             )
#         else:
#             return super().form_valid(form)
