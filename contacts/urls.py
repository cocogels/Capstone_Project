from django.urls import path
from contacts.views import ICLContactListView, ICLContactDetailView, ICLContactUpdateView, ICLContactCreateView
app_name = 'contacts'

urlpatterns = [
    path('icl-contact-list/', ICLContactListView.as_view(), name='list'),
    path('add-contacts/', ICLContactCreateView.as_view(), name='add_contact'),
    path('icl-contact-details/<int:pk>', ICLContactDetailView.as_view(), name='view_contact'),
    path('icl-contact-edit/<int:pk>', ICLContactUpdateView.as_view(), name='edit_contact'),
]
