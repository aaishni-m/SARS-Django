from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'name', 'age', 'gender', 'contact', 'email',
            'fever', 'tiredness', 'dry_cough', 'difficulty_breathing',
            'sore_throat', 'body_pain', 'nasal_congestion', 'runny_nose', 'diarrhea',
            'severity', 'oxygen_level'
        ]
