from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from inventory.models import Product
from business.models import FinancialYear

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('PURCHASE', 'Purchase'),
        ('SALE', 'Sale'),
    ]

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions')
    quantity = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(Decimal('0.001'))])
    price_per_gram = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='transactions')
    transaction_date = models.DateField()
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.price_per_gram
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.product.name} ({self.quantity}g)"
