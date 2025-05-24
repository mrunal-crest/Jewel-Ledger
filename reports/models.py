from django.db import models
from django.contrib.auth.models import User
from business.models import Business

# Create your models here.

class FinancialYear(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='financial_years')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.start_date.year} - {self.end_date.year}"

class Report(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reports')
    REPORT_TYPES = [
        ('PROFIT_LOSS', 'Profit & Loss'),
        ('INVENTORY', 'Inventory'),
        ('SALES', 'Sales'),
        ('PURCHASES', 'Purchases'),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_report_type_display()} Report - {self.start_date} to {self.end_date}"
