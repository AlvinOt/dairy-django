from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.core.validators import MinValueValidator
import uuid

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    roles = models.ManyToManyField('Role', through='UserRole')
    username = None  # Remove the default username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='farm_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='farm_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = UserManager()

# Role Model
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# UserRole Model
class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    farm = models.ForeignKey('Farm', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'role', 'farm')

# Farm Model
class Farm(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True)
    slogan = models.CharField(max_length=255, blank=True, null=True, help_text='Farm motto')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=3, choices=[('ACT', 'Active'), ('INA', 'Inactive')], default='INA')
    verified = models.BooleanField(default=False)
    users = models.ManyToManyField(User, through='UserRole', related_name='farms')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Invitation Model
class Invitation(models.Model):
    email = models.EmailField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True, blank=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} invited to {self.farm} as {self.role}"

# Approval Request Model
class ApprovalRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING')
    request_date = models.DateTimeField(auto_now_add=True)
    decision_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} requests {self.role.name} role at {self.farm.name}"

# Cow Model
class Cow(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    tag_number = models.CharField(max_length=50, unique=True)
    breed = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    weight = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    weight_timestamp = models.DateTimeField(auto_now=True)
    health_status = models.CharField(max_length=100)
    lactation_status = models.CharField(max_length=100)
    last_milking_date = models.DateField()

    def __str__(self):
        return self.name

# MilkingSession Model
class MilkingSession(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    milking_start_time = models.DateTimeField()
    milking_end_time = models.DateTimeField()
    milking_duration = models.DurationField()
    milk_yield = models.DecimalField(max_digits=6, decimal_places=2)
    milking_equipment_used = models.TextField()

# HealthRecord Model
class HealthRecord(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    health_issue = models.CharField(max_length=100)
    treatment = models.TextField()
    treatment_date = models.DateField()
    veterinarian = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'roles__name': 'Vet'})
    notes = models.TextField()

# BreedingRecord Model
class BreedingRecord(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    breeding_method = models.CharField(max_length=100, choices=[('AI', 'Artificial Insemination'), ('Natural', 'Natural Mating')])
    mating_bull = models.CharField(max_length=100)
    mating_date = models.DateField()
    expected_calving_date = models.DateField()
    pregnancy_status = models.CharField(max_length=100)

# CalvingRecord Model
class CalvingRecord(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    calving_date = models.DateField()
    calf_details = models.TextField()
    birthing_complications = models.TextField(blank=True, null=True)
