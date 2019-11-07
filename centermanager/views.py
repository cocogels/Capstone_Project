
import json

from datetime import date, timedelta
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404

from centermanager.models import (
    MatriculationSeniorHighSchool,
    MatriculationHigherEducationNC,
    MatriculationHigherEducationRC,
    CommissionSettingSHS,
    CommissionSettingHENC,
    CommissionSettingHERC,
    CommissionSettingICL,
    SchoolYear,
    SanctionSetting,
)

from centermanager.forms import (
    MatriculationSHSForm,
    MatriculationHENCForm,
    MatriculationHERCForm,
    CommissionSettingSHSForm,
    CommissionSettingHERCForm,
    CommissionSettingHENCForm,
    CommissionSettingICLForm,
    SanctionSettingForm,
    SchoolYearForm,
)
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
        context['employee_obj_list'] = self.get_queryset().exclude(is_superuser=True).exclude(is_centermanager=True)
        context['cc_obj_list'] = self.get_queryset().exclude(is_superuser=True).exclude(is_centermanager=True).exclude(is_centerbusinessmanager=True).exclude(is_marketinghead=True).exclude(is_registrar=True)
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
        context['employee_list'] = User.objects.all().exclude(is_superuser=True).exclude(is_centermanager=True)
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

class MatriculationTemplateView(TemplateView):
    template_name = 'payment/payment_list.html'    
    
    def get_context_data(self, **kwargs):
        context = super(MatriculationTemplateView, self).get_context_data(**kwargs)
        context["shs_list"] = MatriculationSeniorHighSchool.objects.all()
        context["he_nc_list"] = MatriculationHigherEducationNC.objects.all()
        context["he_rc_list"] = MatriculationHigherEducationRC.objects.all()
        return context
    
class MatriculationListView(ListView):
    template_nmae = 'payment/payment_view.html'
    
    def get_context_data(self, **kwargs):
        context = super(MatriculationListView, self).get_context_data(**kwargs)
        context["shs"] = MatriculationSeniorHighSchool.objects.all()
        context["he_nc"] = MatriculationHigherEducationNC.objects.all()
        context["he_rc"] = MatriculationHigherEducationRC.objects.all()
        return context
    

class MatriculationUpdateSHS(UpdateView):
    model = MatriculationSeniorHighSchool
    form_class = MatriculationSHSForm
    template_name = 'payment/shs_payment.html'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            shs_obj = form.save(commit=False)
            shs_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    
    def form_valid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error': True,
                }
            )
        return redirect('centermanager:payment_list')
    
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'shs_errors': form.errors,
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
           
    def get_context_data(self, **kwargs):
        context = super(MatriculationUpdateSHS, self).get_context_data(**kwargs)
        context["shs_obj"] = self.object
        context["shs_form"] = context['form'] 
        return context
    
class MatriculationUpdateHENC(UpdateView):
    model = MatriculationHigherEducationNC
    form_class = MatriculationHENCForm
    template_name = 'payment/henc_payment.html'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            henc_obj = form.save(commit=False)
            henc_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    
    def form_valid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error': True,
                }
            )
        return redirect('centermanager:payment_list')
    
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'shs_errors': form.errors,
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
        
    def get_context_data(self, **kwargs):
        context = super(MatriculationUpdateHENC, self).get_context_data(**kwargs)
        context["henc_object"] = self.object
        context['henc_form'] = context['form']
        return context
    
class MatriculationUpdateHERC(UpdateView):
    model = MatriculationHigherEducationRC
    form_class = MatriculationHERCForm
    template_name = 'payment/herc_payment.html'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            herc_obj = form.save(commit=False)
            herc_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    
    def form_valid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error': True,
                }
            )
        return redirect('centermanager:payment_list')
    
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'shs_errors': form.errors,
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
        
    
    def get_context_data(self, **kwargs):
        context = super(MatriculationUpdateHERC, self).get_context_data(**kwargs)
        context["herc_object"] = self.object
        context['herc_form'] = context['form']
        return context
    
        
        
# class PaymentListView(TemplateView):
#     context_object_name = 'payment_obj_list'
#     template_name = 'payment/payment_list.html'
    
#     def get_queryset(self):
#         queryset = self.model.objects.all()

        
#         request_post = self.request.POST
#         if request_post:
#             if request_post.get('status'):
#                 queryset = queryset.filter(
#                     status__icontains=request_post.get('status')
#                 )
#         return queryset.distinct()
    
#     def get_context_data(self, **kwargs):
#         context = super(PaymentListView, self).get_context_data(**kwargs)
#         context['payment_obj_list'] = self.get_queryset()
#         context['per_page'] = self.request.POST.get('per_page')
        
#         search = False
#         if (
#             self.request.POST.get('status')
#         ):
#             search = True
#         context['search'] = search
#         return context
    
#     def post(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return self.render_to_response(context)
    

# class PaymentCreateView(CreateView):
#     model = Matriculation
#     form_class = MatriculationForm
#     template_name = 'payment/create_payment.html'
    
#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_centermanager:
#             self.users = User.objects.filter(is_active=True).order_by('email')
#         else:
#             self.users = User.objects.filter(is_centermanager=True).order_by('email')
#         return super(PaymentCreateView, self).dispatch(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form = self.get_form()
#         if form.is_valid():
#             payment_obj = form.save(commit=False)
#             payment_obj.save()
            
#             return self.form_valid(form)
#         return self.form_invalid(form)
    
#     def from_valid(self, form):
#         payment_obj = form.save(commit=False)
        
#         if self.request.is_ajax():
#             return JsonResponse(
#                 {
#                     'error':False
#                 }
#             )
#         if self.request.POST.get("savenewform"):
#             return redirect('centermanager:create_payment')
    
#         return redirect('centermanager:payment_list')
    
#     def form_invalid(self, form):
        
#         if self.request.is_ajax():
#             return JsonResponse(
#                 {
#                     'error':True,
#                     'payment_errors':form.errors,
#                 }
#             )        

#     def get_context_data(self, **kwargs):
#         context = super(PaymentCreateView, self).get_context_data(**kwargs)
#         context['payment_form'] = context['form']
#         return context


# class PaymentDetailView(DetailView):
#     model = Matriculation
#     context_object_name = 'payment_record'
#     template_name = 'payment/payment_details.html'
    
#     def get_queryset(self):
#         queryset =  super(PaymentDetailView, self).get_queryset()
#         return queryset.select_related('status')
    
#     def get_context_data(self, **kwargs):
#         context = super(PaymentDetailView, self).get_context_data(**kwargs)
#         return context


# class PaymentUpdateView(UpdateView):
#     model = Matriculation
#     form_class = MatriculationForm
#     template_name = 'payment/create_payment.html'
    
#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_centermanger:
#             self.users = User.objects.filter(is_active=True).order_by('email')
#         else:
#             self.users = User.objects.filter(is_centermanager=True).order_by('email')
#         return super(PaymentUpdateView, self).dispatch(request, *args, **kwargs)
    
    
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             payment_obj = form.save(commit=False)
#             payment_obj.save()
            
#             return self.form_valid(form)
#         return self.form_invalid(form)
    
    
#     def form_valid(self, form):
#         payment_obj = form.save(commit=False)
        
#         if self.request.is_ajax():
#             return JsonResponse(
#                 {
#                     'error':False
#                 }
#             )
#         return redirect('centermanager:payment_list')
    
#     def form_invalid(self, form):
#         if self.request.is_ajax():
#             return JsonResponse(
#                 {
#                     'error': True,
#                     'payment_errors': form.errors,
#                 }
#             )
#         return self.render_to_response(
#             self.get_context_data(form=form)
#         )
            
#     def get_context_data(self, **kwargs):
#         context = super(PaymentUpdateView, self).get_context_data(**kwargs)
#         context['payment_obj'] = self.object
#         context['payment_form'] = context['form']
        
#         return context  
    
    


''' Comission Create View '''


class CommissionSettingListView(TemplateView):
    template_name = 'commission/commission_list.html'
    
        
    def get_context_data(self, **kwargs):
        context = super(CommissionSettingListView, self).get_context_data(**kwargs)
        context['commission_shs_list'] = CommissionSettingSHS.objects.all()
        context['commission_henc_lst'] = CommissionSettingHENC.objects.all()
        context['commission_herc_lst'] = CommissionSettingHERC.objects.all()
        context['commission_icl_lst'] = CommissionSettingICL.objects.all()
        return context
    


''' --------------------------COMMISSION SHS ----------------------------------'''
class CommissionSettingSHSUpdate(UpdateView):
    model = CommissionSettingSHS
    form_class = CommissionSettingSHSForm
    template_name = 'commission/shs_update.html'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            shs_obj = form.save(commit=False)
            shs_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        shs_obj = form.save(commit=False)
        if self.request.is_ajax():
            return JsonResponse(
                
                {
                    'error':False
                }
            )
        return redirect('centermanager:com_shs_update')
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'shs_errors': form.errors
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shs_form"] = context['form'] 
        # context['commission_shs_list'] = CommissionSettingSHS.objects.all()
        context['commission_henc_lst'] = CommissionSettingHENC.objects.all()
        context['commission_herc_lst'] = CommissionSettingHERC.objects.all()
        context['commission_icl_lst'] = CommissionSettingICL.objects.all()
        return context



''' ---------------------------- HENC COMMISSION --------------------------- '''
class CommissionSettingHENCUpdate(UpdateView):
    model = CommissionSettingHENC
    form_class = CommissionSettingHENCForm
    template_name = 'commission/henc_update.html'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            henc_obj = form.save(commit=False)
            henc_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        henc_obj = form.save(commit=False)
        if self.request.is_ajax():
            return JsonResponse(
                
                {
                    'error':False
                }
            )
        return redirect('centermanager:com_henc_update')
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'henc_errors': form.errors
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["henc_form"] = context['form'] 
        context['commission_shs_list'] = CommissionSettingSHS.objects.all()
        #context['commission_henc_lst'] = CommissionSettingHENC.objects.all()
        context['commission_herc_lst'] = CommissionSettingHERC.objects.all()
        context['commission_icl_lst'] = CommissionSettingICL.objects.all()
        return context
    
    
'''--------------------------------- HERC COMMISSION ----------------------------'''
class CommissionSettingHERCUpdate(UpdateView):
    model = CommissionSettingHERC
    form_class = CommissionSettingHERCForm
    template_name = 'commission/herc_update.html'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            herc_obj = form.save(commit=False)
            herc_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        herc_obj = form.save(commit=False)
        if self.request.is_ajax():
            return JsonResponse(
                
                {
                    'error':False
                }
            )
        return redirect('centermanager:com_herc_update')
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'herc_errors': form.errors
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["herc_form"] = context['form'] 
        context['commission_shs_list'] = CommissionSettingSHS.objects.all()
        context['commission_henc_lst'] = CommissionSettingHENC.objects.all()
        # context['commission_herc_lst'] = CommissionSettingHERC.objects.all()
        context['commission_icl_lst'] = CommissionSettingICL.objects.all()
        return context
    
''' ------------------------------ ICL COMMMISSION --------------------------- '''
class CommissionSettingICLUpdate(UpdateView):
    model = CommissionSettingICL
    form_class = CommissionSettingICLForm
    template_name = 'commission/icl_update.html'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            herc_obj = form.save(commit=False)
            herc_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        herc_obj = form.save(commit=False)
        if self.request.is_ajax():
            return JsonResponse(
                
                {
                    'error':False
                }
            )
        return redirect('centermanager:commission_list')
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'icl_errors': form.errors
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["icl_form"] = context['form'] 
        context['commission_shs_list'] = CommissionSettingSHS.objects.all()
        context['commission_henc_lst'] = CommissionSettingHENC.objects.all()
        context['commission_herc_lst'] = CommissionSettingHERC.objects.all()
        #context['commission_icl_lst'] = CommissionSettingICL.objects.all()
        return context  
    
    
          
# class CommissionSettingCreateView(CreateView):
#     model = CommissionSetting
#     form_class = CommissionSettingForm
#     template_name = 'commission/create_commission.html' 
    
#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_centermanager:
#             self.users = User.objects.filter(is_active=True).order_by('email')
#         else:
#             self.users = User.objects.filter(is_centermanager=True).order_by('email')
#         return super(CommissionSettingCreateView, self).dispatch(
#             request, *args, **kwargs
#         )
        
#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form = self.get_form()
#         if form.is_valid():
#             commission_obj = form.save(commit=False)
#             commission_obj.save()
            
#             return self.form_valid(form)
#         return self.form_invalid(form)
    
#     def form_valid(self, form):
#         if self.request.is_ajax():
#             return JsonResponse(
#                 {
#                     'error':True
#                 }
#             )
#         return redirect('centermanager:create_commission')
    
#     def form_invalid(self, form):
#         if self.request.is_ajax():
#             return JsonResponse(
#                 {
#                     'error':True,
#                     'commission_errors': form.errors
#                 }
#             )

#         return self.render_to_response(
#             self.get_context_data(form=form)
#         )
        
        
#     def get_context_data(self, **kwargs):
#         context = super(CommissionSettingCreateView, self).get_context_data(**kwargs)
#         context['commission_form'] = context['form']
#         return context
    
    
        
        

# class CommissionDetailView(DetailView):
#     model = CommissionSetting
#     context_object_name = 'commission_obj'
#     template_name = 'commission/commission_detail.html'

    
#     def get_context_data(self, **kwargs): 
#         context = super(CommissionDetailView, self).get_context_data(**kwargs)
#         return context
    
    
    
    
# class CommissionUpdateView(UpdateView):
#     model = CommissionSetting
#     form_class = CommissionSettingForm
#     template_name = 'commission/create_commission.html'    
    
    
    
#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_centermanager:
#             self.users = User.objects.filter(is_active=True).order_by('email')
#         else:
#             self.users = User.objects.filter(is_centermanager=True).order_by('email')
#         return super(CommissionUpdateView, self).dispatch(
#             request, *args, **kwargs
#         )    
            
    
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             commission_obj = form.save(commit=False)
#             commission_obj.save()
            
#             return self.form_valid(form)
#         return self.form_invalid(form)
    
#     def form_valid(self, form):
#         if self.request.is_akax():
#             return JsonResponse(
#                 {
#                     'error':True,
#                 }
#             )
#         return redirect('centermanager:commission_update')
    
#     def form_invalid(self, form):
#         if self.request.is_ajax():
#             return JsonResponse(
#                 {
#                     'error':True,
#                     'commission_error': form.errors
#                 }
#             )
#         return redirect('centermanager:create_commission')
                        
#     def get_context_data(self, **kwargs):
#         context = super(CommissionUpdateView, self).get_context_data(**kwargs)
#         context['commission_obj'] = self.get_object
#         context['commission_form'] = context['form']
        
#         return context    
    
    
    
    
    
    
    
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
