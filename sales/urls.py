from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import views as api_views

app_name = 'sales'

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'customers', api_views.CustomerViewSet)
router.register(r'sales', api_views.SaleViewSet)

urlpatterns = [
    # Customer URLs
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='customer_edit'),
    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),
    
    # Sale URLs
    path('', views.SaleListView.as_view(), name='sale_list'),
    path('create/', views.SaleCreateView.as_view(), name='sale_create'),
    path('<int:pk>/', views.SaleDetailView.as_view(), name='sale_detail'),
    path('<int:pk>/edit/', views.SaleUpdateView.as_view(), name='sale_edit'),
    path('<int:pk>/delete/', views.SaleDeleteView.as_view(), name='sale_delete'),
    
    # API URLs
    path('api/', include(router.urls)),
] 