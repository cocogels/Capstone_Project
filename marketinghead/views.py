import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View)
from django.urls import reverse
from django.db.models import Q
from django.template.loader import render_to_string
from marketinghead.models import Budget, Collateral, AssignQuota, AssignTerritory
from centermanager.models import TargetSheet
from marketinghead.forms import BudgetForm, CollateralForm, AssignQuotaForm, AssignTerritoryForm
from accounts.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Sum


def budget_request(request):
    return render(request, 'budget/budget_request.html')

def collateral_request(request):
    return render(request, 'collateral/collateral_request.html')
#-------------------------------------------------------------------

class AssignQuotaListView(LoginRequiredMixin, TemplateView):
    model = AssignQuota
    context_object_name = 'assign_obj_list'
    template_name = 'quota/quota_list.html'

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
        quota = AssignQuota.objects.all()
        context['quota'] = quota
        target = TargetSheet.objects.all()
        context['targetsheet'] = target

        context['assignedto_list'] = [
            int(i) for i in self.request.POST.getlist('assigned_to', []) if i
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
    context_object_name = 'assign_list'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_marketinghead:
            self.users = User.objects.filter(is_active=True).order_by('email')
        else:
            self.users = User.objects.filter(
                is_marketinghead=True).order_by('email')
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
        assign_quota_obj = form.save(commit=False)
        if self.request.POST.getlist('assigned_to', []):
            assign_quota_obj.assigned_to.add(*self.request.POST.getlist('assigned_to'))

        assigned_to_list = list(assign_quota_obj.assigned_to.all().values_list('id', flat=True))
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
                    'error': True,
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
        context['assign_list'] = self.get_queryset()
        quota = AssignQuota.objects.all()
        context['quota_list'] = quota
        target = TargetSheet.objects.all()
        context['targetsheet'] = target

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
        user_assigned_accounts = set(
            self.request.user.account_assigned_users.values_list('id', flat=True))
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
            users_mention = list(User.objects.filter(
                is_active=True).values('last_name'))
        elif self.request.user != context['object'].created_by:
            users_mention = [
                {'last_name': context['object'].created_by.last_name}]
        else:
            users_mention = list(
                context['object'].assigned_to.all().values('last_name'))

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
            self.users = User.objects.filter(
                is_marketinghead=True).order_by('email')
        else:
            self.users = User.objects.filter(
                is_marketinghead=True).order_by('email')
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
        assigned_to_list = list(
            assign_quota_obj.assigned_to.all().values_list('id', flat=True))
        recipients = list(set(assigned_to_list) -
                          set(previous_assigned_to_users))

        def get_context_data(self, **kwargs):
            context = super(AssignQuotaUpdateView,
                            self), get_context_data(**kwargs)
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


''' Territory '''


class TerritoryListView(TemplateView):
    model = AssignTerritory
    context_object_name = 'assign_territory_obj'
    template_name = 'territory/territory.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        queryset = queryset.filter(
            Q(assigned_to__in=[self.request.user]) |
            Q(created_by=self.request.user)
        )

        request_post = self.request.POST
        if request_post:
            if request_post.get('user_profile'):
                queryset = queryset.filter(
                    user_profile__icontains=request_post.get('user_profile')
                )

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(TerritoryListView, self).get_context_data(**kwargs)
        context['assign_territory_obj'] = self.get_queryset()
        context['per_page'] = self.request.POST.get('per_page')
        context['users'] = User.objects.filter(
            is_active=True
        ).order_by('last_name')

        context['assignedto_list'] = [
            int(i) for i in self.request.POST.getlist('assigned_to', []) if i
        ]

        search = False
        if (
            self.request.POST.get('user_profile')
        ):
            search = True
        context['search'] = search
        return context

    def post(self, request, *args, **kawrgs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class TerritoryAssign(CreateView):
    model = AssignTerritory
    form_class = AssignTerritoryForm
    template_name = 'territory/territory.html'

    def get_form_kwargs(self):
        kwargs = super(TerritoryAssign, self).get_form_kwargs()
        self.users = User.objects.filter(is_active=True).order_by('email')
        kwargs.update({'assigned_to': self.users})
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            assign_territory_obj = form.save(commit=False)
            assign_territory_obj.created_by = self.request.user
            assign_territory_obj.save()

            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        assign_territory_obj = form.save(commit=False)
        if self.request.POST.getlist('assigned_to', []):
            assign_territory_obj.assigned_to.add(
                *self.request.POST.getlist('assigned_to')
            )

        assigned_to_list = list(
            assign_territory_obj.assigned_to.all().values_list('id', flat=True))
        current_site = get_current_site(self.request)

        if self.request.is_ajax():
            return JsonResponse({{'error': False}})

        if self.request.POST.get('savenewform'):
            return redirect('marketing_head:add_territory')
        return redirect('marketing_head:add_territory')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error': True,
                    'requirements_errors': form.errors
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
    
    def get_context_data(self, **kwargs):
        context = super(TerritoryAssign, self).get_context_data(**kwargs)
        territory = AssignTerritory.objects.all()
        context['territory_form'] = context['form']
        context['territory'] = territory
        context['users'] = self.users
        context['assignedto_list'] = [
            int(i) for i in self.request.POST.getlist('assigned_to', [])
        ]
        
        return context


class TerritoryUpdateView(UpdateView):
    model = AssignTerritory
    form_class = AssignTerritoryForm
    template_name = 'territory/territory_create.html'
    
    def get_form_kwargs(self):
        kwargs = super(TerritoryUpdateView, self).get_form_kwargs()
        self.users = User.objects.filter(is_active=True).order_by('email')    
        kwargs.update({'assigned_to': self.users})
        return kwargs
        
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            assign_territory_obj = form.save(commit=False)
            assign_territory_obj.save()
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        assigned_to_ids = self.get_object().assigned_to.all().values_list('id', flat=True)
        assign_territory_obj = form.save(commit=False)
        messages_text = 'Your {} was Updated Successfully!'.format(form.instance)
        messages.success(self.request, message_text)
        previous_assigned_to_users = list(assign_territory_obj.assigned_to.all().values_list('id', flat=True))
        all_members_list = []
        if self.request.POST.getlist('assigned_to', []):
            current_site = get_current_site(self.request)
            assigned_form_users = form.cleaned_data.get(
                'assigned_to'
            ).values_list('id', flat=True)
            all_members_list = list(
                set(list(assigned_form_users)) - set(list(assigned_to_ids))
            )
            assign_territory_obj.assigned_to.clear()
            assign_territory_obj.assigned_to.add(
                *self.request.POST.getlist('assigned_to')
            )
        else:
            assign_territory_obj.assigned_to.clear()

        current_site = get_current_site(self.request)
        assigned_to_list = list(assign_territory_obj.assigned_to.all().values_list('id', flat=True))
        
        if self.request.is_ajax():
            return JsonResponse({
                'error': False
            })
        return redirect('marketing_head:a_list')
    
    def form_invalid(self, **kwargs):
        if self.request.os_ajax():
            return JsonResponse(
                {
                    'error': True,
                    'territory_errors': form.errors,
                }
            )
            return self.render_to_response(
                self.get_context_data(form=form)
            )
    def get_context_data(self, **kwargs):
        context = super(TerritoryUpdateView, self).get_context_data(**kwargs)
        context['territory_obj'] = self.object
        user_assign_list = [
            assigned_to.id for assigned_to in context['territory_obj'].assigned_to.all()
        ]
        if self.reqest.user == context['territory_obj'].created_by:
            user_assign_list.append(self.request.user.id)
            
        context['territory_form'] = context['form']
        context['users'] = self.users
        context['assignedto_list'] = [
            int(i) for i in self.request.POST.getlist('assigned_to', []) if i
        ]   

        return context
    
""" BUDGET VIEWS """


class BudgetListView(TemplateView):
    model = Budget
    context_object_name = 'budget_list_obj'
    template_name = 'budget/budget_list.html'
    
    def get_queryset(self):
        queryset = self.model.objects.all()
        queryset = queryset.filter(
            Q(created_by=self.request.user)
        )
        
        request_post = self.request.POST
        if request_post:
            if request_post.getlist('arrival'):
                queryset = querset.filter(
                    arrival_icontains=request_post.getlist(arrival)
                )
                
            return queryset.distinct()
        
    def get_context_data(self, **kwargs):
        context = super(BudgetListView, self).get_context_data(**kwargs)
        context['budget_list_obj'] = self.get_queryset()
        budget = Budget.objects.all()
        context['budget'] = budget
        search = False
        if(
            self.request.POST.get(
                'arrival'
            ) 
        ):
            search = True
        context['search'] = search
    
        return context
    
    def post(self, request,*args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budget/create_budget.html'
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            budget_obj = form.save(commit=False)
            budget_obj.created_by = self.request.user
            budget_obj.save()
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        budget_obj = form.save(commit=False)
        current_site = get_current_site(self.request)
        
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':False
                }
            )
        if self.request.POST.get('savenewform'):
            return redirect("marketing_head:budget")
        return redirect('marketing_head:budget_list')
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'budget_errors': form.errors
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
        
    def get_context_data(self, **kwargs):
        context = super(BudgetCreateView, self).get_context_data(**kwargs)
        context['budget_form'] = context['form']
        budget = Budget.objects.all()
        context['budget_list'] = budget
        # budget_total = Budget.objects.all().aggregate(Sum('amount'))
        context['budget_total'] = Budget.objects.all().aggregate(Sum('amount'))
        return context
    

class BudgetDetailView(DetailView):
    model               =  Budget
    context_object_name = 'budget_record'
    template_name       = 'budget/budget_detail.html'
    
   
    def get_queryset(self):
        queryset = super(BudgetDetailView, self).get_queryset()
        return queryset.select_related('arrival')
    
    def get_context_data(self, **kwargs):
        context = super(BudgetDetailView, self).get_context_data(**kwargs)
        context['budget_record'] = self.object 
        context['users'] = self.users
        return context 
        
                   
class BudgetUpdateView(UpdateView):
    model  = Budget 
    form_class = BudgetForm 
    template_name = 'budget/create_budget.html'
 
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            budget_obj = form.save(commit=False)
            budget_obj.save()
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        budget_obj = form.save(commit=False)
        messages_text = 'Your {} was Updated Successfully!'.format(form.instance)
        messages.success(self.request, messages_text)
        currrent_site = get_current_site(self.request)
        
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error': False,
                }
            )
            
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'budget_errors': form.errors
                }
            )
        return self.render_to_response(
            self.get_context_data(form=form)
        )
    
    def get_context_data(self, **kwargs):
        context = super(BudgetUpdateView, self).get_context_data(**kwargs)
        context['budget_obj'] = self.object
        context['users'] = self.users_mention
        context['budget_form'] = context['form']
        
        return context
    
        

""" Colateral Views """

class CollateralListView(TemplateView):
    model = Collateral
    context_object_name = "collateral_obj_list"
    template_name = 'collateral/collateral_list.html'
    
    def get_queryset(self):
        queryset = self.model.objects.all()
        
        request_post = self.request.POST
        if request_post:
            if request_post.get('name'):
                queryset = queryset.filter(
                    name__icontains=request.post.get('name')
                )
            
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super(CollateralListView, self).get_context_data(**kwargs)
        context['collateral_obj_list'] = self.get_queryset()
        collateral = Collateral.objects.all()
        context['collateral'] = collateral
        context['per_page'] = self.request.POST.get('per_page')
        
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
    

class CollateralCreateView(CreateView):
    model = Collateral
    form_class = CollateralForm
    template_name = 'collateral/create_collateral.html'
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            collateral_obj = form.save(commit=False)
            collateral_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    
    def form_valid(self, form):
        collateral_obj = form.save(commit=False)
        current_site = get_current_site(self.request)
        
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':False,
                }
            )
        
        if self.request.POST.get("savenewform"):
            return redirect('marketing_head:create_collateral')

        return redirect('marketing_head:collateral_list')
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error': True,
                    'collateral_errors': form.errors
                }
            )
        
        return self.render_to_response(
            self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super(CollateralCreateView, self).get_context_data(**kwargs)
        context['collateral_form'] = context['form']
        context['collateral_obj_list'] = self.get_queryset()
        collateral = Collateral.objects.all()
        context['collateral_list'] = collateral
        
        return context
    
            
class CollateralDetailView(DetailView):
    model = Collateral
    context_object_name = 'collateral_record'
    template_name = 'collateral/collateral_detail.html'
    
    def get_queryset(self):
        queryset = super(CollateralDetailView, self).get_queryset()
        return queryset.select_related('name')
    
    def get_context_data(self, **kwargs):
        context = super(CollateralDetailView, self).get_context_data(**kwargs)
        context['collateral_record'] = self.object 
        
        return context
    

class CollateralUpdateView(UpdateView):
    model = Collateral
    form_class = CollateralForm
    template_name = 'collateral/create_collateral.html'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            collateral_obj = form.save(commit=False)
            collateral_obj.save()
            
            return self.form_valid(form)
        return self.form_invalid(form)
    
    
    def form_valid(self, form):
        collateral_obj = form.save(commit=False)
        messages_text = 'Your {} was Updated Successfully!'.format(form.instance)
        messages.success(self.request, message_text)
        current_site = get_current_site(self.request)
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':False,
                }
            )
        return redirect('marketing_head:collateral_list')
    
    def form_invalid(self, form):
        
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error':True,
                    'collateral_errors': form.errors,
                }
            )         
            
        return self.render_to_response(
            self.get_context_data(form=form)
        )
        
    def get_context_data(self, **kwargs):
        context = super(CollateralUpdateView, self).get_context_data(**kwargs)
        context['collateral_obj'] = self.object
        context['collateral_form'] = context['form']
        
        return context
        
        
    
    # def form_valid(self, form):
    #     form.save()
    #     messages_text = 'Your {} was Updated Successfully!'.format(
    #         form.instance)
    #     messages.success(self.request, message_text)
    #     if 'continue' in self.request.POST:
    #         return HttpResponseRedirect(
    #             reverse_lazy(
    #                 'marketing_head:collateral_update',
    #                 kwargs={'pk': form.instance.pk}
    #             )
    #         )
    #     else:
    #         return super().form_valid(form)


