from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from PIL import Image
from .utils import compare_models
from .models import Patient
from django.contrib.auth import login, authenticate
from django.contrib import messages  

# Home view — simple landing page
def home(request):
    return render(request, 'home.html')

# Predict view — handles image upload & symptom data, runs predictions
def predict(request):
    result = None

    if request.method == 'POST':
        uploaded_file = request.FILES.get('file1')

        severity = int(request.POST.get('severity', 1))  # Default to 1 (Mild)
        oxygen_level = float(request.POST.get('oxygen_level', 0.0))

        # Get list of checked symptoms from form
        checked_symptoms = request.POST.getlist('symptoms')

        # Map symptoms to True/False based on checked list
        all_symptoms = [
            'fever', 'tiredness', 'dry_cough', 'difficulty_breathing',
            'sore_throat', 'body_pain', 'nasal_congestion', 'runny_nose', 'diarrhea'
        ]
        symptoms_data = {symptom: (symptom in checked_symptoms) for symptom in all_symptoms}

        # Rest of your existing code ...
        patient, created = Patient.objects.get_or_create(email=request.POST.get('email', ''))
        patient.name = request.POST.get('name', 'Anonymous')
        patient.age = int(request.POST.get('age', 0))
        patient.gender = request.POST.get('gender', '')
        patient.contact = request.POST.get('contact', '')
        patient.severity = severity
        patient.oxygen_level = oxygen_level

        for symptom, value in symptoms_data.items():
            setattr(patient, symptom, value)
        patient.save()


        if uploaded_file:
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)

            try:
                with Image.open(file_path) as img:
                    img.verify()
                print(f"[INFO] File verified as a valid image: {filename}")

                prediction_data = {
                    **symptoms_data,
                    'severity': severity,
                    'oxygen_level': oxygen_level,
                }

                avg_percentage = compare_models(file_path, prediction_data)

                if avg_percentage > 70:
                    result = f"Likely to be diagnosed with COVID (Average confidence: {avg_percentage:.2f}%)"
                else:
                    result = f"Unlikely to be diagnosed with COVID (Average confidence: {avg_percentage:.2f}%)"

            except Exception as e:
                print(f"[ERROR] Error processing file: {e}")
                result = "An error occurred while processing the image. Please try again with a valid image."

        else:
            result = "No file uploaded. Please upload an image file."

    return render(request, 'index.html', {'result': result})



# Patient management views

# def add_patient(request):
#     if request.method == 'POST':
#         data = request.POST

#         # Optional: Validate data here or use Django forms for better validation & security
#         try:
#             patient = Patient(
#                 name=data.get('name', '').strip(),
#                 age=int(data.get('age', 0)),
#                 gender=data.get('gender', '').strip(),
#                 contact=data.get('contact', '').strip(),
#                 email=data.get('email', '').strip(),
#                 fever=int(data.get('fever', 0)),
#                 tiredness=int(data.get('tiredness', 0)),
#                 dry_cough=int(data.get('dry_cough', 0)),
#                 difficulty_breathing=int(data.get('difficulty_breathing', 0)),
#                 sore_throat=int(data.get('sore_throat', 0)),
#                 # no_other_symptoms=int(data.get('no_other_symptoms', 0)),
#                 body_pain=int(data.get('body_pain', 0)),
#                 nasal_congestion=int(data.get('nasal_congestion', 0)),
#                 runny_nose=int(data.get('runny_nose', 0)),
#                 diarrhea=int(data.get('diarrhea', 0)),
#                 severity=int(data.get('severity', 0)),
#                 oxygen_level=int(data.get('oxygen_level', 0)),
#             )
#             patient.save()
#             return redirect('patient_list')

#         except Exception as e:
#             print(f"[ERROR] Failed to add patient: {e}")
#             # You might want to pass an error message to template here
#             return render(request, 'add_patient.html', {'error': 'Invalid data provided. Please check and try again.'})

#     return render(request, 'add_patient.html')



def update_contact(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        new_contact = request.POST.get('contact', '').strip()
        if new_contact:
            patient.contact = new_contact
            patient.save()
            return redirect('patient_list')
        else:
            # Optional: Pass error message if contact field empty
            return render(request, 'update_contact.html', {'patient': patient, 'error': 'Contact cannot be empty.'})

    return render(request, 'update_contact.html', {'patient': patient})


def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    return redirect('patient_list')


from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})

    return render(request, 'registration/login.html')

from django.shortcuts import render, redirect
from .models import Patient

# covid_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Patient

# ——— Step 1: Signup & create minimal Patient ———
def signup_view(request):
    if request.method == 'POST':
        username    = request.POST['username']
        email       = request.POST['email']
        password    = request.POST['password']
        name_field  = request.POST.get('name', username)
        age         = int(request.POST.get('age', 0))
        gender      = request.POST.get('gender', '')
        phone       = request.POST.get('phone_number', '')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('signup')
        
        if Patient.objects.filter(email=email).exists():
            messages.error(request, 'A patient with this email already exists!')
            return redirect('signup')

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        patient = Patient.objects.create(
            user=user,
            name=name_field,
            age=age,
            gender=gender,
            contact=phone,
            email=email
        )

        login(request, user)
        # send to step-2, passing patient id
        return redirect('add_patient', patient_id=patient.id)

    return render(request, 'registration/signup.html')


# ——— Step 2: fill in remaining patient data ———
def add_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)

    if request.method == 'POST':
        # symptoms
        for field in [
            'fever','tiredness','dry_cough','difficulty_breathing',
            'sore_throat','body_pain','nasal_congestion',
            'runny_nose','diarrhea'
        ]:
            setattr(patient, field, request.POST.get(field) == 'on')

        # severity & oxygen
        severity     = request.POST.get('severity')
        oxygen_level = request.POST.get('oxygen_level')
        if severity:
            patient.severity = int(severity)
        if oxygen_level:
            patient.oxygen_level = float(oxygen_level)

        patient.save()
        return redirect('dashboard')

    return render(request, 'index.html', {'patient': patient})


# ——— Dashboard: show only logged-in user’s patient record ———
def dashboard_view(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "Complete your profile first.")
        # redirect to step-2 using the patient you just created
        # (you might store it in session if needed)
        return redirect('signup')
    return render(request, 'dashboard.html', {'patient': patient})
