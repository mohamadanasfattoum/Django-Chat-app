from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .form import ProfileForm


# Create your views here.
def profile(request):
    profile = request.user.profile
    return render(request, 'users/profile.html',{'profile': profile})

@login_required
def edit_profile(request):
    form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    return render(request, 'users/edit_profile.html', {'form': form})
 