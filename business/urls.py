from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

router = DefaultRouter()
router.register(r'businesses', api_views.BusinessViewSet)

app_name = 'business'

urlpatterns = [
    # Web views
    path('', views.BusinessListView.as_view(), name='business_list'),
    path('create/', views.BusinessCreateView.as_view(), name='business_create'),
    path('details/', views.BusinessDetailView.as_view(), name='business_detail'),
    path('edit/', views.BusinessUpdateView.as_view(), name='business_edit'),
    path('<int:pk>/delete/', views.BusinessDeleteView.as_view(), name='business_delete'),
    
    # API endpoints
    path('api/', include(router.urls)),
] 