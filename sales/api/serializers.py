from rest_framework import serializers
from ..models import Customer, Sale, SaleItem
from inventory.models import Product

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = SaleItem
        fields = ('id', 'product', 'product_name', 'quantity', 'price', 'total')
        read_only_fields = ('id', 'total')

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']
        
        if product.stock_quantity < quantity:
            raise serializers.ValidationError(
                f"Not enough stock. Available: {product.stock_quantity}"
            )
        return data

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Sale
        fields = ('id', 'invoice_number', 'date', 'customer', 'customer_name',
                 'payment_status', 'total_amount', 'items', 'created_at', 'updated_at')
        read_only_fields = ('id', 'invoice_number', 'total_amount', 'created_at', 'updated_at')

    def create(self, validated_data):
        items_data = self.context['request'].data.get('items', [])
        sale = Sale.objects.create(**validated_data)
        
        total_amount = 0
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product'])
            quantity = item_data['quantity']
            price = item_data['price']
            
            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                price=price
            )
            
            # Update product stock
            product.stock_quantity -= quantity
            product.save()
            
            total_amount += quantity * price
        
        sale.total_amount = total_amount
        sale.save()
        return sale 