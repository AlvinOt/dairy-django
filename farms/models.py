from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class Farm(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    farm_email = models.EmailField(
            max_length=255, blank= True,
            validators=[EmailValidator(message="Enter a valid email address.")]
            )
    farm_phone = models.CharField(
            max_length=20,
            blank=True,
            validators=[RegexValidator(
                regex=r'^(\+\d{10,12})|\d{10,12}$',
                message="Enter a valid Phone number"
                )]
            )
    location = models.CharField(max_length=255)
    description = models.TextField()
    slogan = models.CharField(max_length=255, blank=True, help_text='Motto')
    created = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)


    class Status(models.TextChoices):
        INACTIVE = 'inactive', 'Inactive'
        ACTIVE = 'active', 'Active'

    class Meta:
        ordering = ['-created']
        indexes = [
                models.Index(fields=['created']),
                models.Index(fields=['verified']),
                ]


    def __str__(self):
        return self.name
