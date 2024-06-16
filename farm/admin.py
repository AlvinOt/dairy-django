# farm/admin.py

from django.contrib import admin
from .models import (
    User, Role, UserRole, Farm, Invitation, ApprovalRequest, 
    Cow, MilkingSession, HealthRecord, BreedingRecord, CalvingRecord
)

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('email',)

class CowAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag_number', 'breed', 'farm', 'date_of_birth', 'gender', 'health_status', 'lactation_status')
    search_fields = ('name', 'tag_number', 'breed')
    list_filter = ('farm', 'breed', 'gender', 'health_status', 'lactation_status')
    ordering = ('name',)

class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'status', 'verified', 'created', 'updated')
    search_fields = ('name', 'location')
    list_filter = ('status', 'verified')
    ordering = ('name',)

admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(Farm, FarmAdmin)
admin.site.register(Invitation)
admin.site.register(ApprovalRequest)
admin.site.register(Cow, CowAdmin)
admin.site.register(MilkingSession)
admin.site.register(HealthRecord)
admin.site.register(BreedingRecord)
admin.site.register(CalvingRecord)
