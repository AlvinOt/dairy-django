from django.db import models


class Farm(models.Model):
    name = models.CharField(max_length=100, unique=True)
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
    location = models.CharField(max_length=255)
    description = models.TextField()
    slogan = models.CharField(max_length=255, blank=True, null=True, help_text='Farm motto')


    def __str__(self):
        return self.name
