from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import views as api_views

app_name = 'purchases'

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'suppliers', api_views.SupplierViewSet)
router.register(r'purchases', api_views.PurchaseViewSet)

urlpatterns = [
    # Supplier URLs
    path('suppliers/', views.SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/<int:pk>/', views.SupplierDetailView.as_view(), name='supplier_detail'),
    path('suppliers/<int:pk>/edit/', views.SupplierUpdateView.as_view(), name='supplier_edit'),
    path('suppliers/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),
    
    # Purchase URLs
    path('', views.PurchaseListView.as_view(), name='purchase_list'),
    path('create/', views.PurchaseCreateView.as_view(), name='purchase_create'),
    path('<int:pk>/', views.PurchaseDetailView.as_view(), name='purchase_detail'),
    path('<int:pk>/edit/', views.PurchaseUpdateView.as_view(), name='purchase_edit'),
    path('<int:pk>/delete/', views.PurchaseDeleteView.as_view(), name='purchase_delete'),
    
    # API URLs
    path('api/', include(router.urls)),
] 