
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from . import views

app_name = 'career_consultant'

urlpatterns = [
    path('activity', views.activity, name='activity'),
    path('contact/details/', views.activity1, name='activity1'),
    path('requested/activity', views.activity2, name='activity2'),
    path('requested/activity/list', views.activitylist, name='activitylist'),
    path('request/activity/', views.request_activity, name='activity_req'),

]
urlpatterns = format_suffix_patterns(urlpatterns)