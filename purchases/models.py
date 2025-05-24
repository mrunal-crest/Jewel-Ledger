from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product
from business.models import Business
from transactions.models import Transaction

class Supplier(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='suppliers')
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='purchases')
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='purchase')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchases')
    date = models.DateField()
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

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"
