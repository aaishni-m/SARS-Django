# covid_app/models.py
from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient',
        null=True,
        blank=True,
    )

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    # Basic info
    name          = models.CharField(max_length=255)
    age           = models.PositiveIntegerField(default=0)
    gender        = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    contact       = models.CharField(max_length=15, blank=True)
    email         = models.EmailField(unique=True)

    # Step-2 symptoms (all default=False so form may omit them initially)
    fever               = models.BooleanField(default=False)
    tiredness           = models.BooleanField(default=False)
    dry_cough           = models.BooleanField(default=False)
    difficulty_breathing= models.BooleanField(default=False)
    sore_throat         = models.BooleanField(default=False)
    body_pain           = models.BooleanField(default=False)
    nasal_congestion    = models.BooleanField(default=False)
    runny_nose          = models.BooleanField(default=False)
    diarrhea            = models.BooleanField(default=False)

    # Severity & vitals
    severity     = models.PositiveSmallIntegerField(
                      choices=[(1, 'Mild'), (2, 'Moderate'), (3, 'Severe')],
                      default=1
                   )
    oxygen_level = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} ({self.user.username if self.user else 'no user'})"
