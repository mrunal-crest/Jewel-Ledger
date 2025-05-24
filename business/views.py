from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import BusinessForm
from .models import Business

class BusinessRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
            
        # Check if the user has a business linked
        if not hasattr(request.user, 'userprofile') or not request.user.userprofile.business:
            # Show a warning message instead of redirecting
            messages.warning(request, "Your account is not linked to a business profile. Please ensure your business was created during registration.")
            # The automatic redirection is removed here:
            # return redirect('business:business_create')
            
        return super().dispatch(request, *args, **kwargs)

class BusinessListView(LoginRequiredMixin, ListView):
    model = Business
    template_name = 'business/business_list.html'
    context_object_name = 'businesses'

    def get_queryset(self):
        # Filter businesses by the current user as the owner
        return Business.objects.filter(owner=self.request.user)

class BusinessCreateView(LoginRequiredMixin, CreateView):
    model = Business
    form_class = BusinessForm
    template_name = 'business/business_form.html'
    success_url = reverse_lazy('dashboard') # Redirect to dashboard after creation

    def dispatch(self, request, *args, **kwargs):
        # If the user already has a business, redirect them away from the creation page
        if request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.business:
            messages.info(request, "You already have a business associated with your account.")
            return redirect('dashboard') # Or wherever appropriate
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        # Link the created business to the user's profile
        self.request.user.userprofile.business = self.object
        self.request.user.userprofile.save()
        messages.success(self.request, 'Business created successfully!')
        return response

class BusinessUpdateView(LoginRequiredMixin, UpdateView):
    model = Business
    form_class = BusinessForm
    template_name = 'business/business_form.html'
    success_url = reverse_lazy('business:business_detail')
    context_object_name = 'business'

    def get_object(self, queryset=None):
        # Get the business associated with the logged-in user's profile
        # Ensure the user has a business linked before trying to get it
        if hasattr(self.request.user, 'userprofile') and self.request.user.userprofile.business:
            return self.request.user.userprofile.business
        # If no business is linked, return None or raise an appropriate exception
        # Depending on desired behavior when accessing /business/edit/ without a business
        # For now, returning None might lead to a 404 if the template expects an object
        # A better approach might be to redirect to business creation or dashboard here too.
        # However, based on the mixin change above, the mixin will handle the lack of business.
        return None # The mixin should prevent reaching here without a business.

    def form_valid(self, form):
        messages.success(self.request, 'Business updated successfully!')
        return super().form_valid(form)

class BusinessDeleteView(LoginRequiredMixin, DeleteView):
    model = Business
    template_name = 'business/business_confirm_delete.html'
    success_url = reverse_lazy('business:business_list')

    def get_queryset(self):
        # Ensure only businesses owned by the current user are deletable
        return Business.objects.filter(owner=self.request.user)

class BusinessDetailView(LoginRequiredMixin, DetailView):
    model = Business
    template_name = 'business/business_detail.html'
    context_object_name = 'business'

    def get_object(self, queryset=None):
        # Get the business associated with the logged-in user's profile
        # Ensure the user has a business linked before trying to get it
        if hasattr(self.request.user, 'userprofile') and self.request.user.userprofile.business:
            return self.request.user.userprofile.business
        # If no business is linked, return None or raise an appropriate exception
        return None # The mixin should prevent reaching here without a business.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = self.get_object() # Get the business object

        if business:
            # Get business statistics if business object exists
            context['total_sales'] = business.sales.count()
            context['total_purchases'] = business.purchases.count()
            context['total_products'] = business.products.count()
            context['total_customers'] = business.customers.count()
            context['total_suppliers'] = business.suppliers.count()
        else:
            # Provide default or empty data if business is None (though mixin should prevent this)
            context['total_sales'] = 0
            context['total_purchases'] = 0
            context['total_products'] = 0
            context['total_customers'] = 0
            context['total_suppliers'] = 0
            
        return context 