from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Customer, Sale, SaleItem
from .serializers import CustomerSerializer, SaleSerializer, SaleItemSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Customer.objects.filter(business=self.request.user.userprofile.business)

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Sale.objects.filter(business=self.request.user.userprofile.business)

    def perform_create(self, serializer):
        sale = serializer.save(business=self.request.user.userprofile.business)
        items_data = self.request.data.get('items', [])
        
        for item_data in items_data:
            item_data['sale'] = sale.id
            item_serializer = SaleItemSerializer(data=item_data)
            if item_serializer.is_valid():
                item_serializer.save()
            else:
                sale.delete()
                return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_payment_status(self, request, pk=None):
        sale = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Sale.PAYMENT_STATUS_CHOICES):
            sale.payment_status = new_status
            sale.save()
            return Response({'status': 'success'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        queryset = self.get_queryset()
        total_sales = queryset.count()
        total_amount = sum(sale.total_amount for sale in queryset)
        pending_payments = queryset.filter(payment_status='pending').count()
        
        return Response({
            'total_sales': total_sales,
            'total_amount': total_amount,
            'pending_payments': pending_payments
        }) 