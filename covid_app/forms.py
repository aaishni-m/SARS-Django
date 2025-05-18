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

# myapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password1', 'password2']

