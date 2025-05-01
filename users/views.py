from django.shortcuts import render

# Create your views here.
def profile(request):
    profile = request.user.profile
    return render(request, 'users/profile.html',{'profile': profile})
 