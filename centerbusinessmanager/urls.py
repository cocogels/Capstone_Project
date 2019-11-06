from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from . import views

app_name = 'cbm'

urlpatterns = [
    path('activity/detailed', views.activity_detailed, name='activity_detailed'),
     path('activity/pending', views.activity_pending, name='activity_pending'),

]
urlpatterns = format_suffix_patterns(urlpatterns)