from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'subcategories', views.SubCategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'sales', views.SaleViewSet)
router.register(r'purchases', views.PurchaseViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'suppliers', views.SupplierViewSet)
router.register(r'financial-years', views.FinancialYearViewSet)
router.register(r'reports/profit-loss', views.ProfitLossReportView, basename='profit-loss')
router.register(r'reports/inventory', views.InventoryReportView, basename='inventory')
router.register(r'reports/sales', views.SalesReportView, basename='sales')
router.register(r'reports/purchases', views.PurchasesReportView, basename='purchases')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
] 