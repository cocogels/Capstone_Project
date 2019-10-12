
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import ( CreateView, UpdateView, DetailView, TemplateView, View )
from contacts.models import ICL_ContactModel, SHS_ContactModel, IHE_ContactModel
from contacts.forms import ICLContactForm, SHSContactForm, IHEContactForm
from accounts.models import User
from django.db.models import Q

''' ICL CONTACT  VIEWS '''

class ICLContactListView(TemplateView):
    model = ICL_ContactModel
    context_object_name = 'contact_obj_list'
    template_name = 'contacts.html'
    
    def get_queryset(self):
        queryset = self.model.objects.all()
        queryset = queryset.filter(
            Q(assigned_to__in=[self.request.user])|
            Q(created_by=self.request.user)
        )
        request_post = self.request.POST 
        if request_post:
            if request_post.get('name'):
                queryset = queryset.filter(
                    name__icontains=request_post.get('name')
                )
            
            if request_post.get('org_type'):
                queryset = queryset.filter(
                    org_type__icontains=request_post.get('org_type')
                )
    
            if request_post.get('phone_nummber'):
                queryset = queryset.filter(
                    phone_number__icontains=request_post.get('phone_number')
                )
            
            if request_post.get('email'):
                queryset = queryset.filter(
                    email__icontains=request_post.get('email')
                )
            
            if request_post.get('person'):
                queryset = queryset.filter(
                    person__icontains=request_post.get('person')
                )
            
            if request_post.get('address'):
                queryset = queryset.filter(
                    address__icontains=request_post.get('address')
                )
            
            if request_post.getlist('assigned_to'):
                queryset = queryset.filter(
                    assigned_to__id__in=request_post.getlist('assiged_to')
                )
                
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super(ICLContactListView ,self).get_context_data(**kwargs)
        context['contact_obj_list'] = self.get_queryset()
        context['per_page'] = self.request.POST.get('per_page')
        context['users'] = User.objects.filter(
            is_active=True
        ).order_by('email')
        
        context['assignedto_list'] = [
            int(i) for i in self.request.POST.getlist('assigned_to', []) if i
        ]
        search = False
        if(
            self.request.POST.get('name') or 
            self.request.POST.get('phone_number') or
            self.request.POST.get('person') or
            self.request.POST.get('address') or
            self.request.POST.get('org_type') or
            self.request.POST.get('email') or
            self.request.POST.get('assigned_to')
        ):
            search=True
        context['search'] = search 
        return context
        
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class ICLContactCreateView(CreateView):
    model = ICL_ContactModel
    form_class = ICLContactForm
    template_name = 'create_contact.html'

    # def get_form_kwargs(self):
    #     kwargs = super(ICLContactCreateView, self).get_form_kwargs()
    #     self.users = User.objects.filter(is_active=True).order_by('email')
    #     kwargs.update({"assigned_to": self.users})
    #     return kwargs
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            contact_obj = form.save(commit=False)
            contact_obj.created_by = self.request.user
            contact_obj.save()
            '''
            to be followed
            student accounts 
            
            '''
            return self.form_valid(form)
        return self.form_invalid(form)
        
    def form_valid(self, form):
        contact_obj = form.save(commit=False)
        # if self.request.POST.getlist('assigned_to', []):
        #     contact_obj.assigned_to.add(
        #         *self.request.POST.getlist('assigned_to')
        #     )
        
        #assigned_to_list = list(contact_obj.assigned_to.all().values_list('id', flat=True))
        current_site = get_current_site(self.request)
        #''' Email Notif to be followed '''
        # recipients = assigned_to_list
        # send_email_to_assigned_user.delay(recipients, contact_obj.id, domain=current_site.domain, protocol=self.request.scheme)
        
        #ajax
        # if self.request.is_ajax():
        #     return JsonResponse({'error': False})
        
        if self.request.POST.get('savenewform'):
            return redirect("contacts:add_contact")
        return redirect('contacts:list')
        
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error': True,
                    'contact_errors':form.errors,
                }
            )
        
        return self.render_to_response(
            self.get_context_data(form=form)
        )
    
    def get_context_data(self, **kwargs):
        context = super(ICLContactCreateView, self).get_context_data(**kwargs)
        context['contact_form'] = context['form']
     #   context['users'] = self.users
    #    context['assignedto_list'] = [
     #       int(i) for i in self.request.POST.getlist('assigned_to', []) if i
      #  ]
        return context

class ICLContactDetailView(DetailView):
    model = ICL_ContactModel
    context_object_name = 'icl_contact_record'
    template_name = 'contact_view.html'
    
    def get_queryset(self):
        queryset = super(ICLContactDetailView, self).get_queryset()
        return queryset.select_related('org_type')
        
    def get_context_data(self, **kwargs):
        context = super(ICLContactDetailView, self).get_context_data(**kwargs)
        user_assign_list = [
            assigned_to.id for assigned_to in context['object'].assigned_to.all()
        ]
        ''' to be followed'''
        # user_assigned_accounts = set(self.request.user.account_assigned_users.values_list('id', flat=True))
        # contact_accounts = set(context['object'].accounts)contacts.values_list('id', flat=True))
        # if user_assigned_accounts.intersection(contact_accounts):
        #     user_assign_list.append(self.request.user.id)
        if self.request.user == context['object'].created_by:
            user_assign_list.append(self.request.user.id)

        assigned_data = []
        for each in context['icl_contact_record'].assigned_to.all():
            assigned_dict = {}
            assigned_dict['id'] = each.id
            assigned_dict['name'] = each.email
            assigned_data.append(assigned_dict)

        if self.request.user != context['object'].created_by:
            users_mention = [{'last_name': context['object'].created_by.last_name}]
            
        return context

class ICLContactUpdateView(UpdateView):
    model = ICL_ContactModel
    form_class = ICLContactForm
    template_name = 'create_contact.html'
    
    def get_form_kwargs(self):
        kwargs=super(ICLContactUpdateView, self).get_form_kwargs()
        self.users = User.objects.filter(is_active=True).order_by('email')
        kwargs.update({"assigned_to": self.users})
        return kwargs
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            contact_obj = form.save(commit=False)
            contact_obj.save()
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        assigned_to_ids = self.get_object().assigned_to.all().values_list('id', flat=True)
        contact_obj = form.save(commit=False)
        previous_assigned_to_users = list(contact_obj.assigned_to.all().values_list('id', flat=True))
        all_members_list = []
        if self.request.POST.getlist('assigned_to', []):
            current_site = get_current_site(self.request)
            assigned_form_users = form.cleaned_data.get(
                'assigned_to'
            ).values_list('id', flat=True)
            all_members_list = list(
                set(list(assigned_form_users) - set(list(assigned_to_ids)))
                
            )
            contact_obj.assigned_to.clear()
            contact_obj.assigned_to.add(
                *self.request.POST.getlist('assigned_to')
                )
        else:
            contact_obj.assigned_to.clear()
        
        current_site = get_current_site(self.request)
        assigned_to_list = list(contact_obj.assigned_to.all().values_list('id', flat=True))
        
        # recipients = list(set(assigned_to_list) - set(previous_assigned_to_users))
        # send_email_to_assigned_user.delay(recipients, contact_obj.id, domain=current_site.domain,
        #     protocol=self.request.scheme)
        
        ''' 
            Additional Request for Leads Account 
        '''
        
        if self.request.is_ajax():
            return JsonResponse({'error': False})
        return redirect('contacts:list')
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error': True, 
                    'contact_errors':form.errors,
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
        
    def get_context_data(self, **kwargs):
        context = super(ICLContactUpdateView, self).get_context_data(**kwargs)
        context['contact_obj'] = self.object
        user_assign_list = [
            assigned_to.id for assigned_to in context['contact_obj'].assigned_to.all()
        ]
        if self.request.user == context['contact_obj'].created_by:
            user_assign_list.append(self.request.user.id)
        
        context['contact_form'] = context['form']
        context['users'] = self.users
        context['assignedto_list'] = [
            int(i) for i in self.request.POST.getlist('assigned_to',[]) if i
        ]
        
        return context
    
    

""" -----------------------------------SHS Contact Views------------------------------------------------------------------- """

class SHSContactListView(TemplateView):
    model = SHS_ContactModel
    context_object_name = 'contact_obj_list'
    template_name = 'shs_contact_list.html'
    
    def get_queryset(self):
        queryset = self.model.objects.all()
        queryset = queryset.filter(
            Q(assigned_to__in=[self.request.user])|
            Q(created_by=self.request.user)
        )

        request_post = self.request.POST
        if request_post:
            if request_post.get('name'):
                queryset = queryset.filter(
                    name__icontains=request_post.get('name')
                )
            if request_post.get('email'):
                queryset = queryset.filter(
                    email__icontains=request_post.get('email')
                )
                
        return queryset.distinct()
    
    
    def get_context_data(self, **kwargs):
        context =  super(SHSContactListView, self).get_context_data(**kwargs)
        context['contact_obj_list'] = self.get_queryset()
        context['per_page'] = self.request.POST.get('per_page')
        context['users'] = User.objects.filter(
            is_active=True
        ).order_by('email')
        
        context['assignedto_list'] = [
            int(i) for i in self.request.POST.getlst('assigned_to', []) if i
        ]
        
        search = False
        if(
          self.request.POST.get('name') or
          self.request.POST.get('email')  
        ):
            search = True
        conetxt['search'] = search
        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
    

class SHSContactCreateView(CreateView):
    model = SHS_ContactModel
    form_class = SHSContactForm
    template_name = 'shs/shs_create_contact.html'
    
    def get_form_kwargs(self):
        kwargs = super(SHSContactCreateView, self).get_form_kwargs()
        self.users = User.objects.filter(is_active=True).order_by('email')
        kwargs.update({
            'assigned_to': self.users
        })
        return kwargs
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            contact_obj = form.save(commit=False)
            contact_obj.created_by = self.request.user
            contact_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    
    def form_valid(self, form):
        contact_obj = form.save(commit=False)
        if self.request.POST.getlist('assigned_to', []):
            contact_obj.assigned_to.add(
                *self.request.POST.getlist('assigned_to')
            )
        
        assigned_to_list = list(contact_obj.assigned_to.all().values_list('id', flat=True))
        current_site = get_current_site(self.request)
        
        if self.request.is_ajax():
            return JsonResponse({'error': False})
        
        if self.request.POST.get('savenewform'):
            return redirect('contacts:shs_add_contact')
        return redierct('contacts:shs_list')
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error': True,
                    'contact_errors':form.errors,
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
        
    def get_context_data(self, **kwargs):
        context = super(SHSContactCreateView,self).get_context_data(**kwargs)
        context['contact_form'] = context['form']
        context['users'] = self.users
        context['assignedto_list'] = [
            int(i) for i in self.request.POST.getlist('assigned_to', []) if i
        ]
        
        return context
    
    
class SHSContactDetailView(DetailView):
    model = SHS_ContactModel
    context_object_name = 'shs_contact_record'
    template_name = 'shs_contact_view.html'
    
    def get_queryset(self):
        queryset - super(SHSContactDetailView, self).get_queryset()
        return get_queryset.select_related('org_type')
    
    def get_context_data(self, **kwargs):
        context = super(SHSContactDetailView, self).get_context_data(**kwargs)
        user_assign_list = [
            assigned_to.id for assigned_to in context['object'].assigned_to.all()
        ]
        
        
        if self.request.user == context['object'].created_by:
            user_assign_list.append(self.request.user.id)
            
        assigned_data = []
        for each in context['shs_contact_record'].assigned_to.all():
            assigned_dict = {}
            assigned_dict['id'] = each.id
            assigned_dict['name'] = each.email
            assigned_data.append(assigned_dict)
            
        if self.request.user != context['object'].created_by:
            users_mention = [{'last_name': context['object'].created_by.last_name}]
    
        return context
    

class SHSContactUpdateView(UpdateView):
    model = SHS_ContactModel
    form_class = SHSContactForm
    template_name = 'shs_create_contact.html'
    
    def get_form_kwargs(self):
        kwargs = super(SHSContactUpdateView,self).get_form_kwargs()
        self.users = User.objects.filter(is_active=True).order_by('email')
        kwargs.update({ 'assigned_to':self.users })
        return kwargs
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            contact_obj = form.save(commit=False)
            contact_obj.save()
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        assigned_to_ids = self.get_object().assigned_to.all().values_list('id', flat=True)
        contact_obj = form.save(commit=False)
        previous_assigned_to_users = list(contact_obj.assigned_to.all().values_list('id', flat=True))
        all_members_list = []
        if self.request.POST.getlist('assigned_to', []):
            current_site = get_current_site(self.request)
            assigned_form_users = form.cleaned_data.get(
                'assigned_to'
            ).values_list('id', flat=True)
            all_members_list = list(
                set(list(assigned_form_users)) - set(list(assigned_to_ids))
            )
            contact_obj.assigned_to.clear()
            contact_obj.assigned_to.add(
                *self.request.POST.getlist('assigned_to')
            )
        else:
            contact_obj.assigned_to.clear()
        
        current_site = get_current_site(self.request)
        assigned_to_list = list(contact_obj.assigned_to.all().values_list('id', flat=True))
        
        if self.request.is_ajax():
            return JsonResponse({'error': False})
        return redirect('contacts:shs_list')
        
        
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error': True,
                    'contact_errors': form.errors,
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
        
    
    def get_context_data(self, **kwargs):
        context = super(SHSContactUpdateView, self).get_context_data(**kwargs)
        context['contact_obj'] = self.object
        context['users'] = self.users
        context['assignedto_list'] = [
            int(i) for i in self.request.POSt.getlist('assigned_to',[]) if i
        ]
        
        return context


"""---------------------------------------------------IHE Contact Views------------------------------------- """


class IHEContactListView(TemplateView):
    model = IHE_ContactModel
    context_object_name = 'contact_obj_list'
    template_name = 'ihe_contact_list.html'
    
    def get_queryset(self):
        queryset = self.model.objects.all()
        queryset = queryset.filter(
            Q(assigned_to__in=[self.request.user])|
            Q(created_by=self.request.user)
        )
        request_post = self.request.POST
        if request_post:
            if request_post.get('name'):
                queryset = queryset.filter(
                    name__icontains = request_post.get('name')
                )
        
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super(IHEContactListView, self).get_context_data(**kwargs)
        context['contact_obj_list'] = self.get_queryset()
        context['per_page'] = self.request.POST.get('per_page')
        context['users'] = User.objects.filter(
            is_active=True
        ).order_by('email')
        
        context['assignedto_list'] = [
            int(i) for i in self.request.POST.getlist('assigned_to', []) if i
        ]
        
        search = False
        if(
            self.request.POST.get('name')
        ):
            search = True
        context['search'] = search
        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)



class IHEContactCreateView(CreateView):
    model = IHE_ContactModel
    form_class = IHEContactForm
    template_name = 'ihe_create_contact.html'
    
    def get_form_kwargs(self):
        kwargs = super(IHEContactCreateView, self).get_form_kwargs()
        self.users = User.objects.filter(is_active=True).order_by('email')
        kwargs.update({ 'assigned_to': self.users })
        return kwargs
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            contact_obj = form.save(commit=False)
            contact_obj.created_by = self.request.user
            contact_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        contact_obj = form.save(commit=False)
        if self.request.POST.getlist('assigned_to', []):
            contact_obj.assigned_to.add(
                *self.request.POST.getlist('assigned_to')
            )
            
        assigned_to_list = list(contact_obj.assigned_to.all().values_list('id', flat=True))
        current_site = get_current_site(self.request)   
        
        if self.request.is_ajax():
            return JsonResponse({'error': False})
        
        if self.request.POST.get('savenewform'):
            return redirect('contacts:ihe_add_contact')
        return redirect('contacts:ihe_list')
    
    def get_context_data(self, **kwargs):
        context = super(IHEContactCreateView, self).get_context_data(**kwargs)
        context['contact_form'] = context['form']
        context['users'] = self.users
        context['assignedto_list'] =[
            int(i) for i in self.request.POST.getlist('assigned_to',[]) if i
        ]
        
        return context
    
class IHEContactDetailView(DetailView):
    model = IHE_ContactModel
    context_object_name = 'ihe_contact_record'
    template_name = 'ihe_contact_view.html'
    
    def get_queryset(self):
        queryset - super(IHEContactDetailView, self).get_queryset()
        return queryset.select_related('org_type')
    
    def get_context_data(self, **kwargs):
        context = super(IHEContactDetailView, self).get_context_data(**kwargs)
        user_assign_list = [
            assigned_to.id for assigned_to in context['object'].assigned_to.all()
        ]

        if self.request.user == context['object'].created_by:
                user_assign_list.append(self.request.user.id)

        assigned_data = []
        for each in context['icl_contact_record'].assigned_to.all():
            assigned_dict = {}
            assigned_dict['id'] = each.id
            assigned_dict['name'] = each.email
            assigned_data.append(assigned_dict)

        if self.request.user != context['object'].created_by:
            users_mention = [{'last_name': context['object'].created_by.last_name}]
            
        return context
    


class IHEContactUpdateView(UpdateView):
    model = IHE_ContactModel
    form_class = IHEContactForm
    template_name = 'ihe_create_contact.html'
    
    def get_form_kwargs(self):
        kwargs=super(IHEContactUpdateView, self).get_form_kwargs()
        self.users = User.objects.filter(is_active=True).order_by('email')
        kwargs.update({"assigned_to": self.users})
        return kwargs    
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            contact_obj = form.save(commit=False)
            contact_obj.save()
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        assigned_to_ids = self.get_object().assigned_to.all().values_list('id', flat=True)
        contact_obj = form.save(commit=False)
        previous_assigned_to_users = list(contact_obj.assigned_to.all().values_list('id', flat=True))
        all_members_list = []
        if self.request.POST.getlist('assigned_to', []):
            current_site = get_current_site(self.request)
            assigned_form_users = form.cleaned_data.get(
                'assigned_to'
            ).values_list('id', flat=True)
            all_members_list = list(
                set(list(assigned_form_users) - set(list(assigned_to_ids)))
                
            )
            contact_obj.assigned_to.clear()
            contact_obj.assigned_to.add(
                *self.request.POST.getlist('assigned_to')
                )
        else:
            contact_obj.assigned_to.clear()
        
        current_site = get_current_site(self.request)
        assigned_to_list = list(contact_obj.assigned_to.all().values_list('id', flat=True))
        
        if self.request.is_ajax():
            return JsonResponse({'error': False})
        return redirect('contacts:ihe_list')
    
    def form_invalid(self, **kwargs):
        if self.request.is_ajax():
            return JsonResponse(
            {
                'error': True, 
                'contact_errors':form.errors,
            }
        )
        return self.render_to_response(
            self.get_context_data(form=form)
        )



    def get_context_data(self, **kwargs):
        context = super(IHEContactUpdateView, self).get_context_data(**kwargs)
        context['contact_obj'] = self.object
        user_assign_list = [
            assigned_to.id for assigned_to in context['contact_obj'].assigned_to.all()
        ]
        if self.request.user == context['contact_obj'].created_by:
            user_assign_list.append(self.request.user.id)

        context['contact_form'] = context['form']
        context['users'] = self.users
        context['assignedto_list'] = [
            int(i) for i in self.request.POST.getlist('assigned_to', []) if i
        ]

        return context
    
