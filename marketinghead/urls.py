from django.urls import path


from . import views

app_name = 'marketing_head'

urlpatterns = [
    
    path('budget-list/', views.BudgetListView.as_view(), name='budget_list'),
    path('create-budget/', views.create_collateral, name='budget'),
    path('budget-detail/<int:pk>/', views.BudgetDetailView.as_view(), name='budget_detail'),
    path('budget-update/<int:pk>/', views.BudgetUpdateView.as_view(), name='budget_update'),
    
    
    path('collateral-list/', views.CollateralListView.as_view(), name='collateral_list'),
    path('create-collateral/', views.create_budget, name='create_collateral'),
    path('collateral-detail/<int:pk>/', views.CollateralDetailView.as_view(), name='collateral_detail'),
    path('collateral-update/<int:pk>/', views.CollateralUpdateView.as_view(), name='collateral_update'),
    
    
    path('quota-list/', views.AssignQuotaListView.as_view(), name='assign_list'),
    path('create-quota/', views.create_assign_quota, name='assign_quota'),
    path('quota-update/<int:pk>/', views.QuotaUpdateView.as_view(), name='quota_update'),
    path('assign-territory/', views.assign_territory, name='assign_territory'),

]
