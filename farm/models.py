from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date  # Import date from datetime module
from django.utils import timezone


class FutureDateValidatorMixin:
    def clean_future_date(self, field_name):
        date_value = getattr(self, field_name)
        if date_value and date_value > date.today():
            raise ValidationError(f"{field_name.capitalize()} cannot be in the future.")


def get_default_milking_date():
    return timezone.now().date()


# Farm Model
class Farm(models.Model):
    STATUS_CHOICES = [
        ('ACT', 'Active'),
        ('INA', 'Inactive')
    ]

    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True)
    slogan = models.CharField(max_length=255, blank=True, null=True, help_text='Farm motto')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='INA')
    verified = models.BooleanField(default=False)  # This represents the verification status

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Cow Model
class Cow(models.Model, FutureDateValidatorMixin):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    tag_number = models.CharField(max_length=50, unique=True)
    breed = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            delta = today - self.date_of_birth
            years = delta.days // 365
            months = (delta.days % 365) // 30
            return f"{years} years, {months} months"
        return None

    def clean(self):
        super().clean()
        if not self.tag_number and not self.name:
            raise ValidationError("Either 'tag_number' or 'name' must be provided.")

        self.clean_future_date('date_of_birth')  # Validate date_of_birth against future date

    def __str__(self):
        return self.name or self.tag_number

# CowMass Model
class CowMass(models.Model, FutureDateValidatorMixin):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)  # Changed to ForeignKey
    mass = models.FloatField(blank=True, null=True)
    date_measured = models.DateField(blank=True, null=True)

    def clean(self):
        super().clean()
        self.clean_future_date('date_measured')  # Validate date_measured against future date

    def __str__(self):
        return f"{self.cow.name or self.cow.tag_number} - Mass: {self.mass}"


# MilkingSession Model
class MilkingSession(models.Model, FutureDateValidatorMixin):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    milk_yield = models.DecimalField(max_digits=6, decimal_places=2)
    milking_date = models.DateField(default=get_default_milking_date)

    def clean(self):
        super().clean()
        self.clean_future_date('milking_date')  # Validate milking_date against future date

    def __str__(self):
        return f"{self.cow.name or self.cow.tag_number} - Milking Session: {self.milking_date}"


# HealthRecord Model
class HealthRecord(models.Model, FutureDateValidatorMixin):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    health_issue = models.CharField(max_length=100)
    treatment = models.TextField()
    treatment_date = models.DateField()
    notes = models.TextField(blank=True)
    vet_name = models.CharField(max_length=100, default='Unknown')
    vet_company = models.CharField(max_length=100, default='Unknown')

    def clean(self):
        super().clean()
        self.clean_future_date('treatment_date')  # Validate treatment_date against future date

    def __str__(self):
        return f"{self.cow.name or self.cow.tag_number} - Health Record: {self.health_issue}"


# BreedingRecord Model
class BreedingRecord(models.Model):
    BREEDING_METHOD_CHOICES = [
        ('AI', 'Artificial Insemination'),
        ('Natural', 'Natural Mating')
    ]

    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    breeding_method = models.CharField(max_length=100, choices=BREEDING_METHOD_CHOICES)
    mating_bull = models.CharField(max_length=100, blank=True)  # Make mating_bull optional
    bull_name = models.CharField(max_length=100, blank=True)  # Make bull_name optional
    bull_code = models.CharField(max_length=100, blank=True)  # Make bull_code optional
    expected_calving_date = models.DateField()
    last_calving_date = models.DateField(blank=True, null=True)  # Make last_calving_date optional
    no_of_calving = models.IntegerField(blank=True, null=True)  # Make no_of_calving optional
    inseminator_name = models.CharField(max_length=100, blank=True)  # Make inseminator_name optional for AI

    def clean(self):
        super().clean()
        if self.breeding_method == 'AI' and not self.inseminator_name:
            raise ValidationError("Inseminator name is required for Artificial Insemination.")

    def __str__(self):
        return f"{self.cow.name or self.cow.tag_number} - Breeding Record"


# CalvingRecord Model
class CalvingRecord(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    calving_date = models.DateField()
    calf_details = models.TextField(help_text="Enter details about the calf.")
    birthing_details = models.TextField(blank=True, null=True, help_text="Enter details about the birthing process (optional).")

    def __str__(self):
        return f"{self.cow.name or self.cow.tag_number} - Calving Record"


# Inventory Model
class Inventory(models.Model, FutureDateValidatorMixin):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    date_acquired = models.DateField()

    def clean(self):
        super().clean()
        self.clean_future_date('date_acquired')  # Validate date_acquired against future dates

    def __str__(self):
        return f"{self.item_name} - Quantity: {self.quantity}"


# Expense Model
class Expense(models.Model, FutureDateValidatorMixin):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=100)

    def clean(self):
        super().clean()
        self.clean_future_date('date')  # Validate 'date' against future dates

    def __str__(self):
        return f"Expense: {self.description} - Amount: {self.amount}"


# Revenue Model
class Revenue(models.Model, FutureDateValidatorMixin):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    source = models.CharField(max_length=100)

    def clean(self):
        super().clean()
        self.clean_future_date('date')  # Validate 'date' against future dates

    def __str__(self):
        return f"Revenue: {self.description} - Amount: {self.amount}"
