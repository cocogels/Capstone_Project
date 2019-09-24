from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from . import views
from centermanager.views import SchoolYearCreateView, SchoolYearListView, SchoolYearDetailView

app_name = 'centermanager'


urlpatterns = [
    
    
    path('add-employee/', views.EmployeeListView.as_view(), name='register-emp-list'),
    path('add-employee/create/', views.emp_registration, name='register-emp'),


    path("school-year/", SchoolYearListView.as_view(), name='school_year_list'),
    path("school-year/create/", SchoolYearCreateView.as_view(),name='create_school_year'),
    path("school-year/<int:id>/", SchoolYearDetailView.as_view(), name='school_details'),
    
    path('target-list/', views.TargetListView.as_view(), name='target_list'),
    path('create-target-details/', views.create_target_sheet, name='target' ),
    
    #path('add-school-year/', views.SchoolYearArchiveView.as_view(), name='school_year'),
    path('target-details/<int:pk>/', views.TargetDetailView.as_view(), name="target_details"),
    path('update-target-detail/<int:pk>', views.TargetUpdateView.as_view(), name='target_update'),
    
    # path('payment-list/', views.PaymentListView.as_view(), name='payment_list'),
    # path('create-payment-details/', views.create_payment, name='payment'),
    # path('payment-details/<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    # path('payment-update/<int:pk>/', views.PaymentUpdateView.as_view(), name='payment_update'),
    
    path('sanction-list/', views.SanctionListView.as_view(), name='sanction_list'),
    path('create-sanction-details/', views.create_sanction_setting, name='sanction'),
    path('sanction-detail/<int:pk>/', views.SanctionDetailView.as_view(), name='sanction_detail'),
    path('sanction-update/<int:pk>/', views.SanctionUpdateView.as_view(), name='sanction_update'),
    
    path('commission-list/', views.CommissionListView.as_view(), name='commission_list'),
    path('create-commission-details/', views.create_commission_setting, name='commission'),
    path('commission-detail/<int:pk>/', views.CommissionDetailView.as_view(), name='commission_detail'),
    path('commission-update/<int:pk>/', views.CommissionUpdateView.as_view(), name='commission_update'),
    
]


urlpatterns = format_suffix_patterns(urlpatterns)
