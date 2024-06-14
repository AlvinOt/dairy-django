from django.contrib import admin
from .models import Farm


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'status', 'verified']
    list_filter = ['status', 'created', 'verified']
    search_fields = ['name', 'description']
    raw_id_fields = ['managers']
    date_hierarchy = 'created'
    ordering = ['status', 'verified']
