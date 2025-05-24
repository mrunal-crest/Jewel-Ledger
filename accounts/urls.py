from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import views as api_views

app_name = 'accounts'

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'auth', api_views.AuthViewSet, basename='auth')
router.register(r'businesses', api_views.BusinessViewSet, basename='business')
router.register(r'profile', api_views.UserProfileViewSet, basename='profile')

urlpatterns = [
    # Web URLs
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('create-business/', views.create_business, name='create_business'),
    
    # API URLs
    path('api/', include(router.urls)),
    path('', include('django.contrib.auth.urls')),
] 