from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Purchase, PurchaseItem, Supplier
from .serializers import PurchaseSerializer, PurchaseItemSerializer, SupplierSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Supplier.objects.filter(business=self.request.user.userprofile.business)

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Purchase.objects.filter(business=self.request.user.userprofile.business)

    def perform_create(self, serializer):
        purchase = serializer.save(business=self.request.user.userprofile.business)
        items_data = self.request.data.get('items', [])
        
        for item_data in items_data:
            item_data['purchase'] = purchase.id
            item_serializer = PurchaseItemSerializer(data=item_data)
            if item_serializer.is_valid():
                item_serializer.save()
            else:
                purchase.delete()
                return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_payment_status(self, request, pk=None):
        purchase = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Purchase.PAYMENT_STATUS_CHOICES):
            purchase.payment_status = new_status
            purchase.save()
            return Response({'status': 'success'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        queryset = self.get_queryset()
        total_purchases = queryset.count()
        total_amount = sum(purchase.total_amount for purchase in queryset)
        pending_payments = queryset.filter(payment_status='pending').count()
        
        return Response({
            'total_purchases': total_purchases,
            'total_amount': total_amount,
            'pending_payments': pending_payments
        }) 