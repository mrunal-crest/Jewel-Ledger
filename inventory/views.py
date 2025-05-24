from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Count
from django.db.models import Sum, Count, F
from django.contrib import messages
from .models import Category, SubCategory, Product
from .forms import CategoryForm, SubCategoryForm, ProductForm
from business.views import BusinessRequiredMixin

# Create your views here.


class CategoryListView(BusinessRequiredMixin, ListView):
    model = Category
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        # Filter categories by the user's business
        return Category.objects.filter(business=self.request.user.userprofile.business)

class CategoryCreateView(BusinessRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('inventory:category_list')

    def form_valid(self, form):
        # Assign the business to the category before saving
        form.instance.business = self.request.user.userprofile.business
        messages.success(self.request, 'Category created successfully.')
        return super().form_valid(form)

class CategoryUpdateView(BusinessRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('inventory:category_list')

    def get_queryset(self):
        # Ensure only categories belonging to the user's business are editable
        return Category.objects.filter(business=self.request.user.userprofile.business)

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully.')
        return super().form_valid(form)

class CategoryDeleteView(BusinessRequiredMixin, DeleteView):
    model = Category
    template_name = 'inventory/category_confirm_delete.html'
    success_url = reverse_lazy('inventory:category_list')

    def get_queryset(self):
        # Ensure only categories belonging to the user's business are deletable
        return Category.objects.filter(business=self.request.user.userprofile.business)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Category deleted successfully.')
        return super().delete(request, *args, **kwargs)

class SubCategoryListView(BusinessRequiredMixin, ListView):
    model = SubCategory
    template_name = 'inventory/subcategory_list.html'
    context_object_name = 'subcategories'

    def get_queryset(self):
        # Filter subcategories by the user's business through the category
        return SubCategory.objects.filter(category__business=self.request.user.userprofile.business)

class SubCategoryCreateView(BusinessRequiredMixin, CreateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'inventory/subcategory_form.html'
    success_url = reverse_lazy('inventory:subcategory_list')

    def form_valid(self, form):
        # The form should handle filtering categories by business, so the category on the form instance should be correct
        # Assign the business to the subcategory before saving
        form.instance.business = self.request.user.userprofile.business
        messages.success(self.request, 'Subcategory created successfully.')
        return super().form_valid(form)

class SubCategoryUpdateView(BusinessRequiredMixin, UpdateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'inventory/subcategory_form.html'
    success_url = reverse_lazy('inventory:subcategory_list')

    def get_queryset(self):
        # Ensure only subcategories belonging to the user's business are editable
        return SubCategory.objects.filter(category__business=self.request.user.userprofile.business)

    def form_valid(self, form):
        messages.success(self.request, 'Subcategory updated successfully.')
        return super().form_valid(form)

class SubCategoryDeleteView(BusinessRequiredMixin, DeleteView):
    model = SubCategory
    template_name = 'inventory/subcategory_confirm_delete.html'
    success_url = reverse_lazy('inventory:subcategory_list')

    def get_queryset(self):
        # Ensure only subcategories belonging to the user's business are deletable
        return SubCategory.objects.filter(category__business=self.request.user.userprofile.business)

class ProductListView(BusinessRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Filter products by the user's business
        return Product.objects.filter(business=self.request.user.userprofile.business)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = self.request.user.userprofile.business

        context['total_products'] = Product.objects.filter(business=business).count()
        context['low_stock_products'] = Product.objects.filter(
            business=business, stock_quantity__lte=10
        ).count()

        # Correct expression for total inventory value (stock_quantity * price_per_gram)
        total_value_agg = Product.objects.filter(business=business).annotate(
            item_value=ExpressionWrapper(
                F('stock_quantity') * F('price_per_gram'),
                output_field=DecimalField(max_digits=20, decimal_places=2)
            )
        ).aggregate(total=Sum('item_value'))

        context['total_value'] = total_value_agg['total'] or 0

        return context

class ProductCreateView(BusinessRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('inventory:product_list')

    def form_valid(self, form):
        form.instance.business = self.request.user.userprofile.business
        messages.success(self.request, 'Product created successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid:", form.errors)
        messages.error(self.request, "Failed to create product. Please check the form.")
        return super().form_invalid(form)


class ProductUpdateView(BusinessRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('inventory:product_list')

    def get_queryset(self):
        # Ensure only products belonging to the user's business are editable
        return Product.objects.filter(business=self.request.user.userprofile.business)

    def form_valid(self, form):
        messages.success(self.request, 'Product updated successfully.')
        return super().form_valid(form)

class ProductDeleteView(BusinessRequiredMixin, DeleteView):
    model = Product
    template_name = 'inventory/product_confirm_delete.html'
    success_url = reverse_lazy('inventory:product_list')

    def get_queryset(self):
        # Ensure only products belonging to the user's business are deletable
        return Product.objects.filter(business=self.request.user.userprofile.business)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Product deleted successfully.')
        return super().delete(request, *args, **kwargs)

class ProductDetailView(BusinessRequiredMixin, DetailView):
    model = Product
    template_name = 'inventory/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        # Ensure only products belonging to the user's business are viewable
        return Product.objects.filter(business=self.request.user.userprofile.business)
