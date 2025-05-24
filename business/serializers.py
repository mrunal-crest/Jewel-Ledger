from rest_framework import serializers
from .models import Business, FinancialYear

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['id', 'name', 'description', 'address', 'phone', 'email', 'website', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class FinancialYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialYear
        fields = ['id', 'business', 'start_date', 'end_date', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] 