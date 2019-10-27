from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from . import views

app_name = 'cbm'

urlpatterns = [
    path('activity', views.activity_list, name='activity_list'),

]
urlpatterns = format_suffix_patterns(urlpatterns)