

import json

from datetime import date, timedelta
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from centermanager.models import SanctionSetting
from centermanager.forms import SanctionSettingForm
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, ListView)
from django.urls import reverse
from django.db.models import Q
from django.template.loader import render_to_string
from accounts.models import User
from django.views.generic.dates import YearMixin, DateMixin
from centermanager.forms import EmployeeRegistrationForm




'''  SANCTION SETTING '''


class SanctionSettingListView(TemplateView):
    model = SanctionSetting
    context_object_name = 'sanction_obj_list'
    template_name = 'sanction/sanction_list.html'

    def get_queryset(self):
        queryset = SanctionSetting.objects.all()

    def get_context_data(self, **kwargs):
        context = super(SanctionSettingListView,self).get_context_data(**kwargs)
        context['sanction_obj_list'] = self.get_queryset()
        context['per_page'] = self.request.POST.get('per_page')
        
        sanction = SanctionSetting.objects.all()
        context['sanction_list'] = sanction
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

    def post(self,*args, **kwargs):
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
                    'error': False,
                }
            )

        return redirect('centermanager:sanction_list')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error': True,
                    'sanction_errors': form.errors
                }
            )

        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def def_context_data(self, **kwargs):
        context = super(SanctionSettingCreateView,self).get_context_data(**kwargs)
        context['sanction_form'] = context['form']
        return context


class SanctionSettingDetailView(DetailView):
    model = SanctionSetting
    context_object_name = 'sanction_record'
    template_name = 'sanction/sanction_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SanctionSettingDetailView,
                        self).get_context_data(**kwargs)
        return context


class SanctionSettingUpdateView(UpdateView):
    model = SanctionSetting
    form_class = SanctionSettingForm
    template_name = 'sanction/create_sanction.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.is_centermanager:
            self.users = User.objects.filter(is_active=True).order_by('email')
        else:
            self.users = User.objects.filter(
                is_centermanager=True).order_by('email')
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
                    'error': False,
                }
            )
        return redirect('centermanager:sanction_list')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'error': True,
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
