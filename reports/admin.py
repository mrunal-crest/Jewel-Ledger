from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'financial_year', 'start_date', 'end_date', 'created_by', 'created_at')
    list_filter = ('report_type', 'financial_year', 'created_at')
    search_fields = ('report_type', 'financial_year__start_date', 'financial_year__end_date')
