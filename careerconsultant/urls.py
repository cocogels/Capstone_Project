from django.urls import path

from . import views

app_name = 'careerconsultant'

urlpatterns = [
    path('add-contacts/', views.create_icl_contact, name='icl_contact'),
    path('contacts-list/', views.ICLContactListView.as_view(), name='icl_contact_list'),

    path('add-contacts/', views.create_ihe_contact, name='ihe_contact'),
    path('contacts-list/', views.IHEContactListView.as_view(),name='ihe_contact_list'),
    
    path('add-contacts/', views.create_shs_contact, name='shs_contact'),
    path('contacts-list/', views.SHSContactListView.as_view(), name='shs_contact_list'),
]
