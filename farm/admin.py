from django.contrib import admin
from .models import (
    Farm, Cow, CowMass, MilkingSession, HealthRecord, BreedingRecord, 
    CalvingRecord, Inventory, Expense, Revenue
)

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'status', 'verified', 'created', 'updated')
    search_fields = ('name', 'location', 'status')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Cow)
class CowAdmin(admin.ModelAdmin):
    list_display = ('tag_number', 'name', 'farm', 'breed', 'date_of_birth', 'gender')
    search_fields = ('tag_number', 'name', 'breed', 'farm__name')
    list_filter = ('farm', 'gender')

@admin.register(CowMass)
class CowMassAdmin(admin.ModelAdmin):
    list_display = ('cow', 'mass', 'date_measured')
    search_fields = ('cow__name', 'cow__tag_number')
    list_filter = ('date_measured',)

@admin.register(MilkingSession)
class MilkingSessionAdmin(admin.ModelAdmin):
    list_display = ('cow', 'milk_yield', 'milking_date')
    search_fields = ('cow__name', 'cow__tag_number')
    list_filter = ('milking_date',)

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('cow', 'health_issue', 'treatment_date', 'vet_name', 'vet_company')
    search_fields = ('cow__name', 'cow__tag_number', 'health_issue', 'vet_name', 'vet_company')
    list_filter = ('treatment_date', 'vet_name', 'vet_company')

@admin.register(BreedingRecord)
class BreedingRecordAdmin(admin.ModelAdmin):
    list_display = ('cow', 'breeding_method', 'expected_calving_date', 'last_calving_date', 'no_of_calving')
    search_fields = ('cow__name', 'cow__tag_number', 'breeding_method')
    list_filter = ('breeding_method', 'expected_calving_date', 'last_calving_date')

@admin.register(CalvingRecord)
class CalvingRecordAdmin(admin.ModelAdmin):
    list_display = ('cow', 'calving_date', 'calf_details')
    search_fields = ('cow__name', 'cow__tag_number')
    list_filter = ('calving_date',)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'quantity', 'date_acquired')
    search_fields = ('item_name',)
    list_filter = ('date_acquired',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'date', 'category')
    search_fields = ('description', 'category')
    list_filter = ('date', 'category')

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'date', 'source')
    search_fields = ('description', 'source')
    list_filter = ('date', 'source')
