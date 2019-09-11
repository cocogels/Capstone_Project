from django.urls import path
from . import views

app_name = 'crm_blog'

urlpatterns = [
    path('home/', views.blog_home_view, name='home'),
    path('view-target-sheet/', views.ViewTargetListView.as_view(), name='view-target-list')
]
