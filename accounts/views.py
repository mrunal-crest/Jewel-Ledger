from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .forms import CustomUserCreationForm, CustomAuthenticationForm, BusinessCreationForm, UserProfileForm
from .models import UserProfile
from business.models import Business
from inventory.models import Product
from sales.models import Sale
from purchases.models import Purchase

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:create_business')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if Business.objects.filter(owner=user).exists():
                    return redirect('accounts:dashboard')
                return redirect('accounts:create_business')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def create_business(request):
    if request.method == 'POST':
        form = BusinessCreationForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()
            return redirect('accounts:dashboard')
    else:
        form = BusinessCreationForm()
    return render(request, 'accounts/create_business.html', {'form': form})

@login_required
def dashboard(request):
    # Get user's business
    business = Business.objects.filter(owner=request.user).first()
    if not business:
        return redirect('accounts:create_business')

    # Get date range for analytics
    today = timezone.now()
    thirty_days_ago = today - timedelta(days=30)

    # Compute total inventory value in Python
    products = Product.objects.filter(business=business)
    total_inventory_value = sum([product.total_price for product in products])

    # Monthly sales total
    monthly_sales = Sale.objects.filter(
        business=business,
        date__gte=thirty_days_ago
    ).aggregate(
        total=Sum('final_amount')
    )['total'] or 0

    # Total product count
    total_products = products.count()

    # Pending orders (if 'status' field added to Purchase)
    # Comment out or adjust this block if 'status' is not implemented
    pending_orders = Purchase.objects.filter(
        business=business,
        status='pending'  # This assumes you’ve added a `status` CharField
    ).count()

    # Recent activities
    recent_activities = []

    # Recent sales
    recent_sales = Sale.objects.filter(
        business=business
    ).order_by('-date')[:5]

    for sale in recent_sales:
        recent_activities.append({
            'date': sale.date,
            'description': f"Sale to {sale.customer.name}",
            'amount': sale.final_amount,
            'status': 'Completed'
        })

    # Recent purchases
    recent_purchases = Purchase.objects.filter(
        business=business
    ).order_by('-date')[:5]

    for purchase in recent_purchases:
        recent_activities.append({
            'date': purchase.date,
            'description': f"Purchase from {purchase.supplier.name}",
            'amount': purchase.final_amount,
            'status': getattr(purchase, 'status', 'N/A')
        })

    # Sort activities by date
    recent_activities.sort(key=lambda x: x['date'], reverse=True)
    recent_activities = recent_activities[:10]

    context = {
        'business': business,
        'total_inventory_value': total_inventory_value,
        'monthly_sales': monthly_sales,
        'total_products': total_products,
        'pending_orders': pending_orders,
        'recent_activities': recent_activities,
    }

    return render(request, 'accounts/dashboard.html', context)
