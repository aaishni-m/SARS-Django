from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from PIL import Image
from .utils import compare_models
from .models import Patient

# Home view
def home(request):
    return render(request, 'home.html')

# Predict view
def predict(request):
    result = None
    if request.method == 'POST':
        # Handle file upload
        uploaded_file = request.FILES.get('file1')
        if uploaded_file:
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)

            try:
                with Image.open(file_path) as img:
                    img.verify()
                print(f"File verified as a valid image: {filename}")

                # Collect patient symptom data from form
                prediction_data = {
                    'fever': int(request.POST.get('fever', 0)),
                    'tiredness': int(request.POST.get('tiredness', 0)),
                    'dry_cough': int(request.POST.get('dry_cough', 0)),
                    'difficulty_breathing': int(request.POST.get('difficulty_breathing', 0)),
                    'sore_throat': int(request.POST.get('sore_throat', 0)),
                    'no_other_symptoms': int(request.POST.get('no_other_symptoms', 0)),
                    'body_pain': int(request.POST.get('body_pain', 0)),
                    'nasal_congestion': int(request.POST.get('nasal_congestion', 0)),
                    'runny_nose': int(request.POST.get('runny_nose', 0)),
                    'diarrhea': int(request.POST.get('diarrhea', 0)),
                    'severity': int(request.POST.get('severity', 0)),
                    'oxygen_level': int(request.POST.get('oxygen_level', 0)),
                }

                # Get predictions
                avg_percentage = compare_models(file_path, prediction_data)

                if avg_percentage > 70:
                    result = f"Likely to be diagnosed with COVID (Average: {avg_percentage:.2f}%)"
                else:
                    result = f"Unlikely to be diagnosed with COVID (Average: {avg_percentage:.2f}%)"

            except Exception as e:
                print(f"Error processing file: {e}")
                result = "An error occurred while processing the file."

    return render(request, 'index.html', {'result': result})

# Patient management views
def add_patient(request):
    if request.method == 'POST':
        data = request.POST
        patient = Patient(
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            contact=data['contact'],
            email=data['email'],
            fever=data['fever'],
            tiredness=data['tiredness'],
            dry_cough=data['dry_cough'],
            difficulty_breathing=data['difficulty_breathing'],
            sore_throat=data['sore_throat'],
            no_other_symptoms=data['no_other_symptoms'],
            body_pain=data['body_pain'],
            nasal_congestion=data['nasal_congestion'],
            runny_nose=data['runny_nose'],
            diarrhea=data['diarrhea'],
            severity=data['severity'],
            oxygen_level=data['oxygen_level']
        )
        patient.save()
        return redirect('patient_list')
    return render(request, 'add_patient.html')

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

def update_contact(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        patient.contact = request.POST['contact']
        patient.save()
        return redirect('patient_list')
    return render(request, 'update_contact.html', {'patient': patient})

def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    return redirect('patient_list')
