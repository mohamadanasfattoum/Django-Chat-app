from django.urls import path

from .views import profile, edit_profile, profile_settings

urlpatterns = [
    path('', profile, name='profile'),
    path('edit/', edit_profile, name='edit_profile'),
    path('onboarding/', edit_profile, name='profile-onboarding'),
    path('settings/', profile_settings, name='profile_settings'),

]