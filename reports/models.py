from django.db import models
from django.contrib.auth.models import User
from business.models import Business, FinancialYear

# Create your models here.

class Report(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reports')
    REPORT_TYPES = [
        ('PROFIT_LOSS', 'Profit & Loss'),
        ('INVENTORY', 'Inventory'),
        ('SALES', 'Sales'),
        ('PURCHASES', 'Purchases'),
    ]

    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField(blank=True, null=True)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_report_type_display()} Report"
