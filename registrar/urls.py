from django.urls import path




from . import views

app_name = 'registrar'

urlpatterns = [
    

    path('list/requirements/', views.RequirementsListView.as_view(), name='requirements_list'),
    path('create/requirements', views.RequirementsCreateView.as_view(), name='add_requirements'),
    path('create/requirements/transferee', views.RrequirementsTransCreateView.as_view(), name='add_trans_requirements'),
    path('requirements/<int:pk>/detail/', views.RequirementsDetailView.as_view(), name='requirements_view'),
    path('requirements/transferee/<int:pk>/detail/', views.RequirementsTransDetailView.as_view(), name='requirements_trans_view'),
    path('requirements/<int:pk>/edit/', views.RequirementsUpdateView.as_view(), name='requirements_edit'),
    path('requirements/transferee/<int:pk>/edit/', views.RequirementsTransUpdateView.as_view(), name='requirements_trans_edit'),
 
    
    
    path('create/course/', views.CourseCreateView.as_view(), name='add_course'),
    path('list/course/', views.CourseListView.as_view(), name='course_list'),
    path('<int:pk>/course/detail/', views.CourseDetailView.as_view(), name='course_view'),
    path('<int:pk>/course/edit/', views.CourseUpdateView.as_view(), name='course_edit'),


]


