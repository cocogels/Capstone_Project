from django.shortcuts import render, redirect

from django.contrib import messages

from django.contrib.auth import  authenticate

from django.contrib.auth.decorators import login_required

from .admin import MarketingAdminUserCreationForm

from .forms import UserRegistrationForm, UserLoginForm

from .models import UserMarketingProfile

from django.urls import reverse





def user_registration(request):
    
    if request.method == 'POST':
        form = MarketingAdminUserCreationForm(request.POST)
        
        if form.is_valid():            
            form.save()
            messages.success(request, 'You Have Successfuly Registered User Account..!!')
            return redirect('accounts:register')
        else:
            messages.error(request, 'Account Registration Failed Try Again..!!!')
            return redirect('accounts:register')
    else:
        form = MarketingAdminUserCreationForm()
    template_name = 'registration/register.html'
    context = {
        "form":form
    }
    return render(request, template_name, context)
    
