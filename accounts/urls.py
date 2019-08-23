from django.urls import path


from accounts.views import user_registration

app_name="accounts"

urlpatterns = [
    path('registration/', user_registration, name='register'),
    # path('user-login/', user_login, name='login' ),
    # path('user-logout/', user_logout, name='logout'),
]