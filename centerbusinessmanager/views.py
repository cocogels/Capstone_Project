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
#from centermanager.forms import SchoolYearForm
from datetime import date, timedelta
from django.contrib import messages
from django.views.generic.dates import YearArchiveView
from centermanager.forms1 import YearSelectForm
from django.forms.models import model_to_dict
from centermanager.mixins import AjaxFormMixin
from django.http import HttpResponse, JsonResponse

''' activity '''
def activity_detailed(request):
    return render(request, 'detailed.html')
    
def activity_pending(request):
    return render(request, 'pending.html')


