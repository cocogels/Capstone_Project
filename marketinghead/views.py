from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView 

from .models import Budget, Collateral, AssignQuota, AssignTerritory
from .forms  import BudgetForm, CollateralForm, AssignQuotaForm, AssignTerritoryForm



def create_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        
        if form.is_valid():
            
             arrival  = form.cleaned_data['arrival']
             amount   = form.cleaned_data['amount']
             
        
        create = Budget(
            amount=amount,
            arriva=arrival,
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
        
        
    
    


def create_assign_quota(request):
    if request.method == 'POST':
        form = AssignQuotaForm(request.POST or None)

        if form.is_valid():
            
            user_profile        = form.cleaned_data['user_profile']
            a_senior_high       = form.cleaned_data['a_senior_high']
            a_higher_education  = form.cleaned_data['a_higher_education']
            a_retail            = form.cleaned_data['a_retail']
            a_corporate         = form.cleaned_data['a_corporate']
            a_owwa              = form.cleaned_data['a_owwa']

            form = AssignQuota(
                
                user_profile        = user_profile,
                a_senior_high       = a_senior_high,
                a_higher_education  = a_higher_education,
                a_retail            = a_retail,
                a_corporate         = a_corporate,
                a_owwa              = a_owwa,
                

            )
            

            form.save()

            messages.success(request, 'You Have Successfully Assign Quota')
            return redirect('marketing_head:assign_list')
    else:
        form  = AssignQuotaForm()

        

    template_name = 'quota/create_quota.html'
    context = {
        'form': form,
  
    }
    
    return render(request, template_name, context)



class AssignQuotaListView(ListView):
    model = AssignQuota
    template_name = 'quota/quota_list.html'
    queryset = AssignQuota.objects.all()


class QuotaUpdateView(UpdateView):
    model = Budget
    template_name = 'quota/create_quota.html'
    form_class = BudgetForm
    success_url = reverse_lazy('marketing_head:quota_list')

    def form_valid(self, form):
        form.save()
        messages_text = 'Your {} was Updated Successfully!'.format(
            form.instance)
        messages.success(self.request, message_text)
        if 'continue' in self.request.POST:
            return HttpResponseRedirect(
                reverse_lazy(
                    'marketing_head:quota_update',
                    kwargs={'pk': form.instance.pk}
                )
            )

        else:
            return super().form_valid(form)


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
