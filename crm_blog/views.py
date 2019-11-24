from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from centermanager.models import TargetSheet

@login_required
def blog_home_view(request):
    template_name = 'home.html'
    
    return render(request, template_name, {'title': 'Home'})


