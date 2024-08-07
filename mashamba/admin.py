from django.contrib import admin
from .models import (
    Farm, Cow, MilkingSession, HealthRecord,
    BreedingRecord, CalvingRecord, Inventory, Expense, Revenue, ProductService
)
from .forms import MilkingSessionForm, BreedingRecordForm, CalvingRecordForm  # Import your custom forms here

# Register your models and associate custom forms with admin models

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'location', 'active', 'verified', 'created', 'updated')
    list_filter = ('active', 'verified', 'created', 'updated')
    search_fields = ('name', 'location', 'manager__username')


@admin.register(ProductService)
class ProductServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'farm', 'price')  # Fields to display in the admin list view
    list_filter = ('farm',)  # Filter options in the admin
    search_fields = ('name', 'farm__name')


@admin.register(Cow)
class CowAdmin(admin.ModelAdmin):
    list_display = ('name_or_tag', 'farm', 'breed', 'gender', 'date_of_birth')
    list_filter = ('gender', 'breed', 'farm')
    search_fields = ('name_or_tag', 'farm__name')


@admin.register(MilkingSession)
class MilkingSessionAdmin(admin.ModelAdmin):
    list_display = ('cow', 'milk_yield', 'milking_time')
    list_filter = ('milking_time',)
    form = MilkingSessionForm  # Associate MilkingSessionForm with MilkingSessionAdmin

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('cow', 'health_issue', 'treatment_date', 'vet_name', 'vet_company')
    list_filter = ('treatment_date', 'vet_name', 'vet_company')
    search_fields = ('cow__name_or_tag', 'health_issue')

@admin.register(BreedingRecord)
class BreedingRecordAdmin(admin.ModelAdmin):
    list_display = ('cow', 'breeding_method', 'bull_name', 'expected_calving_date')
    list_filter = ('breeding_method', 'expected_calving_date')
    search_fields = ('cow__name_or_tag', 'bull_name')
    form = BreedingRecordForm  # Associate BreedingRecordForm with BreedingRecordAdmin

@admin.register(CalvingRecord)
class CalvingRecordAdmin(admin.ModelAdmin):
    list_display = ('cow', 'calving_date', 'calf_details')
    list_filter = ('calving_date',)
    search_fields = ('cow__name_or_tag', 'calf_details')
    form = CalvingRecordForm  # Associate CalvingRecordForm with CalvingRecordAdmin

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'quantity', 'date_acquired')
    list_filter = ('date_acquired',)
    search_fields = ('item_name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'date', 'category')
    list_filter = ('date', 'category')
    search_fields = ('name', 'category')

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'date', 'description')
    list_filter = ('date',)
    search_fields = ('name', 'description')
