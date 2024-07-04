from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from datetime import date  #std lib

# Farm Model
class Farm(models.Model):
    name = models.CharField(max_length=100, unique=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farms_managed')
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True)
    slogan = models.CharField(max_length=255, blank=True, help_text='Farm motto')
    email = models.EmailField(max_length=254, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)  # This represents the verification status

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('mashamba:farm_detail', kwargs={'slug': self.slug})


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name



class ProductService(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='products_services')
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} - {self.farm.name}"

# Cow Model
class Cow(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    name_or_tag = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100, unique=True, blank=True)
    breed = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    mass = models.FloatField(blank=True, null=True)
    updated = models.DateField(blank=True, default=date.today)


    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            delta = today - self.date_of_birth
            years = delta.days // 365
            months = (delta.days % 365) // 30
            return f"{years} years, {months} months"
        return None


    def save(self, *args, **kwargs):
        if not self.identifier:
            super().save(*args, **kwargs)  # Save the instance to generate a pk
            self.identifier = f'Cow-{self.pk}'  # Example: Cow-1, Cow-2, etc.
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name_or_tag

# MilkingSession Model
class MilkingSession(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='milking_sessions')
    milk_yield = models.DecimalField(max_digits=6, decimal_places=2)
    milking_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.cow} - {self.milk_yield} on {self.milking_time}"


# HealthRecord Model
class HealthRecord(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    health_issue = models.CharField(max_length=255)
    treatment = models.CharField(max_length=255)
    treatment_date = models.DateField(default=date.today)
    notes = models.TextField(blank=True)
    vet_name = models.CharField(max_length=100)
    vet_company = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.cow} - {self.health_issue} treated on {self.treatment_date}"


# BreedingRecord Model
class BreedingRecord(models.Model):
    BREEDING_METHOD_CHOICES = [
        ('AI', 'Artificial Insemination'),
        ('Natural', 'Natural Mating')
    ]

    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    breeding_method = models.CharField(max_length=100, choices=BREEDING_METHOD_CHOICES)
    bull_name = models.CharField(max_length=100, blank=True)  # Make bull_name optional
    bull_code = models.CharField(max_length=100, blank=True)  # Make bull_code optional
    expected_calving_date = models.DateField(blank=True, null=True)
    repeat_breeding_date = models.DateField(blank=True, null=True)
    last_calving_date = models.DateField(blank=True, null=True)  # Make last_calving_date optional
    no_of_calving = models.IntegerField(blank=True, null=True)  # Make no_of_calving optional
    inseminator_name = models.CharField(max_length=100, blank=True)  # Make inseminator_name optional for AI


    def __str__(self):
        return f"{self.cow} - {self.breeding_method} - Expected Calving: {self.expected_calving_date}"


# CalvingRecord Model
class CalvingRecord(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    calving_date = models.DateField(default=date.today)
    calf_details = models.TextField(help_text="Enter details about the calf.")
    birthing_details = models.TextField(blank=True, null=True, help_text="Enter details about the birthing process (optional).")


    def __str__(self):
        return f"{self.cow} - Calving on {self.calving_date}"


# Inventory Model
class Inventory(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date_acquired = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.item_name} - {self.quantity} units"

    class Meta:
        verbose_name_plural = 'inventories'


# Expense Model
class Expense(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} - {self.cost} on {self.date}"


# Revenue Model
class Revenue(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.name} - {self.cost} on {self.date}"
