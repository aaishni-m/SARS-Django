from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from PIL import Image
from .utils import compare_models
from .models import Patient

# Home view — simple landing page
def home(request):
    return render(request, 'home.html')

# Predict view — handles image upload & symptom data, runs predictions
def predict(request):
    result = None
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file1')
        if uploaded_file:
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)

            try:
                # Verify image file integrity before proceeding
                with Image.open(file_path) as img:
                    img.verify()
                print(f"[INFO] File verified as a valid image: {filename}")

                # Collect symptom data from the POST request, with safe int casting and defaults
                prediction_data = {
                    'fever': int(request.POST.get('fever', 0)),
                    'tiredness': int(request.POST.get('tiredness', 0)),
                    'dry_cough': int(request.POST.get('dry_cough', 0)),
                    'difficulty_breathing': int(request.POST.get('difficulty_breathing', 0)),
                    'sore_throat': int(request.POST.get('sore_throat', 0)),
                    # 'no_other_symptoms': int(request.POST.get('no_other_symptoms', 0)),  # If you want to add later
                    'body_pain': int(request.POST.get('body_pain', 0)),
                    'nasal_congestion': int(request.POST.get('nasal_congestion', 0)),
                    'runny_nose': int(request.POST.get('runny_nose', 0)),
                    'diarrhea': int(request.POST.get('diarrhea', 0)),
                    'severity': int(request.POST.get('severity', 0)),
                    'oxygen_level': int(request.POST.get('oxygen_level', 0)),
                }

                # Run your combined model predictions (Joblib + PyTorch)
                avg_percentage = compare_models(file_path, prediction_data)

                # Set the result string based on threshold
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

def add_patient(request):
    if request.method == 'POST':
        data = request.POST

        # Optional: Validate data here or use Django forms for better validation & security
        try:
            patient = Patient(
                name=data.get('name', '').strip(),
                age=int(data.get('age', 0)),
                gender=data.get('gender', '').strip(),
                contact=data.get('contact', '').strip(),
                email=data.get('email', '').strip(),
                fever=int(data.get('fever', 0)),
                tiredness=int(data.get('tiredness', 0)),
                dry_cough=int(data.get('dry_cough', 0)),
                difficulty_breathing=int(data.get('difficulty_breathing', 0)),
                sore_throat=int(data.get('sore_throat', 0)),
                # no_other_symptoms=int(data.get('no_other_symptoms', 0)),
                body_pain=int(data.get('body_pain', 0)),
                nasal_congestion=int(data.get('nasal_congestion', 0)),
                runny_nose=int(data.get('runny_nose', 0)),
                diarrhea=int(data.get('diarrhea', 0)),
                severity=int(data.get('severity', 0)),
                oxygen_level=int(data.get('oxygen_level', 0)),
            )
            patient.save()
            return redirect('patient_list')

        except Exception as e:
            print(f"[ERROR] Failed to add patient: {e}")
            # You might want to pass an error message to template here
            return render(request, 'add_patient.html', {'error': 'Invalid data provided. Please check and try again.'})

    return render(request, 'add_patient.html')


def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})


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
