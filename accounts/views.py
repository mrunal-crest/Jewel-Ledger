from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, BusinessCreationForm, UserProfileForm
from .models import UserProfile
from business.models import Business

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        business_form = BusinessCreationForm(request.POST)
        
        if user_form.is_valid() and business_form.is_valid():
            user = user_form.save()
            business = business_form.save(commit=False)
            business.owner = user
            business.save()
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                business=business,
                phone=user_form.cleaned_data.get('phone', ''),
                address=user_form.cleaned_data.get('address', ''),
                role=user_form.cleaned_data.get('role', '')
            )
            
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('core:dashboard')
    else:
        user_form = UserRegistrationForm()
        business_form = BusinessCreationForm()
    
    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'business_form': business_form
    })

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
            
            # Update user's profile with new business
            profile = request.user.userprofile
            profile.business = business
            profile.save()
            
            messages.success(request, 'Business created successfully!')
            return redirect('core:dashboard')
    else:
        form = BusinessCreationForm()
    
    return render(request, 'accounts/create_business.html', {'form': form})
