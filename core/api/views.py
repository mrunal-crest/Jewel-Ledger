from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from business.models import Business
from core.models import Category, SubCategory, Product, FinancialYear, Transaction
from sales.models import Sale, Customer
from purchases.models import Purchase, Supplier
from accounts.models import UserProfile
from .serializers import (
    CategorySerializer, SubCategorySerializer, ProductSerializer,
    SaleSerializer, PurchaseSerializer, CustomerSerializer,
    SupplierSerializer, FinancialYearSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = ['name']

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = ['category', 'name']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = ['subcategory', 'subcategory__category']

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['customer__name', 'transaction__product__name']
    filterset_fields = ['payment_status', 'transaction__financial_year']

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['supplier__name', 'transaction__product__name']
    filterset_fields = ['payment_status', 'transaction__financial_year']

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone', 'email']

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone', 'email']

class FinancialYearViewSet(viewsets.ModelViewSet):
    queryset = FinancialYear.objects.all()
    serializer_class = FinancialYearSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']

class ProfitLossReportView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        financial_year = request.query_params.get('financial_year')
        if not financial_year:
            return Response({'error': 'Financial year is required'}, status=400)

        # Get sales and purchases for the financial year
        sales = Sale.objects.filter(transaction__financial_year_id=financial_year)
        purchases = Purchase.objects.filter(transaction__financial_year_id=financial_year)

        # Calculate totals
        total_sales = sum(sale.final_amount for sale in sales)
        total_purchases = sum(purchase.final_amount for purchase in purchases)
        profit_loss = total_sales - total_purchases

        return Response({
            'total_sales': total_sales,
            'total_purchases': total_purchases,
            'profit_loss': profit_loss
        })

class InventoryReportView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        category = request.query_params.get('category')
        subcategory = request.query_params.get('subcategory')

        products = Product.objects.all()
        if category:
            products = products.filter(subcategory__category_id=category)
        if subcategory:
            products = products.filter(subcategory_id=subcategory)

        inventory_data = []
        for product in products:
            inventory_data.append({
                'product_name': product.name,
                'category': product.subcategory.category.name,
                'subcategory': product.subcategory.name,
                'weight': product.weight,
                'price_per_gram': product.price_per_gram,
                'total_value': product.total_price
            })

        return Response(inventory_data)

class SalesReportView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        financial_year = request.query_params.get('financial_year')
        if not financial_year:
            return Response({'error': 'Financial year is required'}, status=400)

        sales = Sale.objects.filter(transaction__financial_year_id=financial_year)
        sales_data = []
        for sale in sales:
            sales_data.append({
                'date': sale.transaction.transaction_date,
                'customer': sale.customer.name,
                'product': sale.transaction.product.name,
                'quantity': sale.transaction.quantity,
                'price_per_gram': sale.transaction.price_per_gram,
                'total_amount': sale.final_amount
            })

        return Response(sales_data)

class PurchasesReportView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        financial_year = request.query_params.get('financial_year')
        if not financial_year:
            return Response({'error': 'Financial year is required'}, status=400)

        purchases = Purchase.objects.filter(transaction__financial_year_id=financial_year)
        purchases_data = []
        for purchase in purchases:
            purchases_data.append({
                'date': purchase.transaction.transaction_date,
                'supplier': purchase.supplier.name,
                'product': purchase.transaction.product.name,
                'quantity': purchase.transaction.quantity,
                'price_per_gram': purchase.transaction.price_per_gram,
                'total_amount': purchase.final_amount
            })

        return Response(purchases_data) 