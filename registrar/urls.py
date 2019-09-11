from django.urls import path




from . import views

app_name = 'registrar'

urlpatterns = [
    path('student-requirements-details/', views.student_requirements_view, name='requirements'),
    path('available-course-details/', views.available_course_view, name='available-course'),
]