from django.shortcuts import render, redirect, get_object_or_404


from django.contrib.auth import  authenticate

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from accounts.models import User

from django.urls import reverse

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


from .forms import UserUpdateForm, ProfileUpdateForm, EmployeeCreationForm




def user_registration(request):
    
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            form  = form.save()
            messages.success(request, 'You Have Successfuly Registered User Account..!!')
            return redirect('accounts:register_list')
        else:
            messages.error(request, 'Account Registration Failed Try Again..!!!')
            return redirect('accounts:register')
    else:
        form = EmployeeCreationForm()

    template_name = 'registration/register.html'

    context = {
        "form":form,  
    }
    return render(request, template_name, context)
    



class RegistrationListView(ListView):
    model = User
    template_name = 'registration/register_list.html'
    queryset = User.objects.all()


''' ------------------------------------------------------------------------------ '''

def user_profile(request):

    if request.method =='POST':
        user_form       = UserUpdateForm(request.POST, instance=request.user)
        profile_form    = ProfileUpdateForm(request.POST,instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Account Has Been Updated..!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Update Profile Information Failed Try Again..!!!')
            return redirect('accounts:profile')
            
    else:
        user_form = UserUpdateForm()
        profile_form = ProfileUpdateForm()

    template_name   = 'user/profile.html'
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    
    return render(request, template_name, context)




