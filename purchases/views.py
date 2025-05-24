from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Count
from django.contrib import messages
from .models import Supplier, Purchase, PurchaseItem
from .forms import SupplierForm, PurchaseForm, PurchaseItemFormSet
from business.views import BusinessRequiredMixin

# Create your views here.

class SupplierListView(BusinessRequiredMixin, ListView):
    model = Supplier
    template_name = 'purchases/supplier_list.html'
    context_object_name = 'suppliers'
    ordering = ['name']

    def get_queryset(self):
        return Supplier.objects.filter(business=self.request.user.userprofile.business)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_suppliers'] = Supplier.objects.filter(business=self.request.user.userprofile.business).count()
        return context

class SupplierCreateView(BusinessRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'purchases/supplier_form.html'
    success_url = reverse_lazy('purchases:supplier_list')

    def form_valid(self, form):
        form.instance.business = self.request.user.userprofile.business
        messages.success(self.request, 'Supplier created successfully.')
        return super().form_valid(form)

class SupplierUpdateView(BusinessRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'purchases/supplier_form.html'
    success_url = reverse_lazy('purchases:supplier_list')

    def get_queryset(self):
        return Supplier.objects.filter(business=self.request.user.userprofile.business)

    def form_valid(self, form):
        form.instance.business = self.request.user.userprofile.business
        messages.success(self.request, 'Supplier updated successfully.')
        return super().form_valid(form)

class SupplierDeleteView(BusinessRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'purchases/supplier_confirm_delete.html'
    success_url = reverse_lazy('purchases:supplier_list')

    def get_queryset(self):
        return Supplier.objects.filter(business=self.request.user.userprofile.business)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Supplier deleted successfully.')
        return super().delete(request, *args, **kwargs)

class SupplierDetailView(BusinessRequiredMixin, DetailView):
    model = Supplier
    template_name = 'purchases/supplier_detail.html'
    context_object_name = 'supplier'

    def get_queryset(self):
        return Supplier.objects.filter(business=self.request.user.userprofile.business)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier = self.get_object()
        
        purchase_stats = Purchase.objects.filter(supplier=supplier, business=self.request.user.userprofile.business).aggregate(
            total_purchases=Count('id'),
            total_amount=Sum('final_amount'),
            total_paid=Sum('paid_amount')
        )
        
        recent_purchases = Purchase.objects.filter(
            supplier=supplier, business=self.request.user.userprofile.business
        ).order_by('-date')[:5]
        
        payment_status = Purchase.objects.filter(
            supplier=supplier, business=self.request.user.userprofile.business
        ).values('payment_status').annotate(
            count=Count('id')
        )
        
        context.update({
            'purchase_stats': purchase_stats,
            'recent_purchases': recent_purchases,
            'payment_status': payment_status,
            'purchases': Purchase.objects.filter(supplier=supplier, business=self.request.user.userprofile.business).order_by('-date')
        })
        return context

class PurchaseListView(BusinessRequiredMixin, ListView):
    model = Purchase
    template_name = 'purchases/purchase_list.html'
    context_object_name = 'purchases'
    ordering = ['-date']

    def get_queryset(self):
        return Purchase.objects.filter(business=self.request.user.userprofile.business)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_purchases'] = Purchase.objects.filter(business=self.request.user.userprofile.business).aggregate(
            total=Sum('final_amount')
        )['total'] or 0
        return context

class PurchaseCreateView(BusinessRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'purchases/purchase_form.html'
    success_url = reverse_lazy('purchases:purchase_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PurchaseItemFormSet(self.request.POST, instance=self.object, form_kwargs={'user': self.request.user})
        else:
            context['formset'] = PurchaseItemFormSet(instance=self.object, form_kwargs={'user': self.request.user})
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        form.instance.business = self.request.user.userprofile.business
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Purchase created successfully.')
            return redirect(self.success_url)
        return self.render_to_response(self.get_context_data(form=form))

class PurchaseUpdateView(BusinessRequiredMixin, UpdateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'purchases/purchase_form.html'
    success_url = reverse_lazy('purchases:purchase_list')

    def get_queryset(self):
        return Purchase.objects.filter(business=self.request.user.userprofile.business)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PurchaseItemFormSet(self.request.POST, instance=self.object, form_kwargs={'user': self.request.user})
        else:
            context['formset'] = PurchaseItemFormSet(instance=self.object, form_kwargs={'user': self.request.user})
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        form.instance.business = self.request.user.userprofile.business
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Purchase updated successfully.')
            return redirect(self.success_url)
        return self.render_to_response(self.get_context_data(form=form))

class PurchaseDeleteView(BusinessRequiredMixin, DeleteView):
    model = Purchase
    template_name = 'purchases/purchase_confirm_delete.html'
    success_url = reverse_lazy('purchases:purchase_list')

    def get_queryset(self):
        return Purchase.objects.filter(business=self.request.user.userprofile.business)

class PurchaseDetailView(LoginRequiredMixin, DetailView):
    model = Purchase
    template_name = 'purchases/purchase_detail.html'
    context_object_name = 'purchase'

    def get_queryset(self):
        return Purchase.objects.filter(business=self.request.user.userprofile.business)
