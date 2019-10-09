from django.urls import path


from accounts.views import user_registration, user_profile

from . import views

app_name="accounts"

urlpatterns = [
    path('registration-list/', views.RegistrationListView.as_view(),name='register_list'),
    path('registration/', user_registration, name='register'),
    path('user-profile/', user_profile, name='profile' ),
    
    
    path('add/user/', views.CreateUserView.as_view(), name='create_user'),
    path('user/list/', views.UsersListView.as_view(), name='user_list'),
    path('user/<int:pk>/detail', views.UserDetailView.as_view(), name='user_details'),
    path('user/<int:pk>/edit', views.UpdateUserView.as_view(), name='user_update'),

]

