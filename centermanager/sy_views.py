import json
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, ListView)
from django.urls import reverse
from django.db.models import Q
from django.template.loader import render_to_string
from centermanager.models import SchoolYear
from accounts.models import User
from centermanager.forms import SchoolYearForm
from datetime import date, timedelta
from django.contrib import messages
from django.views.generic.dates import YearArchiveView
from centermanager.forms1 import YearSelectForm
from django.forms.models import model_to_dict
from centermanager.mixins import AjaxFormMixin
from django.http import JsonResponse
''' School Year Views '''


class SchoolYearCreateView(AjaxFormMixin, CreateView):
    model = SchoolYear
    form_class = SchoolYearForm
    template_name = 'target_sheet/create_target.html'

    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_centermanager:
            self.users = User.objects.filter(is_active=True).order_by('email')
        else:
            self.users = User.objects.filter(
                is_centermanager=True).order_by('email')
        return super(SchoolYearCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = SchoolYearForm(request.POST)
        if form.is_valid():
            school_year_obj = form.save(commit=False)
            school_year_obj.save()
            return self.form_valid(form)
        return self.form_invalid(form)

            
    def form_valid(self, form):
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
        context = super(SchoolYearCreateView, self).get_context_data(**kwargs)
        context['school_year_form'] = context['form']
        school_year = SchoolYear.objects.all()
        return context



class SchoolYearListView(ListView):
    model = SchoolYear
    template_name = 'school_year/school_year.html'
    context_object_name = 'school_year_list'
    
    def get_queryset(self):
        queryset = super(SchoolYearListView, self).get_queryset()
        queryset = self.model.objects.all()

        request_post = self.request.POST
        if request_post:
            if request_post.get('start_year'):
                queryset = queryset.filter(
                    start_year__icontains=request_post.get('start_year')
                )
            if request_post.get('end_year'):
                queryset = queryset.filter(
                    end_year__icontains=request_post.get('end_year')
                )
            
        return queryset.distinct()
    
    

    def get_context_data(self, **kwargs):
        context = super(SchoolYearListView, self).get_context_data(**kwargs)
        context['school_year_list'] = self.get_queryset()
    
        search = False
        if(
            self.request.POST.get('start_year') or
            self.request.POST.get('end_year')
        ):
            search = True
            
        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
    
    
    
class SchoolYearArchiveView(YearArchiveView):
    date_field = 'date_created'
    allow_future = False
    template_name = 'target_sheet/target_details.html'
    
    
    def get_context_data(self, **kwargs):
        
        now = date.today
        school_year = SchoolYear.objects.all()        
        context['school_year'] = shool_yeacr
        return super(SchoolYearArchiveView, self).get_context_data(**kwargs)


