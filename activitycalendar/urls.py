from django.urls import path, include

from activitycalendar.views import CalendarTemplateView,CalendarCreateView

from . import views 
 
app_name = 'calendar'


urlpatterns = [
 
    # path('calendar/', CalendarTemplateView.as_view(), name='calendar_home'),
    # path('calendar/add/activity/', CalendarCreateView.as_view(), name='add_activity'),
]
