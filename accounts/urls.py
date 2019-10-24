from django.urls import path



from . import views

app_name="accounts"

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile' ),
    path('add/user/', views.CreateUserView.as_view(), name='create_user'),
    path('user/list/', views.UsersListView.as_view(), name='user_list'),
    path('user/<int:pk>/detail', views.UserDetailView.as_view(), name='user_details'),
    path('user/<int:pk>/edit', views.UpdateUserView.as_view(), name='user_update'),
]

