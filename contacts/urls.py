from django.urls import path
from contacts.views import ICLContactListView, ICLContactDetailView, ICLContactUpdateView, ICLContactCreateView
from contacts.views import SHSContactListView, SHSContactCreateView, SHSContactDetailView, SHSContactUpdateView
from contacts.views import IHEContactListView, IHEContactCreateView, IHEContactDetailView, IHEContactUpdateView


app_name = 'contacts'

urlpatterns = [
    path('icl/contact-list/', ICLContactListView.as_view(), name='list'),
    path('icl/add-contacts/', ICLContactCreateView.as_view(), name='add_contact'),
    path('icl/contact-details/<int:pk>', ICLContactDetailView.as_view(), name='view_contact'),
    path('icl/contact-edit/<int:pk>', ICLContactUpdateView.as_view(), name='edit_contact'),
    
    path('shs/contact-list/', SHSContactListView.as_view(), name='shs_list'),
    path('shs/add-contacts/', SHSContactCreateView.as_view(), name='shs_add_contact'),
    path('shs/contact-details/<int:pk>', SHSContactDetailView.as_view(), name='shs_view_contact'),
    path('shs/contact-edit/<int:pk>', SHSContactUpdateView.as_view(), name='shs_edit_contact'),
    
    path('ihe/contact-list/', IHEContactListView.as_view(), name='ihe_list'),
    path('ihe/add-contacts/', IHEContactCreateView.as_view(), name='ihe_add_contact'),
    path('ihe/contact-details/<int:pk>', IHEContactDetailView.as_view(), name='ihe_view_contact'),
    path('ihe/contact-edit/<int:pk>', IHEContactUpdateView.as_view(), name='ihe_edit_contact'),
]
