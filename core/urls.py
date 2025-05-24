from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home and Dashboard
    path('', views.home, name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('business/create/', views.BusinessCreateView.as_view(), name='create_business'),

    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # SubCategory URLs
    path('subcategories/', views.subcategory_list, name='subcategory_list'),
    path('subcategories/create/', views.subcategory_create, name='subcategory_create'),
    path('subcategories/<int:pk>/update/', views.subcategory_update, name='subcategory_update'),
    path('subcategories/<int:pk>/delete/', views.subcategory_delete, name='subcategory_delete'),

    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # Sale URLs
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/create/', views.sale_create, name='sale_create'),
    path('sales/<int:pk>/', views.sale_detail, name='sale_detail'),
    path('sales/<int:pk>/update/', views.sale_update, name='sale_update'),
    path('sales/<int:pk>/delete/', views.sale_delete, name='sale_delete'),

    # Purchase URLs
    path('purchases/', views.purchase_list, name='purchase_list'),
    path('purchases/create/', views.purchase_create, name='purchase_create'),
    path('purchases/<int:pk>/', views.purchase_detail, name='purchase_detail'),
    path('purchases/<int:pk>/update/', views.purchase_update, name='purchase_update'),
    path('purchases/<int:pk>/delete/', views.purchase_delete, name='purchase_delete'),

    # Customer URLs
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/update/', views.customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),

    # Supplier URLs
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/update/', views.supplier_update, name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),

    # Report URLs
    path('reports/profit-loss/', views.profit_loss_report, name='profit_loss'),
    path('reports/inventory/', views.inventory_report, name='inventory_report'),
    path('reports/sales/', views.sales_report, name='sales_report'),
    path('reports/purchases/', views.purchases_report, name='purchases_report'),

    # Financial Year URLs
    path('financial-years/', views.financial_year_list, name='financial_year_list'),
    path('financial-years/create/', views.financial_year_create, name='financial_year_create'),
    path('financial-years/<int:pk>/update/', views.financial_year_update, name='financial_year_update'),
    path('financial-years/<int:pk>/delete/', views.financial_year_delete, name='financial_year_delete'),
] 