
import json

from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from centermanager.models import SchoolYearModel, TargetSheet, MatriculationStatusCategory, MatriculationCourseCategory, Matriculation, SanctionSetting, CommissionSetting
from centermanager.forms import SchoolYearForm, TargetSheetForm, MatriculationForm, SanctionSettingForm, CommissionSettingForm
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, ListView)
from django.urls import reverse
from django.db.models import Q
from django.template.loader import render_to_string
from accounts.models import User
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
        context['employee_obj_list'] = self.get_queryset
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
    
    
    
    
    
    
    
    
    
    
    
''' School Year Views '''    



class SchoolYearCreateView(CreateView):
    model = SchoolYearModel
    form_class = SchoolYearForm
    template_name = 'school_year/school_year.html'
    
    
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_centermanager:
            self.users = User.objects.filter(is_active=True).order_by('email')
        else:
            self.users = User.objects.filter(is_centermanager=True).order_by('email')
        return super(SchoolYearCreateView, self).dispatch(request, *args, **kwargs)    
    
    def post(self,request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            school_year_obj = form.save(commit=False)
            school_year_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        school_year_obj = form.save(commit=False)
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':False,
                }
            )
        return redirect("centermanager:target")
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'school_year_errors':form.errors
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
    
    def get_context_data(self, **kwargs):
        context = super(SchoolYearCreateView, self).get_context_data(**kwargs)
        context['school_year_form'] = context['form']
        return context



''' Target Sheet View '''

class TargetSheetListView(TemplateView):
    model = TargetSheet
    context_object_name = 'target_sheet_obj'
    template_name = 'target_sheet/targetsheet_list.html'

    
    def get_queryset(self):
        queryset = self.model.objects.all()
         
        request_post = self.request.POST
        if request_post:
            if request_post.get('school_year'):
                queryset = queryset.filter(
                    school_year__icontains=request_post.get('school_year')
                )
        return queryset.distinct()
    
    
    def get_context_data(self, **kwargs):
        context = super(TargetSheetListView, self).get_context_data(**kwargs)
        context['target_sheet_obj'] = self.get_queryset()
        context['per_page'] = self.request.POST.get('per_page')
        
        search = False
        if (
            self.request.POST.get('school_year')
        ):
            search = True
        context['search'] = search
        return context
    
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)        
        

class TargetSheetCreateView(CreateView):
    model = TargetSheet
    form_class = TargetSheetForm
    template_name = 'target_sheet/create_target.html'
    
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_centermanager:
            self.users = User.objects.filter(is_active=True).order_by('email')
        else:
            self.users = User.objects.filter(is_centermanager=True).order_by('email')
        return super(TargetSheetCreateView, self).dispatch(
            request, *args, **kwargs
        )
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            target_sheet_obj = form.save(commit=False)
            target_sheet_obj.save()
            
        return self.form_valid(form)
        return self.form_invalid(form)
    
    
    
    def form_valid(self, form):
        target_sheet_obj = form.save(commit=False)
        
        #current_site = get_current_site(self.request)
        
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error': False,
                }
            )
        return redirect('centermanager:create_target')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error': True,
                    'target_sheet_errors': form.errors
                }
            )
            
        return self.render_to_response(
            self.get_context_data(form=form)
        )
        
    def get_context_data(self, **kwargs):
        context = super(TargetSheetCreateView, self).get_context_data(**kwargs)
        context['target_form'] = context['form']
        return context


 
class TargetSheetDetailView(DetailView):
    model = TargetSheet
    form_class = TargetSheetForm
    template_name = 'target_sheet/target_details.html'
    
    
class TargetUpdateView(UpdateView):
    model = TargetSheet
    form_class = TargetSheetForm
    template_name = 'target_sheet/create_target.html'
    
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            target_sheet_obj = form.save(commit=False)
            target_sheet_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    
    def form_valid(self):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':False,
                }
            )
        return redirect('centermanager:target_update')
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'target_sheet_error': form.errors,
                }
            )
        return redirect('centermanager:create_target')
    
    
    def get_context_data(self, **kwargs):
        context = super(TargetUpdateView, self).get_context_data(**kwargs)
        context['target_sheet_obj'] = self.object
        context['target_sheet_form'] = context['form']
        
        return context
    
    
# class TargetUpdateView(UpdateView):
#     model = TargetSheet
#     form_class = TargetSheetForm
#     template_name = 'target_sheet/create_target.html'
#     success_url = reverse_lazy('centermanager:target_list')

#     def form_valid(self, form):
#         form.save()
#         message_text = 'Your {} was Updated Successfully!'.format(
#             form.instance)
#         messages.success(self.request, message_text)
#         if 'continue' in self.request.POST:
#             return HttpResponseRedirect(
#                 reverse_lazy('centermanager:update_target',
#                              kwargs={'pk': form.instance.pk}))
#         else:
#             return super().form_valid(form)




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
    
    
      
'''  SANCTION SETTING '''

class SanctionSettingListView(TemplateView):
    model = SanctionSetting
    context_object_name = 'sanction_obj_list'
    template_name = 'sanction/sanction_list.html'
    
    def get_queryset(self):
        queryset = self.model.objects.all
    
    def get_context_data(self, **kwargs):
        context = super(SanctionSettingListView, self).get_context_data(**kwargs)
        context['per_page'] = self.request.POST.get('per_page')
        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    

class SanctionSettingCreateView(CreateView):
    model = SanctionSetting
    form_class = SanctionSettingForm
    template_name = 'sanction/create_sanction.html'
    
    def dispatch(self, request, *args,  **kwargs):
        if self.request.user.is_centermanager:
            self.users = User.objects.filter(is_active=True).order_by('email')
        else:
            self.users = User.objects.filter(is_centermanager=True).order_by('email')
        return super(SanctionSettingCreateView, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()

        if form.is_valid():
            sanction_obj = form.save(commit=False)
            sanction_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    
    def form_valid(self, form):
        sanction_obj = form.save(commit=False)
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':False,
                }
            )
        if self.request.POST.get("savenewform"):
            return redirect('centermanager:create_sanction')
        return redirect('centermanager:sanction_list')
    
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'sanction_errors': form.errors
                }
            )
            
        return self.render_to_response(
            self.get_context_data(form=form)
        )
        
    def def_context_data(self, **kwargs):
        context = super(SanctionSettingCreateView, self).get_context_data(**kwargs)
        context['sanction_form'] = context['form']
        return context
            
    
            


class SanctionSettingDetailView(DetailView):
    model = SanctionSetting
    context_object_name = 'sanction_record'
    template_name = 'sanction/sanction_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SanctionSettingDetailView, self).get_context_data(**kwargs)
        return context


class SanctionSettingUpdateView(UpdateView):
    model = SanctionSetting
    form_class = SanctionSettingForm
    template_name = 'sanction/create_sanction.html'
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.is_centermanager:
            self.users = User.objects.filter(is_active=True).order_by('email')
        else:
            self.users = User.objects.filter(is_centermanager=True).order_by('email')
        return super(SanctionSettingUpdateView, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            sanction_obj = form.save(commit=False)
            sanction_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':False,
                }
            )
        return redirect('centermanager:sanction_list')
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'sanction_error': form.errors,
                }
            )
        return redirect('centermanager:create_sanction')
    
    def get_context_data(self, **kwargs):
        context = super(SanctionSettingUpdateView, self).get_context_data(**kwargs)
        context['sanction_obj'] = self.object
        context['sanction_form'] = context['form']
        
        return context            

# class SanctionUpdateView(UpdateView):
#     model = SanctionSetting
#     form_class = SanctionSettingForm
#     template_name = 'sanction_setting/create_sanction.html'
#     success_url = reverse_lazy('centermanager:sanction_list')

#     def form_valid(self, form):
#         form.save()
#         message_text = 'Your {} was Updated Successfully!'.format(
#             form.instance)
#         messages.success(self.request, message_text)
#         if 'continue' in self.request.POST:
#             return HttpResponseRedirect(
#                 reverse_lazy('centermanager:sanction_update',
#                              kwargs={'pk': form.instance.pk}))
#         else:
#             return super().form_valid(form)


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
