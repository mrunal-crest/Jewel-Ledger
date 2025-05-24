from rest_framework import viewsets
from .models import Business, FinancialYear
from .serializers import BusinessSerializer, FinancialYearSerializer

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

    def get_queryset(self):
        return Business.objects.filter(owner=self.request.user)

class FinancialYearViewSet(viewsets.ModelViewSet):
    queryset = FinancialYear.objects.all()
    serializer_class = FinancialYearSerializer

    def get_queryset(self):
        return FinancialYear.objects.filter(business__owner=self.request.user) 