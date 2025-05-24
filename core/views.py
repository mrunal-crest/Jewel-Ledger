from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from sales.models import Sale, Customer
from purchases.models import Purchase, Supplier
from business.models import Business
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import BusinessForm

# Create your views here.
@login_required
def home(request):
    return render(request, 'core/home.html')

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        business = self.request.user.userprofile.business

        # Calculate today's sales
        today_sales = Sale.objects.filter(
            transaction__transaction_date__date=today,
            transaction__business=business
        ).aggregate(total=models.Sum('final_amount'))['total'] or 0

        # Calculate today's purchases
        today_purchases = Purchase.objects.filter(
            transaction__transaction_date__date=today,
            transaction__business=business
        ).aggregate(total=models.Sum('final_amount'))['total'] or 0

        # Get total products
        total_products = Product.objects.filter(business=business).count()

        # Get low stock items (products with quantity less than 5)
        low_stock_items = Product.objects.filter(
            business=business,
            quantity__lt=5
        ).count()

        # Get recent sales
        recent_sales = Sale.objects.filter(
            transaction__business=business
        ).order_by('-transaction__transaction_date')[:5]

        # Get recent purchases
        recent_purchases = Purchase.objects.filter(
            transaction__business=business
        ).order_by('-transaction__transaction_date')[:5]

        context.update({
            'today_sales': today_sales,
            'today_purchases': today_purchases,
            'total_products': total_products,
            'low_stock_items': low_stock_items,
            'recent_sales': recent_sales,
            'recent_purchases': recent_purchases,
        })
        return context

class BusinessCreateView(LoginRequiredMixin, CreateView):
    model = Business
    form_class = BusinessForm
    template_name = 'core/business_create.html'
    success_url = reverse_lazy('core:dashboard')

    def form_valid(self, form):
        business = form.save()
        # Create or update user profile with the business
        UserProfile.objects.update_or_create(
            user=self.request.user,
            defaults={'business': business}
        )
        messages.success(self.request, 'Business profile created successfully!')
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        # If user already has a business, redirect to dashboard
        if hasattr(request.user, 'userprofile') and request.user.userprofile.business:
            return redirect('core:dashboard')
        return super().get(request, *args, **kwargs)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        # If user has a business, redirect to dashboard
        if hasattr(self.request.user, 'userprofile') and self.request.user.userprofile.business:
            return reverse_lazy('core:dashboard')
        # Otherwise, redirect to business creation
        return reverse_lazy('core:create_business')

# Category Views
@login_required
def category_list(request):
    return render(request, 'core/category_list.html')

@login_required
def category_create(request):
    return render(request, 'core/category_create.html')

@login_required
def category_update(request, pk):
    return render(request, 'core/category_update.html')

@login_required
def category_delete(request, pk):
    return render(request, 'core/category_delete.html')

# SubCategory Views
@login_required
def subcategory_list(request):
    return render(request, 'core/subcategory_list.html')

@login_required
def subcategory_create(request):
    return render(request, 'core/subcategory_create.html')

@login_required
def subcategory_update(request, pk):
    return render(request, 'core/subcategory_update.html')

@login_required
def subcategory_delete(request, pk):
    return render(request, 'core/subcategory_delete.html')

# Product Views
@login_required
def product_list(request):
    return render(request, 'core/product_list.html')

@login_required
def product_create(request):
    return render(request, 'core/product_create.html')

@login_required
def product_update(request, pk):
    return render(request, 'core/product_update.html')

@login_required
def product_delete(request, pk):
    return render(request, 'core/product_delete.html')

# Sale Views
@login_required
def sale_list(request):
    return render(request, 'core/sale_list.html')

@login_required
def sale_create(request):
    return render(request, 'core/sale_create.html')

@login_required
def sale_detail(request, pk):
    return render(request, 'core/sale_detail.html')

@login_required
def sale_update(request, pk):
    return render(request, 'core/sale_update.html')

@login_required
def sale_delete(request, pk):
    return render(request, 'core/sale_delete.html')

# Purchase Views
@login_required
def purchase_list(request):
    return render(request, 'core/purchase_list.html')

@login_required
def purchase_create(request):
    return render(request, 'core/purchase_create.html')

@login_required
def purchase_detail(request, pk):
    return render(request, 'core/purchase_detail.html')

@login_required
def purchase_update(request, pk):
    return render(request, 'core/purchase_update.html')

@login_required
def purchase_delete(request, pk):
    return render(request, 'core/purchase_delete.html')

# Customer Views
@login_required
def customer_list(request):
    return render(request, 'core/customer_list.html')

@login_required
def customer_create(request):
    return render(request, 'core/customer_create.html')

@login_required
def customer_update(request, pk):
    return render(request, 'core/customer_update.html')

@login_required
def customer_delete(request, pk):
    return render(request, 'core/customer_delete.html')

# Supplier Views
@login_required
def supplier_list(request):
    return render(request, 'core/supplier_list.html')

@login_required
def supplier_create(request):
    return render(request, 'core/supplier_create.html')

@login_required
def supplier_update(request, pk):
    return render(request, 'core/supplier_update.html')

@login_required
def supplier_delete(request, pk):
    return render(request, 'core/supplier_delete.html')

# Report Views
@login_required
def profit_loss_report(request):
    return render(request, 'core/profit_loss_report.html')

@login_required
def inventory_report(request):
    return render(request, 'core/inventory_report.html')

@login_required
def sales_report(request):
    return render(request, 'core/sales_report.html')

@login_required
def purchases_report(request):
    return render(request, 'core/purchases_report.html')

# Financial Year Views
@login_required
def financial_year_list(request):
    return render(request, 'core/financial_year_list.html')

@login_required
def financial_year_create(request):
    return render(request, 'core/financial_year_create.html')

@login_required
def financial_year_update(request, pk):
    return render(request, 'core/financial_year_update.html')

@login_required
def financial_year_delete(request, pk):
    return render(request, 'core/financial_year_delete.html')
