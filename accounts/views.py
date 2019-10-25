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

from .forms import UserUpdateForm, ProfileUpdateForm, EmployeeCreationForm, ChangePasswordForm



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user_obj'] = self.request.user
        return context
    
    
class UsersListView(LoginRequiredMixin, TemplateView):
    model = User
    context_object_name = 'users'
    template_name = 'registration/register_list.html'

    def get_queryset(self):
        queryset = self.model.objects.all()

        request_post = self.request.POST
        if request_post:
            if request_post.get('email'):
                queryset = queryset.filter(
                    email__icontains=request_post.get('email')
                )

        return queryset.order_by('email')

    def get_context_data(self, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        active_users = self.get_queryset().filter(is_active=True)
        inactive_users = self.get_queryset().filter(is_active=False)
        context['active_users'] = active_users
        context['inactive_users'] = inactive_users
        context['per_page'] = self.request.POST.get('per_page')
        context['status'] = [
            ('True', ' Active'),
            ('False', 'In Active')
        ]
        context['user_obj_list'] = User.objects.all()
        return context
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CreateUserView(LoginRequiredMixin, CreateView):
    model = User
    form_class = EmployeeCreationForm
    template_name = 'registration/register.html'

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        user = form.save(commit=False)
        ''' Send Email To The New User to be followed'''
        # current_site = self.request.get_host()
        # protocol = self.request.scheme
        # send_email_to_new_user.delay(
        #     user.email,
        #     self.request.user.email,
        #     domain=current_site,
        #     protocol=protocol
        #     )

        if self.request.is_ajax():
            data = {
                'success_url': reverse_lazy(
                    'acccounts:users_list'
                ),
                'error': False
            }
            return JsonResponse(data)
        return super(CreateUserView, self).form_valid(form)

    def form_invalid(self, form):
        response = super(CreateUserView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(data)
        return response
    
    # def get_form_kwargs(self):
    #     kwargs = super(CreateUserView, self).get_form_kwargs()
    #     kwargs.update({"request_user": self.request.user})
    #     return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(CreateUserView, self).get_context_data(**kwargs)
        context['user_form'] = context['form']
        context['user_list'] = User.objects.all()
        if 'errors' in kwargs:
            context['errors'] = kwargs['errors']
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'users'
    template_name = 'user_detail.html'

    
    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user_obj = self.object 
        users_data = []
        
        for each in User.objects.all():
            assigned_dict = {}
            assigned_dict['id'] = each.id 
            assigned_dict['email'] = each.email
            users_data.append(assigned_dict)
        
        context.update({
            "user_obj":user_obj,
            "assigned_territory":AssignTerritory.objects.filter(assigned_to=user_obj.id),
            "assigned_quota":AssignQuota.objects.filter(assigned_to=user_obj.id),
            "assigned_data": json.dumps(users_data),
        })
        
        return context



class UpdateUserView(UpdateView):
    model = User
    form_class = EmployeeCreationForm 
    template_name = 'registration/create.html'


    def form_valid(self, form):
        user = form.save(commit=False)
        if self.request.is_ajax():
            if self.request.user.is_centermanager and not self.request.user.is_superuser:   
                if self.request.user.id != self.object.id:
                    data = {
                        'error_403':True,
                        'error':True
                    }
                    return JsonResponse(data)
        if (self.request.user.is_ihe and 
            self.request.user.is_icl and
            self.request.user.is_shs and
            self.request.user.is_centerbusinessmanager and 
            self.request.user.is_marketinghead and  
            self.request.user.is_registrar and 
            self.request.user.is_budgetary):
            
            user.is_superuser = False
        user.save()
        
        
        
        if (self.request.user.is_centermanager and self.requset.user.is_superuser):
            if self.request.is_ajax():
                data = {'success_url': reverse_lazy(
                    'accounts:users_list'
                ),'error':False}
                return JsonResponse(data)
            return JsonResponse(data)

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'accounts:profile'
            ), 'error':False}
            return JsonResponse(data)
        return super(UpdateUserView, self).form_valid(form)
    
    def form_invalid(self, form):
        response = super(UpdateUserView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({
                'error':True,
                'errors': form.errors
                })
            return response
    
    def get_form_kwargs(self):
        kwargs = super(UpdateUserView, self).get_form_kwargs()
        kwargs.update({
            "request_user": self.request.user
            })
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(UpdateUserView, self).get_context_data(**kwargs)
        context['user_obj'] = self.object
        user_profile_name = str(context['user_obj'].profile_pic).split("/")
        user_profile_name = user_profile_name[-1]
        context['user_profile_name'] = user_profile_name
        CONTEXT['user_form'] = context['form']
        if "errors" in kwargs:
            context['errors'] =kwargs['errors']
        return context


class ChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/change_password.html'
    
    def get_context_data(self, **kwargs):
        context = super(ChangePasswordView, self).get_context_data(**kwargs)
        context['change_password_form'] = ChangePasswordForm()
        return context
    
    def post(self, request, *args, **kwargs):
        error, errors = "",""
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            user.set_password(request.POST.get('Newpassword'))
            user.is_active=True
            user.save()
            return HttpResponseRedirect('/')
        else:
            errors = form.errors
        return render(request, 'registration/change_password.html',
                      {'error': error, 'errors':errors,
                       'change_password_form': form}
                      )








































# def user_registration(request):

#     if request.method == 'POST':
#         form = EmployeeCreationForm(request.POST)
#         if form.is_valid():
#             form = form.save()
#             messages.success(
#                 request, 'You Have Successfuly Registered User Account..!!')
#             return redirect('accounts:register_list')
#         else:
#             messages.error(
#                 request, 'Account Registration Failed Try Again..!!!')
#             return redirect('accounts:register')
#     else:
#         form = EmployeeCreationForm()

#     template_name = 'registration/register.html'

#     context = {
#         "form": form,
#     }
#     return render(request, template_name, context)


# class RegistrationListView(ListView):
#     model = User
#     template_name = 'registration/register_list.html'
#     queryset = all()


# ''' ------------------------------------------------------------------------------ '''


# def user_profile(request):

#     if request.method == 'POST':
#         user_form = UserUpdateForm(request.POST, instance=request.user)
#         profile_form = ProfileUpdateForm(
#             request.POST, instance=request.user.profile)

#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Your Account Has Been Updated..!')
#             return redirect('accounts:profile')
#         else:
#             messages.error(
#                 request, 'Update Profile Information Failed Try Again..!!!')
#             return redirect('accounts:profile')

#     else:
#         user_form = UserUpdateForm()
#         profile_form = ProfileUpdateForm()

#     template_name = 'user/profile.html'
#     context = {
#         'user_form': user_form,
#         'profile_form': profile_form,
#     }

#     return render(request, template_name, context)
