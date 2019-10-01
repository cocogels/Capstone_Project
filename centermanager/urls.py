from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from . import views
from centermanager.views import SchoolYearCreateView, SchoolYearListView, SchoolYearDetailView

app_name = 'centermanager'


urlpatterns = [
    path('',views.overview, name='overview'),
    
    path('add-employee/', views.EmployeeListView.as_view(), name='register-emp-list'),
    path('add-employee/create/', views.emp_registration, name='register-emp'),

    #--------------------------SCHOOL YEAR------------------------------------------------
    path("school-year/", views.SchoolYearListView.as_view(), name='school_year_list'),
    path("school-year/", views.create_schoolYear, name='school_year'),
    path("school-year/create/", views.SchoolYearCreateView.as_view(),name='create_school_year'),
    path("school-year/<int:id>/", views.SchoolYearDetailView.as_view(), name='school_details'),

    #--------------------------TARGET SHEET------------------------------------------------    
    path('target-list/', views.TargetSheetListView.as_view(), name='target_list'),
    path("target-list/", views.create_targetSheet, name='target_sheet'),
    #path('create-target-details/', views.create_target_sheet, name='target' ),
    path('create-target-details/', views.create_targetSheet, name='target'),
    path('target-details/<int:pk>/', views.TargetDetailView.as_view(), name="target_details"),
    path('update-target-detail/<int:pk>', views.TargetUpdateView.as_view(), name='target_update'),
        
    #--------------------------SANCTION------------------------------------------------        
    path('sanction-list/', views.SanctionListView.as_view(), name='sanction_list'),
    path('create-sanction-details/', views.create_sanction_setting, name='sanction'),
    path('sanction-detail/<int:pk>/', views.SanctionDetailView.as_view(), name='sanction_detail'),
    path('sanction-update/<int:pk>/', views.SanctionUpdateView.as_view(), name='sanction_update'),

    #--------------------------COMMISSION------------------------------------------------    
    path('commission-list/', views.CommissionListView.as_view(), name='commission_list'),
    path('create-commission-details/', views.create_commission_setting, name='commission'),
    path('commission-detail/<int:pk>/', views.CommissionDetailView.as_view(), name='commission_detail'),
    path('commission-update/<int:pk>/', views.CommissionUpdateView.as_view(), name='commission_update'),

    #--------------------------MATRICULATION------------------------------------------------    
    path('matriculation-list/', views.matriculationListView.as_view(), name='matriculation_list'),
    path('create-matriculation-details/', views.create_payment, name='matriculation'),
   
    
]


urlpatterns = format_suffix_patterns(urlpatterns)
