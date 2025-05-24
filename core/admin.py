from django.contrib import admin
from .models import (
    Category,
    SubCategory,
    Product,
    FinancialYear,
    Transaction
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'category__name')
    list_filter = ('category', 'created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'weight', 'price_per_gram', 'total_price', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'subcategory__name')
    list_filter = ('subcategory', 'created_at', 'updated_at')

@admin.register(FinancialYear)
class FinancialYearAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'product', 'quantity', 'price_per_gram', 'total_amount', 'transaction_date', 'created_by')
    search_fields = ('product__name', 'notes')
    list_filter = ('transaction_type', 'transaction_date', 'created_at', 'updated_at')
