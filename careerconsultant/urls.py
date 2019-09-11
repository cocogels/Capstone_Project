from django.urls import path

from . import views

app_name = 'careerconsultant'

urlpatterns = [
    path('add-contacts/', views.create_icl_contact, name='icl_contact'),
    path('contacts-list/', views.ICLContactListView.as_view(), name='icl_contact_list'),

]
