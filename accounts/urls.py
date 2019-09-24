from django.urls import path


from accounts.views import user_registration, user_profile

from . import views

app_name="accounts"

urlpatterns = [
    path('registration-list/', views.RegistrationListView.as_view(),name='register_list'),
    path('registration/', user_registration, name='register'),
    path('user-profile/', user_profile, name='profile' ),
    
]
