from django.urls import path, include


from activity.views import(
    RequestActivityCreateView,
    RequestActivityListView,
    RequestActivityDetailView,
    RequestActivityUpdateView,
)

app_name = 'activity'

urlpatterns = [
    
    

    path('api/request/', RequestActivityCreateView.as_view(), name='request_activity'),
    path('api/request/list/', RequestActivityListView.as_view(), name='list_activity'),
    path('api/request/<int:pk>/view/', RequestActivityDetailView.as_view(), name='detail_activity'),
    path('api/request/<int:pk>/edit/', RequestActivityUpdateView.as_view(), name='edit_activity'),

]
