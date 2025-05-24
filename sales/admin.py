from django.contrib import admin
from .models import Customer, Sale

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at', 'updated_at')
    search_fields = ('name', 'phone', 'email', 'address')
    list_filter = ('created_at', 'updated_at')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'customer', 'discount', 'final_amount', 'payment_status', 'created_at', 'updated_at')
    list_filter = ('payment_status', 'created_at', 'updated_at')
    search_fields = ('customer__name', 'transaction__product__name')
    readonly_fields = ('final_amount',)
