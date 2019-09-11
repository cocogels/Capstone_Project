from django.urls import path


from . import views

app_name = 'marketing_head'

urlpatterns = [
    
    path('budget-lis/', views.BudgetListView.as_view(), name='budget_list'),
    path('create-budget/', views.create_budget, name='budget'),
    path('budget-detail/<int:pk>/', views.BudgetDetailView.as_view(), name='budget_detail'),
    path('budget-update/<int:pk>/', views.BudgetUpdateView.as_view(), name='budget_update'),
    
    path('quota-list/', views.AssignQuotaListView.as_view(), name='assign_list'),
    path('create-quota/', views.create_assign_quota, name='assign_quota'),
    path('quota-update/<int:pk>/', views.QuotaUpdateView.as_view(), name='quota_update'),
    path('assign-territory/', views.assign_territory, name='assign_territory'),

]
