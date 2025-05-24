from rest_framework import serializers
from django.contrib.auth.models import User
from business.models import Business
from ..models import UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    business_name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True, required=False)
    address = serializers.CharField(write_only=True, required=False)
    role = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 
                 'first_name', 'last_name', 'business_name', 'phone', 
                 'address', 'role')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data.pop('business_name')
        validated_data.pop('phone', None)
        validated_data.pop('address', None)
        validated_data.pop('role', None)
        
        user = User.objects.create_user(**validated_data)
        return user

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ('id', 'name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    business = BusinessSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'business', 'phone', 'address', 'role')
        read_only_fields = ('id', 'user', 'business') 