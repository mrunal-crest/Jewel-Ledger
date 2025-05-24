from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Count
from django.contrib import messages
from django.utils import timezone
from .models import Customer, Sale, SaleItem
from .forms import CustomerForm, SaleForm, SaleItemFormSet
from business.views import BusinessRequiredMixin # Import the mixin

# Create your views here.

class CustomerListView(BusinessRequiredMixin, ListView):
    model = Customer
    template_name = 'sales/customer_list.html'
    context_object_name = 'customers'
    ordering = ['name']

    def get_queryset(self):
        # Ensure only customers belonging to the user's business are listed
        return Customer.objects.filter(business=self.request.user.userprofile.business)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter total customers by the user's business
        context['total_customers'] = Customer.objects.filter(business=self.request.user.userprofile.business).count()
        return context

class CustomerDetailView(BusinessRequiredMixin, DetailView):
    model = Customer
    template_name = 'sales/customer_detail.html'
    context_object_name = 'customer'

    def get_queryset(self):
        # Ensure only customers belonging to the user's business are viewable
        return Customer.objects.filter(business=self.request.user.userprofile.business)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        
        # Get customer's sales statistics, filtered by business
        sales_stats = Sale.objects.filter(customer=customer, business=self.request.user.userprofile.business).aggregate(
            total_sales=Count('id'),
            total_amount=Sum('final_amount'),
            total_paid=Sum('paid_amount')
        )
        
        # Get recent sales, filtered by business
        recent_sales = Sale.objects.filter(
            customer=customer, business=self.request.user.userprofile.business
        ).order_by('-date')[:5]
        
        # Calculate payment status distribution, filtered by business
        payment_status = Sale.objects.filter(
            customer=customer, business=self.request.user.userprofile.business
        ).values('payment_status').annotate(
            count=Count('id')
        )
        
        context.update({
            'sales_stats': sales_stats,
            'recent_sales': recent_sales,
            'payment_status': payment_status,
            'sales': Sale.objects.filter(customer=customer, business=self.request.user.userprofile.business).order_by('-date')
        })
        return context

class CustomerCreateView(BusinessRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'sales/customer_form.html'
    success_url = reverse_lazy('sales:customer_list')

    def form_valid(self, form):
        # Assign the business to the customer before saving
        form.instance.business = self.request.user.userprofile.business
        messages.success(self.request, 'Customer created successfully.')
        return super().form_valid(form)

class CustomerUpdateView(BusinessRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'sales/customer_form.html'
    success_url = reverse_lazy('sales:customer_list')

    def get_queryset(self):
        # Ensure only customers belonging to the user's business are editable
        return Customer.objects.filter(business=self.request.user.userprofile.business)

    def form_valid(self, form):
        # Assign the business to the customer (should already be set by get_queryset, but good practice)
        form.instance.business = self.request.user.userprofile.business
        messages.success(self.request, 'Customer updated successfully.')
        return super().form_valid(form)

class CustomerDeleteView(BusinessRequiredMixin, DeleteView):
    model = Customer
    template_name = 'sales/customer_confirm_delete.html'
    success_url = reverse_lazy('sales:customer_list')

    def get_queryset(self):
        # Ensure only customers belonging to the user's business are deletable
        return Customer.objects.filter(business=self.request.user.userprofile.business)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Customer deleted successfully.')
        return super().delete(request, *args, **kwargs)

class SaleListView(BusinessRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/sale_list.html'
    context_object_name = 'sales'
    ordering = ['-date']

    def get_queryset(self):
        # Ensure only sales belonging to the user's business are listed
        return Sale.objects.filter(business=self.request.user.userprofile.business)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter total sales by the user's business
        context['total_sales'] = Sale.objects.filter(business=self.request.user.userprofile.business).aggregate(
            total=Sum('final_amount')
        )['total'] or 0
        return context

class SaleCreateView(BusinessRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sales:sale_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the user to the form to filter customer and product choices
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            # Pass the user to the formset to filter product choices
            context['formset'] = SaleItemFormSet(self.request.POST, instance=self.object, form_kwargs={'user': self.request.user})
        else:
            # Pass the user to the formset to filter product choices
            context['formset'] = SaleItemFormSet(instance=self.object, form_kwargs={'user': self.request.user})
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        # Assign the business to the sale before saving
        form.instance.business = self.request.user.userprofile.business
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Sale created successfully.')
            return redirect(self.success_url)
        # If formset is invalid, re-render the form with errors
        return self.render_to_response(self.get_context_data(form=form))

class SaleUpdateView(BusinessRequiredMixin, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sales:sale_list')

    def get_queryset(self):
        # Ensure only sales belonging to the user's business are editable
        return Sale.objects.filter(business=self.request.user.userprofile.business)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the user to the form to filter customer and product choices
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
             # Pass the user to the formset to filter product choices
            context['formset'] = SaleItemFormSet(self.request.POST, instance=self.object, form_kwargs={'user': self.request.user})
        else:
            # Pass the user to the formset to filter product choices
            context['formset'] = SaleItemFormSet(instance=self.object, form_kwargs={'user': self.request.user})
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        # Assign the business to the sale (should already be set by get_queryset, but good practice)
        form.instance.business = self.request.user.userprofile.business
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Sale updated successfully.')
            return redirect(self.success_url)
        # If formset is invalid, re-render the form with errors
        return self.render_to_response(self.get_context_data(form=form))

class SaleDeleteView(BusinessRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sales/sale_confirm_delete.html'
    success_url = reverse_lazy('sales:sale_list')

    def get_queryset(self):
        # Ensure only sales belonging to the user's business are deletable
        return Sale.objects.filter(business=self.request.user.userprofile.business)

class SaleDetailView(BusinessRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/sale_detail.html'
    context_object_name = 'sale'

    def get_queryset(self):
        # Ensure only sales belonging to the user's business are viewable
        return Sale.objects.filter(business=self.request.user.userprofile.business)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sale = self.get_object()
        
        # Calculate item totals
        items = sale.items.all().annotate(
            total=ExpressionWrapper(
                F('quantity') * F('price'),
                output_field=DecimalField()
            )
        )
        
        # Calculate payment statistics
        payment_stats = {
            'total_amount': sale.final_amount,
            'paid_amount': sale.paid_amount,
            'remaining_amount': sale.final_amount - sale.paid_amount,
            'payment_percentage': (sale.paid_amount / sale.final_amount * 100) if sale.final_amount > 0 else 0
        }
        
        # Get customer's purchase history, filtered by business
        customer_history = Sale.objects.filter(
            customer=sale.customer, business=self.request.user.userprofile.business
        ).exclude(
            pk=sale.pk
        ).order_by('-date')[:5]
        
        context.update({
            'items': items,
            'payment_stats': payment_stats,
            'customer_history': customer_history,
            'days_since_sale': (timezone.now().date() - sale.date).days
        })
        return context
