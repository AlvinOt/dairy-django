from django import forms
from django.contrib import admin
from .models import Farm

class FarmAdminForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = '__all__'
        widgets = {
            'slug': forms.HiddenInput(),  # Hide the slug field in the admin form
        }
