from rest_framework import serializers
from ..models import Report
# Import Business model if needed for related fields, though serializer should handle ForeignKey

class ReportSerializer(serializers.ModelSerializer):
    # Explicitly define fields to be serialized
    id = serializers.ReadOnlyField()
    name = serializers.CharField(read_only=True)
    report_type = serializers.CharField(read_only=True, source='get_report_type_display') # Display human-readable choice
    description = serializers.CharField(read_only=True)
    financial_year = serializers.StringRelatedField(read_only=True) # Display string representation of FinancialYear
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True) # Display username of creator
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    # Add a method field to access business data if needed, with a check for None
    business_name = serializers.SerializerMethodField()

    def get_business_name(self, obj):
        # Check if the report has a business linked
        if obj.business:
            return obj.business.name
        return None # Or an empty string, depending on desired output

    class Meta:
        model = Report
        fields = [
            'id', 'name', 'report_type', 'description', 'financial_year', 
            'start_date', 'end_date', 'created_by', 'created_at', 'updated_at',
            'business_name', # Include the new field
        ] 