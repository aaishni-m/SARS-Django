from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    
    fever = models.BooleanField()
    tiredness = models.BooleanField()
    dry_cough = models.BooleanField()
    difficulty_breathing = models.BooleanField()
    sore_throat = models.BooleanField()
    # no_other_symptoms = models.BooleanField()
    body_pain = models.BooleanField()
    nasal_congestion = models.BooleanField()
    runny_nose = models.BooleanField()
    diarrhea = models.BooleanField()
    
    severity = models.PositiveSmallIntegerField(choices=[(1, 'Mild'), (2, 'Moderate'), (3, 'Severe')])
    oxygen_level = models.FloatField()

    def __str__(self):
        return self.name
