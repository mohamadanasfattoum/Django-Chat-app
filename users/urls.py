from django.urls import path

from .views import profile, edit_profile, profile_settings, profile_emailchange, profile_emailverify

urlpatterns = [
    path('', profile, name='profile'),
    path('edit/', edit_profile, name='edit_profile'),
    path('onboarding/', edit_profile, name='profile-onboarding'),
    path('settings/', profile_settings, name='profile-settings'),
    path('emailchange/', profile_emailchange, name='profile-emailchange'),
    path('emailverify/', profile_emailverify, name='profile-emailverify'),

]