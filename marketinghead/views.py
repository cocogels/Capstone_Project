import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View)
from django.urls import reverse
from django.db.models import Q
from django.template.loader import render_to_string
from marketinghead.models import Budget, Collateral, AssignQuota, AssignTerritory
from marketinghead.forms  import BudgetForm, CollateralForm, AssignQuotaForm, AssignTerritoryForm
from accounts.models import User
from django.core.exceptions import PermissionDenied



class AssignQuotaListView(LoginRequiredMixin, TemplateView):
    model = AssignQuota
    context_object_name = 'assign_obj_list'
    template_name = 'quota/quota.html'
    
    def get_queryset(self):
        queryset = self.model.objects.all()
        
        if(self.request.user.is_marketinghead):
            queryset = queryset.filter(
                Q(assigned_to__in=[self.request.user]) |
                Q(created_by=self.request.user)
            )
        request_post = self.request.POST
        if request_post:
            if request_post.getlist('assigned_to'):
                queryset = queryset.filter(
                    assigned_to__id__in=request_post.getlist('assigned_to')
                )
            return queryset.distinct()
        
       
    def get_context_data(self, **kwargs):
        context = super(AssignQuotaListView, self).get_context_data(**kwargs)
        context['assign_obj_list'] = self.get_queryset()
        context['assignedto_list'] = [
            int(i) for i in self.request.POST.getlist('assigned_to',[]) if i
        ]
        search = False
        if(
            self.request.POST.get(
                'email'
            ) or self.request.POST.get('assigned_to')
        ):
            search = True
        context['search'] = search
        return context
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    

class CreateAssignQuota(LoginRequiredMixin, CreateView):
    model = AssignQuota
    form_class = AssignQuotaForm
    template_name = 'quota/create_quota.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_marketinghead:
            self.users = User.objects.filter(is_active=True).order_by('email')
        else:
            self.users = User.objects.filter(is_marketinghead=True).order_by('email')
        return super(CreateAssignQuota, self).dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super(CreateAssignQuota, self).get_form_kwargs()
        if self.request.user.is_marketinghead:
            self.users = User.objects.filter(is_active=True).order_by('email')
            kwargs.update({"assigned_to": self.users})
        return kwargs
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            assign_quota_obj = form.save(commit=False)
            assign_quota_obj.created_by = self.request.user
            assign_quota_obj.save()
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        # assign_quota_obj = form.save(commit=False)
        # if self.request.POST.getlist('assigned_to', []):
        #     assign_quota_obj.assigned_to.add(*self.request.POST.getlist('assigned_to'))
        
      
                        
        #assigned_to_list = list(assign_quota_obj.assigned_to.all().values_list('id', flat=True))
        current_site = get_current_site(self.request)
        
        if self.request.is_ajax():
            return JsonResponse({'error': False})

        if self.request.POST.get("savenewform"):
            return redirect("marketing_head:assign_quota")
        
        return redirect("marketing_head:assign_list")
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'quota_errors': form.errors
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
        
    def get_context_data(self, **kwargs):
        context = super(CreateAssignQuota, self).get_context_data(**kwargs)
        context['quota_form'] = context['form']
        context['users'] = self.users
        context['assignedto_list'] = [
            int(i) for i in self.request.POST.getlist('assigned_to', []) if i
        ]
        return context


class AssignQuotaDetailView(LoginRequiredMixin, DetailView):
    model = AssignQuota 
    context_object_name = 'quota_record'
    template_name = "quota/quota_detail.html"
    
    def get_object(self):
        obj = super().get_object
        if self.request.user.is_marketinghead:
            AssignQuota.objects.get_or_create(user=self.request.user)
        
        return obj
    
    def get_context_data(self, **kwargs):
        context = super(AssignQuotaDetailView, self).get_context_data(**kwargs)
        user_assign_list = [
            assigned_to.id for assigned_to in context['object'].assigned_to.all()
        ]
        user_assigned_accounts = set(self.request.user.account_assigned_users.values_list('id', flat=True))
        if user_assigned_accounts.intersection(contact_accounts):
            user_assign_list.append(self.request.user.id)
        
        if self.request.user == context['object'].created_by:
            user_assign_list.append(self.request.user.id)
        
        assigned_data = []
        for each in context['quota_record'].assigned_to.all():
            assigned_dict = {}
            assigned_dict['id'] = each.id
            assigned_dict['name'] = each.email
            assigned_data.append(assigned_dict)
        
        if self.request.user.is_marketinghead:
            users_mention = list(User.objects.filter(is_active=True).values('last_name'))
        elif self.request.user != context['object'].created_by:
            users_mention   = [{'last_name': context['object'].created_by.last_name}]
        else:
            users_mention = list(context['object'].assigned_to.all().values('last_name'))
            
        context.update({
            "assigned_data": json.dumps(assigned_data),
            'users_mention': user_mention,
        })
        
        return context

class AssignQuotaUpdateView(LoginRequiredMixin, UpdateView):
    model = AssignQuota
    form_class = AssignQuotaForm
    tempalte_name = "quota/create_quota.html"
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_marketinghead:
            self.users = User.objects.filter(is_marketinghead=True).order_by('email')
        else:
            self.users = User.objects.filter(is_marketinghead=True).order_by('email')
        return super(AssignQuotaUpdateView, self).dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super(AssignQuotaUpdateView, self).get_form_kwargs()
        if self.request.user.is_marketinghead:
            self.users = User.objects.filter(is_active=True).order_by('email')
            kwargs.update({'assigned_to': self.users})
        return kwargs
    
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            assign_quota_obj = form.save(commit=False)
            assign_quota_obj.save()
            return self.form_valid(form)
    
    def form_valid(self, form):
        assigned_to_ids = self.get_object().assigned_to_all().values_list('id', flat=True)
        assign_quota_obj = form.save(commit=False)
        previous_assigned_to_users = list(assign_quota_obj.assigned_to.all().values_list('id', flat=True))
        all_members_list = []
        if self.request.POST.getlist('assigned_to', []):
            current_site = get_current_site(self.request)
            assigned_form_users = form.cleaned_data.get(
                'assigned_to'
            ).values(list('id', flat=True))
            all_members_list = list(
                set(list(assigned_form_users)) - set(list(assigned_to_ids))
            )
            assign_quota_obj.assigned_to.clear()
            assign_quota_obj.assigned_to.add(
                *self.request.POST.getlist('assigned_to')
            )
        else:
            assign_quota_obj.assigned_to.clear()
        
        current_site = get_current_site(self.request)
        assigned_to_list = list(assign_quota_obj.assigned_to.all().values_list('id', flat=True))
        recipients = list(set(assigned_to_list) - set(previous_assigned_to_users))

        def get_context_data(self, **kwargs):
            context = super(AssignQuotaUpdateView, self),get_context_data(**kwargs)
            context['assign_quota_obj'] = self.object
            user_assign_list = [
                assigned_to.id for assigned_to in context['assign_quota_obj'].assigned_to.all()
            ]
            if self.request.user == context['assign_quota_obj'].created_by:
                user_assign_list.append(self.request.user.id)
            
            
            context['quota_form'] = context['form']
            context['users'] = self.users
            context['assignedto_list'] = [
                int(i) for i in self.request.POST.getlist('assigned_to', []) if i
            ]
            return context
            
# def create_assign_quota(request):
#     if request.method == 'POST':
#         form = AssignQuotaForm(request.POST or None)

#         if form.is_valid():
            
#             user_profile        = form.cleaned_data['user_profile']
#             a_senior_high       = form.cleaned_data['a_senior_high']
#             a_higher_education  = form.cleaned_data['a_higher_education']
#             a_retail            = form.cleaned_data['a_retail']
#             a_corporate         = form.cleaned_data['a_corporate']
#             a_owwa              = form.cleaned_data['a_owwa']

#             form = AssignQuota(
                
#                 user_profile        = user_profile,
#                 a_senior_high       = a_senior_high,
#                 a_higher_education  = a_higher_education,
#                 a_retail            = a_retail,
#                 a_corporate         = a_corporate,
#                 a_owwa              = a_owwa,
                

#             )
            

#             form.save()

#             messages.success(request, 'You Have Successfully Assign Quota')
#             return redirect('marketing_head:assign_list')
#     else:
#         form  = AssignQuotaForm()

        

#     template_name = 'quota/create_quota.html'
#     context = {
#         'form': form,
  
#     }
    
#     return render(request, template_name, context)

''' Territory '''

def assign_territory(request):
    if request.method == 'POST':
        form = AssignTerritoryForm(request.POST or None)

        if form.is_valid():

            user_profile        = form.cleaned_data['user_profile']
            territory_choices   = form.cleaned_data['territory_choices']

    

            form = AssignTerritory(
                user_profile        = user_profile,
                territory_choices   = territory_choices,
            )

            form.save()
            messages.success(request, 'You Have Successfully Assigned Territory')
            return redirect('marketing_head:assign_list')
    else:
        form = AssignTerritoryForm()

    template_name = 'territory/territory.html'
    territory = AssignTerritory.objects.all()
    context = {
        'form': form,
        'territory': territory
    }
    return render(request, template_name, context)



def create_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            
             amount   = form.cleaned_data['amount']
             arrival  = form.cleaned_data['arrival']
             
        create = Budget(
            amount=amount,
            arrival=arrival,
        )
        
        create.save()
        messages.success(request, 'You Have Successfully Added Budget Details' )
        return redirect('marketing_head:budget_list')
    
    else:
        form = BudgetForm()
    
    template_name = 'budget/create_budget.html'
    context = {
        'form':form
    }
    
    return render(request, template_name, context)



class BudgetListView(ListView):
    model           = Budget
    template_name   = 'budget/budget_list.html'
    queryset        = Budget.objects.all()
    

class BudgetDetailView(DetailView):
    model           = Budget
    template_name   = 'budget/budget_detail.html'
    

class BudgetUpdateView(UpdateView):
    model  = Budget 
    template_name = 'budget/create_budget.html'
    form_class = BudgetForm 
    success_url = reverse_lazy('marketing_head:budget_list')
    
    
    def form_valid(self, form):
        form.save()
        messages_text = 'Your {} was Updated Successfully!'.format(form.instance)
        messages.success(self.request, message_text)
        if 'continue' in self.request.POST:
            return HttpResponseRedirect(
                reverse_lazy(
                    'marketing_head:budget_update',
                    kwargs={'pk': form.instance.pk}         
                             )
            )
        
        else:
            return super().form_valid(form)    
        
        
def create_collateral(request):
    if request.method == 'POST':
        form = CollateralForm(request.POST)
        if form.is_valid():
            name     = form.cleaned_data['name']
            unit     = form.cleaned_data['unit']
            quantity = form.cleaned_data['quantity']

        create = Collateral(
            name=name,
            unit=unit,
            quantity=quantity,
        )

        create.save()
        messages.success(request, 'You Have Successfully Added Collateral Details')
        return redirect('marketing_head:collateral_list')
    else:
        form = CollateralForm()

    template_name = 'collateral/create_collateral.html'
    context = {
        'form': form
    }
    return render(request, template_name, context)


class CollateralListView(ListView):
    model = Collateral
    template_name = 'collateral/collateral_list.html'
    queryset = Collateral.objects.all()


class CollateralDetailView(DetailView):
    model = Collateral
    template_name = 'collateral/collateral_detail.html'


class CollateralUpdateView(UpdateView):
    model = Collateral
    template_name = 'collateral/create_collateral.html'
    form_class = CollateralForm
    success_url = reverse_lazy('marketing_head:collateral_list')

    def form_valid(self, form):
        form.save()
        messages_text = 'Your {} was Updated Successfully!'.format(
            form.instance)
        messages.success(self.request, message_text)
        if 'continue' in self.request.POST:
            return HttpResponseRedirect(
                reverse_lazy(
                    'marketing_head:collateral_update',
                    kwargs={'pk': form.instance.pk}
                )
            )
        else:
            return super().form_valid(form)


