from django.contrib import admin
from .models import Supplier, Purchase

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at', 'updated_at')
    search_fields = ('name', 'phone', 'email', 'address')
    list_filter = ('created_at', 'updated_at')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'supplier', 'additional_cost', 'final_amount', 'payment_status', 'created_at', 'updated_at')
    list_filter = ('payment_status', 'created_at', 'updated_at')
    search_fields = ('supplier__name', 'transaction__product__name')
    readonly_fields = ('final_amount',)
