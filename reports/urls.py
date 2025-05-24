from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import views as api_views

router = DefaultRouter()
router.register(r'reports', api_views.ReportViewSet)

app_name = 'reports'

urlpatterns = [
    # Web views
    path('', views.ReportListView.as_view(), name='report_list'),
    path('create/', views.ReportCreateView.as_view(), name='report_create'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('<int:pk>/edit/', views.ReportUpdateView.as_view(), name='report_edit'),
    path('<int:pk>/delete/', views.ReportDeleteView.as_view(), name='report_delete'),
    
    # API endpoints
    path('api/', include(router.urls)),
] 