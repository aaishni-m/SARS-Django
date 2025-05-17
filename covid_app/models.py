from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    SEVERITY_CHOICES = [
        ('Mild', 'Mild'),
        ('Moderate', 'Moderate'),
        ('Severe', 'Severe'),
    ]
    BOOLEAN_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    fever = models.CharField(max_length=3, choices=BOOLEAN_CHOICES)
    tiredness = models.CharField(max_length=3, choices=BOOLEAN_CHOICES)
    dry_cough = models.CharField(max_length=3, choices=BOOLEAN_CHOICES)
    difficulty_breathing = models.CharField(max_length=3, choices=BOOLEAN_CHOICES)
    sore_throat = models.CharField(max_length=3, choices=BOOLEAN_CHOICES)
    no_other_symptoms = models.CharField(max_length=3, choices=BOOLEAN_CHOICES)
    body_pain = models.CharField(max_length=3, choices=BOOLEAN_CHOICES)
    nasal_congestion = models.CharField(max_length=3, choices=BOOLEAN_CHOICES)
    runny_nose = models.CharField(max_length=3, choices=BOOLEAN_CHOICES)
    diarrhea = models.CharField(max_length=3, choices=BOOLEAN_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    oxygen_level = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.email})"
