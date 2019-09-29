from django.urls import path




from . import views

app_name = 'registrar'

urlpatterns = [
    

    path('create/requirements/', views.RequirementsCreateView.as_view(), name='add_requirements'),
    path('list/requirements/', views.RequirementsListView.as_view(), name='requirements_list'),
    path('requirements/<int:pk>/detail/', views.RequirementsDetailView.as_view(), name='requirements_view'),
    path('requirements/<int:pk>/edit/', views.RequirementsUpdateView.as_view(), name='requirements_edit'),

    
    
    path('create/course/', views.CourseCreateView.as_view(), name='add_course'),
    path('list/available-course/', views.CourseListView.as_view(), name='course_list'),
    path('<int:pk>/available-course/detail/', views.CourseDetailView.as_view(), name='course_view'),
    path('<int:pk>/available-course/edit/', views.CourseUpdateView.as_view(), name='course_edit'),


]


