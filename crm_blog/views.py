from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from centermanager.models import TargetSheet

@login_required
def blog_home_view(request):
    template_name = 'overview/overview.html' #will direct in this page after login
    
    return render(request, template_name, {'title': 'Home'})




class ViewTargetListView(ListView):
    model = TargetSheet
    template_name = 'target/view_target_list.html'  
    queryset = TargetSheet.objects.all()
    
    
