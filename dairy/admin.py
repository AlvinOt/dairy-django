from django.contrib import admin
from .models import Farm
from .forms import FarmAdminForm

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    form = FarmAdminForm
    list_display = ['name', 'created', 'location', 'status', 'verified']
    list_filter = ['status', 'created', 'verified']
    search_fields = ['name', 'description', 'email', 'phone']
    raw_id_fields = ['managers']
    date_hierarchy = 'created'
    ordering = ['status', 'verified']
