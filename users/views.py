from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .form import ProfileForm, EmailForm



# Create your views here.
def profile(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect('account_login')  
                 
    return render(request, 'users/profile.html',{'profile': profile})

@login_required
def edit_profile(request):
    form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        
    if request.path == reverse('profile-onboarding'):
        onboarding = True
    else:
        onboarding = False

    return render(request, 'users/edit_profile.html', {'form': form, 'onboarding': onboarding})
 


@login_required
def profile_settings(request):
    return render(request, 'users/profile_settings.html')

@login_required
def profile_emailchange(request): # email change
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form': form})
    
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                # Email already in use by another user
                # Add an error to the form   
                messages.warning(request, f'{email} already in use')
                return redirect('profile-settings')
            form.save()
            # than Signal updates emailaddress and set verified to 
            send_email_confirmation(request, request.user)
            return redirect('profile-settings')
        else:
            # Form is not valid, handle the errors
            messages.warning(request, 'Email is not valid')
            return redirect('profile-settings')
        
    return redirect('home')


@login_required 
def profile_emailverify(request): # email verification
    send_email_confirmation(request, request.user) # send email confirmation
    return redirect('profile-settings')


@login_required
def profile_delete(request):
    user = request.user
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('home')
    return render(request, 'users/profile_delete.html')
