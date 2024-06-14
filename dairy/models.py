from django.db import models
from django.utils.text import slugify
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User

class Status(models.TextChoices):
    INACTIVE = 'INA', 'Inactive'
    ACTIVE = 'ACT', 'Active'

class Farm(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    managers = models.ManyToManyField(User, related_name='managed_farms')
    email = models.EmailField(
            max_length=255, blank=True,
            validators=[EmailValidator(message="Enter a valid email address.")]
            )
    phone = models.CharField(
        max_length=20, blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Enter a valid phone number."
        )]
    )
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True)
    slogan = models.CharField(max_length=255, blank=True, null=True, help_text='Farm motto')
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
            max_length=3,
            choices=Status.choices,
            default=Status.INACTIVE
            )
    verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
            models.Index(fields=['verified']),
            models.Index(fields=['name']),
        ]
        verbose_name = 'Farm'
        verbose_name_plural = 'Farms'

    def __str__(self):
        return self.name
