from django.shortcuts import render, redirect

from django.contrib import messages

from django.views.generic.list import ListView
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View)
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string
from .forms import ICLContactForm
from .models import IHE_ContactModel, ICL_ContactModel, SHS_ContactModel, IHE_ContactCategoryModel, ICL_ContactCategoryModel, SHS_ContactCategoryModel
from accounts.models import Profile, UserMarketingProfile
# Create your views here.


def create_icl_contact(request):
    
    if request.method == 'POST':
        form = ICLContactForm(request.POST or None)
        
        if form.is_valid():
          
            
            form.save()
            messages.success(request, "New Contact Detail Has Been Created.!")   
            return redirect('careerconsultant:icl_contact_list')
    else:
        form = ICLContactForm()
    template_name = 'icl/icl_create.html'
    context = {
        'form': form
    }        

    return render(request, template_name, context)


class ICLContactListView(ListView):
    model = ICL_ContactModel
    template_name = 'icl/icl_list.html'
    
#     def get_queryset(self):
#         queryset = self.model.objects.all()
#         if (
#             self.request.user.is_icl and not 
#             self.request.user.is_superuser
#         ):
#             queryset = queryset.filter(
#                 Q(created_by=self.request.user)
#             )
            
#         if request_post:
#             if request_post.get('name'):
#                 queryset = queryset.filter(
#                 name__icontains=request_post.get('name')
#             )
#         if request_post:
#             if request_post.get('created_by'):
#                 queryset = queryset.filter(
#                     crreated_by__icontains=request_post.get('created_by')
#                 )

            
#         if request_post.get('org_type'):
#             query_set = queryset.filter(
#                 org_type__icontains=request_post.get('org_type')
#             )
        
#         if request_post.get('telephone_number'):
#             query_set = queryset.filter(
#                 telephone_number__icontains=request_post.get('telephone_number')
#             )
        
#         if request_post.get('phone_number'):
#                query_set = queryset.filter(
#                phone_number__icontains=request_post.get('phone_number')
#             )
    
#         if request_post.get('email'):
#                query_set = queryset.filter(
#                email_icontains=request_post.get('email')
#             )
    
#         if request_post.get('c_person'):
#                query_set = queryset.filter(
#                 c_person__icontains=request_post.get('c_person')
#             )
#         return queryset.distinct()
        
    
#     def get_context_data(self, **kwargs):
#         context = super(ICLContactListView, self).get_context_data(**kwargs)
#         context['icl_contact_list'] = self.get_queryset()
#         context['per_page'] = self.request.POST.get('per_page')
#         context['users'] = Profile.objects.filter(is_active=True).order_by('last_name')
        
#         search = False
#         if(
#             self.request.POST.get('name') or
#             self.request.POST.get('org_type') or
#             self.request.POST.get('telephone_number') or
#             self.request.POST.get('phone_number') or
#             self.request.POST.get('email') or
#             self.request.POST.get('c_person')
#         ):
#             search=True
#         context['search'] = search
#         return context
        
#     def post(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return self.render_to_response(context)


# class ICLCreateContactView(CreateView):
#     model       = ICL_ContactModel
#     form_class  = ICLContactForm
#     template_name = 'icl/icl_create.html'

#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_icl or self.request.user.is_superuser:
#             self.users = Profile.objects.filter(is_active=True).order_by('last_email')
        
#         else:
#             self.users = Profile.objects.filter(is_icl=True).order_by('last_email')
#         return super(ICLCreateContactView, self).dispatch(
#             request, *args, **kwargs
#         )
        
#         def get_form_kwargs(self):
            
#             kwargs = super(ICLCreateContactView, self).get_form_kwargs()
#             if self.request.user/is_icl or self.request.user.is_superuser:
#                 self.users= Profile.objects.filter(is_active=True).order_by('last_name')
            
#             return kwargs
            

#     def post(self, request,*args,**kwargs):
#         self.object = None
#         form = self.get_form()
#         icl_contactform = ICLContactForm(request.POST)
#         if form.is_valid() and icl_contactform.is_valid():
            
#             iclcontact_obj          = icl_contactform.save()
#             contact_obj             = form.asve(commit=False)
#             contact_obj.created_by  = self.request.user
#             contact_obj.save()
            
#         return self.form_invalid(form)

    
#     def form_invalid(self, form):
#         icl_contactform = ICLContactForm(self.rquest.POST)
#         if self.request.is_ajax():
#             return JsonResponse({'error': True, 'contact_errors': form.errors})
    
#     def get_context_data(self, **kwargs):
        
#        context = super(ICLCreateContactView, self).get_context_data(**kwargs)
#        context['contact_form'] = context['form']
#        context['users'] = self.users
       
       
       
