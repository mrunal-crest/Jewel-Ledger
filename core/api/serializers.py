from rest_framework import serializers
from business.models import Business
from core.models import Category, SubCategory, Product, FinancialYear, Transaction
from sales.models import Sale, Customer
from purchases.models import Purchase, Supplier
from accounts.models import UserProfile

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = SubCategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='subcategory.category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class FinancialYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialYear
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    product_name = serializers.CharField(source='transaction.product.name', read_only=True)
    category_name = serializers.CharField(source='transaction.product.subcategory.category.name', read_only=True)
    subcategory_name = serializers.CharField(source='transaction.product.subcategory.name', read_only=True)

    class Meta:
        model = Sale
        fields = '__all__'

    def create(self, validated_data):
        transaction_data = validated_data.pop('transaction')
        transaction = Transaction.objects.create(**transaction_data)
        sale = Sale.objects.create(transaction=transaction, **validated_data)
        return sale

    def update(self, instance, validated_data):
        transaction_data = validated_data.pop('transaction', None)
        if transaction_data:
            transaction = instance.transaction
            for attr, value in transaction_data.items():
                setattr(transaction, attr, value)
            transaction.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class PurchaseSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    product_name = serializers.CharField(source='transaction.product.name', read_only=True)
    category_name = serializers.CharField(source='transaction.product.subcategory.category.name', read_only=True)
    subcategory_name = serializers.CharField(source='transaction.product.subcategory.name', read_only=True)

    class Meta:
        model = Purchase
        fields = '__all__'

    def create(self, validated_data):
        transaction_data = validated_data.pop('transaction')
        transaction = Transaction.objects.create(**transaction_data)
        purchase = Purchase.objects.create(transaction=transaction, **validated_data)
        return purchase

    def update(self, instance, validated_data):
        transaction_data = validated_data.pop('transaction', None)
        if transaction_data:
            transaction = instance.transaction
            for attr, value in transaction_data.items():
                setattr(transaction, attr, value)
            transaction.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance 