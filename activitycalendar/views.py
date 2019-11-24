from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import datetime
from activitycalendar.models import ActivityCalendar
from activitycalendar.forms import ActivityCalendarForm
from viewflow.flow.views import StartFlowMixin,FlowMixin
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View)
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from bootstrap_datepicker_plus import DatePickerInput
from django.utils.safestring import mark_safe
from rest_framework import generics, permissions
from activitycalendar.serializer import ActivityCalendarSerializer


class ActivityCalendarAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ActivityCalendar.objects.all()
    serializer_class = ActivityCalendarSerializer
    
class ActivityCalendarCreateAPIView(generics.ListCreateAPIView):
    queryset = ActivityCalendar.objects.all()
    serializer_class = ActivityCalendarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
class CalendarTemplateView(TemplateView):
    template_name = 'fullcalendar.html'
    form_class = ActivityCalendarForm
    model = ActivityCalendar

        
    def get_context_data(self, **kwargs):
        context = super(CalendarTemplateView, self).get_context_data(**kwargs)
        context['activity'] = ActivityCalendar.objects.all()
        return context 


class CalendarCreateView(StartFlowMixin, CreateView):
    model = ActivityCalendar
    form_class = ActivityCalendarForm
    
    # def post(self, request, *args, **kwargs):
    #     self.object=None
    #     form = self.get_form()
    #     if form.is_valid():
    #         activity_obj = form.save(commit=False)
    #         activity_obj.created_by = self.request.user
    #         activity_obj.save()
            
    #         return self.form_valid(form)
    #     return self.form_invalid(form)
    
    
    # def form_valid(self, form):
    #     activity_obj = form.save(commit=False)
    #     if self.request.is_ajax():
    #         return JsonResponse(
    #             {
    #                 'error':False
    #             }
    #         )
            
    #     if self.request.POST.get("savenewform"):
    #         return redirect('calendar:add_activity')
    #     return redirect('calendar:calendar_home')
    
    # def form_invalid(self, form):
    #     if self.request.is_ajax():
    #         return JsonResponse(
    #             {
    #                 'error':True,
    #                 'calendar_errors': form.errors
    #             }
    #         )
    #     return self.render_to_response(
    #         self.get_context_data(form=form)
    #     )
        
    # def get_context_data(self, **kwargs):
    #     context = super(CalendarCreateView, self).get_context_data(**kwargs)
    #     context['calendar_form'] = context['form']
    #     return context
    
    def get_object(self):
        return self.activation.process.activity
    
    def activation_done(self, form):
        activitycalendar = form.save()
        self.activation.process.activity = activitycalendar
        super(CalendarCreateView,self).activation_done(form)
        
class CalendarUpdateView(FlowMixin,UpdateView):
    model = ActivityCalendar
    form_class = ActivityCalendarForm
    
    
    # def dispatch(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         activity_obj = form.save(commit=False)
    #         activity_obj.save()
            
    #         return self.form_valid(form)
    #     return self.form_invalid(form)
    
    # def form_valid(self):
    #     if self.request.is_ajax():
    #         return JsonResponse(
    #             {
    #                 'error':False,
    #             }
    #         )
    #     return redirect('calendar:add_activity')
    
    # def form_invalid(self, form):
    #     if self.request.is_ajax():
    #         return JsonResponse(
    #             {
    #                 'error':True,
    #                 'calendar_errors': form.errors
    #             }
    #         )
    #     return redirect('calendar:add_activity')
    
    # def get_context_data(self, **kwargs):
    #     context = super(CalendarUpdateView, self).get_context_data(**kwargs)
    #     context['activity_obj'] = self.object()
    #     context['activity_form'] = context['form']
        
        
class CalendarStartView(StartFlowMixin, UpdateView):
    form_class = ActivityCalendarForm
    

    def get_object(self):
        return self.activation.process.activity
    
    def activation_done(self, form):
        activitycalendar = form.save()
        self.activation.process.activity = activity
        super(CalendarStartView, self).activation_done(form)
        

class CalendarView(FlowMixin,UpdateView):
    
    fields = ['activity_name', 'start_date', 'end_date']

    def get_object(self):
        return self.activation.process.activity


class RevisedView(FlowMixin, CreateView):
    model = ActivityCalendar
    fields = ['activity_name', 'start_date', 'end_date']
    
    def activation_done(self, form):
        activity = self.activation.process.activity
        activity.revised = self.object
        activity.save(update_fields=['revised'])
        self.activation.done


    