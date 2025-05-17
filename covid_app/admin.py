from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'gender', 'severity', 'oxygen_level')
    list_filter = ('gender', 'severity', 'fever')
    search_fields = ('name', 'email')
