from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login
from .serializers import UserRegistrationSerializer, BusinessSerializer, UserProfileSerializer
from ..models import UserProfile
from business.models import Business

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            business = Business.objects.create(
                name=request.data.get('business_name'),
                owner=user
            )
            UserProfile.objects.create(
                user=user,
                business=business,
                phone=request.data.get('phone', ''),
                address=request.data.get('address', ''),
                role=request.data.get('role', '')
            )
            return Response({
                'message': 'User registered successfully',
                'user_id': user.id,
                'business_id': business.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            return Response({
                'message': 'Login successful',
                'user_id': user.id,
                'business_id': user.userprofile.business.id if hasattr(user, 'userprofile') else None
            })
        return Response({
            'message': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

class BusinessViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Business.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        business = serializer.save(owner=self.request.user)
        profile = self.request.user.userprofile
        profile.business = business
        profile.save()

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_object(self):
        return self.request.user.userprofile 