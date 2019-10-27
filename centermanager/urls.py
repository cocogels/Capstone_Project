from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from . import views
from . import t_views
from . import s_views
from . import sy_views
app_name = 'centermanager'


urlpatterns = [
    
    path('add/employee/', views.EmployeeRegistration.as_view(), name='add_employee'),
    path('employee/list/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employee/<int:pk>/details/', views.EmployeeDetailView.as_view(), name='employee_detial'),
    path('employee/<int:pk>/edit/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    
#    path('create/payment/', views.PaymentCreateView.as_view(), name='create_payment'),
    path('payment/list/', views.MatriculationTemplateView.as_view(), name='payment_list'),
    path('payment/view/', views.MatriculationListView.as_view(), name='payment_view'),
#    path('payment/<int:pk>/details/', views.PaymentDetailView.as_view(), name='payment_detail'),
    path('payment/<int:pk>/higher-education/nc/edit', views.MatriculationUpdateHENC.as_view(), name='henc_update'),
    path('payment/<int:pk>/higher-education/rc/edit', views.MatriculationUpdateHERC.as_view(), name='herc_update'),
    path('payment/<int:pk>/shs/edit', views.MatriculationUpdateSHS.as_view(), name='shs_update'),
    
    
    
#   path('create/commission/', views.CommissionSettingCreateView.as_view(), name='create_commission'),
    path('commission/list/', views.MatriculationTemplateView.as_view(), name='commission_list'),  
#   path('commission/<int:pk>/details/', views.CommissionDetailView.as_view(), name='commission_detial'),
    path('commission/<int:pk>/shs/edit', views.CommissionSettingSHSUpdate.as_view(), name='com_shs_update'),
    path('commission/<int:pk>/higher-education/nc/edit', views.CommissionSettingHERCUpdate.as_view(), name='com_herc_update'),
    path('commission/<int:pk>/higher-education/rc/edit', views.CommissionSettingHENCUpdate.as_view(), name='com_henc_update'),
    path('commission/<int:pk>/icl/edit', views.CommissionSettingICLUpdate.as_view(), name='com_icl_update'),

    
    path('create/sanction/', s_views.SanctionSettingCreateView.as_view(), name='create_sanction'),
    path('sanction/list/', s_views.SanctionSettingListView.as_view(), name='sanction_list'),   
    path('sanction/<int:pk>/details/', s_views.SanctionSettingDetailView.as_view(), name='sanction_detial'),
    path('sanction/<int:pk>/edit/', s_views.SanctionSettingUpdateView.as_view(), name='sanction_update'),


    path('school-year/', sy_views.SchoolYearCreateView.as_view(), name='create_school_year'),
    path('school-year/list/', sy_views.SchoolYearListView.as_view(), name='school_year_list'),
    path('school-year/<int:year>', sy_views.SchoolYearArchiveView.as_view(), name='school_year_archive'),
    
    path('create/target-sheet/<int:pk>', t_views.TargetSheetCreateView.as_view(), name='create_target'),
    path('target-sheet/', t_views.TargetSheetListView.as_view(), name='target'),
    path('target-sheet/<int:pk>/details/', t_views.TargetSheetDetailView.as_view(), name='target_details'),
    path('target-sheet/<int:pk>/edit/', t_views.TargetUpdateView.as_view(), name='target_update'),
         
]




urlpatterns = format_suffix_patterns(urlpatterns)
