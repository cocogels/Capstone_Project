from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.




@login_required
def blog_home_view(request):
    template_name = 'home.html'
    
    return render(request, template_name, {'title': 'Home'})



@login_required
def blog_user_detail_view(request):
    
    template_name = 'user/profile.html'
    
    return render(request, template_name, {'title': 'Profile'})

