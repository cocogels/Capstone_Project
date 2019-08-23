from django.urls import path


from . import views


app_name = 'centermanager'


urlpatterns = [
    
    path('create-target-details/', views.create_target_sheet, name='target' ),
    path('list-target-sheet/', views.list_target_sheet, name='target_list'),
    path('update-target-sheet/', views.update_target_sheet, name='target_details'),
    path('create-payment-details/', views.create_payment_details, name='payment'),
    path('create-sanction-details/', views.create_sanction_setting, name='sanction'),
    path('create-commission-details/', views.create_commission_setting, name='commission'),
    
]