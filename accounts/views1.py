from django.shortcuts import render, redirect, get_object_or_404


from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse, Http404, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from accounts.models import User
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.views.generic import (CreateView, DeleteView, DetailView,
    TemplateView, UpdateView, ListView, View)


from marketinghead.models import AssignQuota, AssignTerritory
from centermanager.models import User





class AccountsView(ListView):
    template_name = ''
    paginated_by = 20
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user  = User.objects.all()
        quota = AssignQuota.objects.all()
        territory = AssignTerritory.objects.all()
    
        context["user_list"] = user
        context["quota_list"] = quota
        context['territory_list'] = territory
        return context