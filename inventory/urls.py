from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import views as api_views

router = DefaultRouter()
router.register(r'products', api_views.ProductViewSet)
router.register(r'categories', api_views.CategoryViewSet)
router.register(r'subcategories', api_views.SubCategoryViewSet)

app_name = 'inventory'

urlpatterns = [
    # Product views
    path('', views.ProductListView.as_view(), name='product_list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    
    # Category views
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # SubCategory views
    path('subcategories/', views.SubCategoryListView.as_view(), name='subcategory_list'),
    path('subcategories/create/', views.SubCategoryCreateView.as_view(), name='subcategory_create'),
    path('subcategories/<int:pk>/edit/', views.SubCategoryUpdateView.as_view(), name='subcategory_edit'),
    path('subcategories/<int:pk>/delete/', views.SubCategoryDeleteView.as_view(), name='subcategory_delete'),
    
    # API endpoints
    path('api/', include(router.urls)),
] 