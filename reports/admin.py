from django.contrib import admin
from .models import FinancialYear, Report

@admin.register(FinancialYear)
class FinancialYearAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'is_active', 'created_at')
    list_filter = ('is_active',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'financial_year', 'start_date', 'end_date', 'created_by', 'created_at')
    list_filter = ('report_type', 'financial_year', 'created_by')
    search_fields = ('report_type',)
