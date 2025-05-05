from django.forms import ModelForm # Import ModelForm for creating forms based on models
from django import forms # Import forms for creating custom forms
from .models import GroupMessages , ChatGroup # Import the models for which we will create forms


class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessages # Specify the model to create a form for
        fields = ['body'] # Specify the fields to include in the form
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Add message ...', 'class':'p-4 text-black', 'maxlength': '300', 'autofocus': True }), # Custom widget for the body field
        }