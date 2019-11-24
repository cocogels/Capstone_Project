
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, ListView)
from django.urls import reverse
from django.db.models import Q
from django.template.loader import render_to_string
from centermanager.models import TargetSheet, SchoolYear
from accounts.models import User
from centermanager.forms import TargetSheetForm,SchoolYearForm
from datetime import date, timedelta
from django.contrib import messages

from centermanager.filterset import SchoolYearFilter
''' Target Sheet View '''



class TargetSheetListView(TemplateView):
    context_object_name = 'target_sheet_obj'
    template_name = 'target_sheet/targetsheet_list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.users = User.objects.filter(is_active=True).order_by('email')
        return super(TargetSheetListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = TargetSheet.objects.all()
        start = date.today()
        end   = date.today() + timedelta(days=365)
        queryset = queryset.filter(
            Q(active_year__start_year__lte=start)|
            Q(active_year__end_year__lte=end)
        )
    
    
    def get_context_data(self, **kwargs):
        context = super(TargetSheetListView, self).get_context_data(**kwargs)
        context['target_sheet_obj'] = self.get_queryset()
        context['filter'] = SchoolYearFilter(self.request.GET, queryset=self.get_queryset())
        context['per_page'] = self.request.POST.get('per_page')
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
    
    
    
    
    def post(self, request, *args, **kwargs,):
        self.object = None
        school_year = SchoolYear.objects.get(active_year=True)
        form = TargetSheetForm(request.POST, instance=school_year)
        if form.is_valid():
            target_sheet_obj = form.save(commit=False)
            target_sheet_obj.save()
            
            
            return self.form_valid(form)
        return self.form_invalid(form)

            
    def form_valid(self, form):
        form.instance.active_year_id = SchoolYear.objects.get(active_year=True)
        target_sheet_obj = form.save()
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error': False,
                }
            )
        return redirect('centermanager:create_target')
        return super(TargetSheetCreateView, self).form_valid(form)

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
