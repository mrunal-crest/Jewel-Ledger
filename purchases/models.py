from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product
from business.models import Business
from core.models import Transaction

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='purchase')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchases')
    additional_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.final_amount = self.transaction.total_amount + self.additional_cost
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Purchase from {self.supplier.name} - {self.transaction.product.name}"
