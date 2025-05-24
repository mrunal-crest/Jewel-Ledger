from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Report
from .forms import ReportForm

# Create your views here.

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reports/report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return Report.objects.filter(business=self.request.user.userprofile.business)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("current user: ",self.request.user.userprofile.business)
        business = self.request.user.userprofile.business
        
        # Get date range for dashboard stats
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)
        
        # Sales statistics
        context['total_sales'] = business.sales.filter(date__gte=thirty_days_ago).aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        context['sales_count'] = business.sales.filter(date__gte=thirty_days_ago).count()
        
        # Purchase statistics
        context['total_purchases'] = business.purchases.filter(date__gte=thirty_days_ago).aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        context['purchases_count'] = business.purchases.filter(date__gte=thirty_days_ago).count()
        
        # Inventory statistics
        context['total_products'] = business.products.count()
        context['low_stock_products'] = business.products.filter(quantity__lte=10).count()
        
        return context

class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/report_form.html'
    success_url = reverse_lazy('reports:report_list')

    def form_valid(self, form):
        form.instance.business = self.request.user.userprofile.business
        return super().form_valid(form)

class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/report_form.html'
    success_url = reverse_lazy('reports:report_list')

    def get_queryset(self):
        return Report.objects.filter(business=self.request.user.userprofile.business)

class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'reports/report_confirm_delete.html'
    success_url = reverse_lazy('reports:report_list')

    def get_queryset(self):
        return Report.objects.filter(business=self.request.user.userprofile.business)

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'reports/report_detail.html'
    context_object_name = 'report'

    def get_queryset(self):
        return Report.objects.filter(business=self.request.user.userprofile.business)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = self.get_object()
        
        # Add report-specific data based on report type
        if report.report_type == 'sales':
            context['data'] = report.business.sales.filter(
                date__range=[report.start_date, report.end_date]
            )
        elif report.report_type == 'purchases':
            context['data'] = report.business.purchases.filter(
                date__range=[report.start_date, report.end_date]
            )
        elif report.report_type == 'inventory':
            context['data'] = report.business.products.all()
        
        return context
