from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from . import views
from centermanager.views import SchoolYearCreateView

app_name = 'centermanager'


urlpatterns = [
    
    path('add/employee/', views.EmployeeRegistration.as_view(), name='add_employee'),
    path('employee/list/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employee/<int:pk>/details/', views.EmployeeDetailView.as_view(), name='employee_detial'),
    path('employee/<int:pk>/edit/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    
    path('create/payment/', views.PaymentCreateView.as_view(), name='create_payment'),
    path('payment/list/', views.PaymentListView.as_view(), name='payment_list'),
    path('payment/<int:pk>/details/', views.PaymentDetailView.as_view(), name='payment_detail'),
    path('payment/<int:pk>/edit/', views.PaymentUpdateView.as_view(), name='payment_update'),
    
    
    path('create/commission/', views.CommissionSettingCreateView.as_view(), name='create_commission'),
    path('commission/list/', views.CommissionSettingListView.as_view(), name='commission_list'),  
    path('commission/<int:pk>/details/', views.CommissionDetailView.as_view(), name='commission_detial'),
    path('commission/<int:pk>/edit/', views.CommissionUpdateView.as_view(), name='commission_update'),

    
    path('create/sanction/', views.SanctionSettingCreateView.as_view(), name='create_sanction'),
    path('sanction/list/', views.SanctionSettingListView.as_view(), name='sanction_list'),   
    path('sanction/<int:pk>/details/', views.SanctionSettingDetailView.as_view(), name='sanction_detial'),
    path('sanction/<int:pk>/edit/', views.SanctionSettingUpdateView.as_view(), name='sanction_update'),


    
    path('create/school-year/', views.SchoolYearCreateView.as_view(), name='create_school_year'),
    

    path('create/target-sheet/', views.TargetSheetCreateView.as_view(), name='create_target'),
    path('target-sheet/', views.TargetSheetListView.as_view(), name='target'),
    path('target-sheet/<int:pk>/details/', views.TargetSheetDetailView.as_view(), name='target_details'),
    path('target-sheet/<int:pk>/edit/', views.TargetUpdateView.as_view(), name='target_update'),
         
]




urlpatterns = format_suffix_patterns(urlpatterns)
