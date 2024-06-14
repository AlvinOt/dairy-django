from django.contrib import admin
from .models import Farm
from .forms import FarmForm

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    form = FarmForm  # Use the custom form
    list_display = ['name', 'location', 'status', 'verified']
    list_filter = ['status', 'created', 'verified']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ['managers']
