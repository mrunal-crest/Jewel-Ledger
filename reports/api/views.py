from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Report
from .serializers import ReportSerializer
from django.db.models import Q # Import Q object for complex lookups

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Ensure only reports belonging to the user's business are accessible
        # Handle the case where the user's business might be None
        user = self.request.user
        if hasattr(user, 'userprofile') and user.userprofile.business:
            return Report.objects.filter(business=user.userprofile.business)
        else:
            # If the user has no linked business, return an empty queryset
            return Report.objects.none() 