from flask import Flask, render_template, request, redirect
import os
from PIL import Image
import sqlite3
from model import compare_models  # Import the compare_models function
from datetime import datetime  # Add this import statement at the top


app = Flask(__name__)
UPLOAD_FOLDER = 'D:/SARS/static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
unique_filename = datetime.now().strftime("%Y%m%d%H%M%S") + '.png'
image_path = f'static/{unique_filename}'


# Database setup
def create_patient_table():
    conn = sqlite3.connect('patient.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            contact TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            fever TEXT NOT NULL,
            tiredness TEXT NOT NULL,
            dry_cough TEXT NOT NULL,
            difficulty_breathing TEXT NOT NULL,
            sore_throat TEXT NOT NULL,
            no_other_symptoms TEXT NOT NULL,
            body_pain TEXT NOT NULL,
            nasal_congestion TEXT NOT NULL,
            runny_nose TEXT NOT NULL,
            diarrhea TEXT NOT NULL,
            severity INTEGER NOT NULL,  
            oxygen_level REAL NOT NULL 
        )
    ''')
    conn.commit()
    conn.close()

# Ensure the database is ready
create_patient_table()

@app.route('/')
def home():
    return render_template('index.html', result='Upload an image for prediction')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from datetime import datetime

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Form submitted!")

    if 'file1' not in request.files:
        return 'There is no file1 in form!'

    file1 = request.files['file1']

    if file1.filename == '':
        return 'No selected file. Please upload a valid PNG, JPG, or JPEG image.'

    if not allowed_file(file1.filename):
        return 'File type not allowed. Please upload a valid PNG, JPG, or JPEG image.'

    # Collect patient data from the form
    patient_data = {
        'fever': int(request.form['fever']),
        'tiredness': int(request.form['Tiredness']),
        'dry cough': int(request.form['dry_cough']),
        'difficulty_breathing': int(request.form['difficulty_breathing']),
        'sore_throat': int(request.form['sore_throat']),
        'no_other_symptoms': int(request.form['no_other_symptoms']),
        'body_pain': int(request.form['body_pain']),
        'nasal_congestion': int(request.form['nasal_congestion']),
        'runny_nose': int(request.form['runny_nose']),
        'diarrhea': int(request.form['diarrhea']),
        'severity': request.form['severity'],  # Severity as a string
        'oxygen_level': float(request.form['oxygen_level']),
        'age': request.form['age'],
        'gender': request.form['gender']
    }

    # Generate a unique filename to prevent overwriting
    unique_filename = datetime.now().strftime("%Y%m%d%H%M%S") + '.png'
    path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

    try:
        # Save the file with the unique filename
        file1.save(path)

        # Verify if the image is valid
        with Image.open(path) as img:
            img.verify()  # Verifies the file is an actual image
        print(f"File saved at {path} and verified as a valid image.")

        # Get predictions from both models, passing both image path and patient data
        avg_percentage = compare_models(path, patient_data)  # Pass both path and patient_data

        # Use the logic to create the result
        if avg_percentage > 70:
            result = f"Likely to be diagnosed with COVID (Average: {avg_percentage:.2f}%)"
        else:
            result = f"Unlikely to be diagnosed with COVID (Average: {avg_percentage:.2f}%)"

    except Exception as e:
        print(f"Error processing file: {e}")
        return f"An error occurred: {e}"

    # Return result with the unique image path
    return render_template('index.html', result=result, image_path=f'static/{unique_filename}')




@app.route('/patient_form')
def patient_form():
    return render_template('index.html')

@app.route('/submit_patient', methods=['POST'])
def submit_patient():
    # Collect form data, ensuring numeric fields are converted properly
    patient_data = {
        'name': request.form.get('name', ''),
        'age': request.form.get('age', 0),
        'gender': request.form.get('gender', ''),
        'contact': request.form.get('contact', ''),
        'email': request.form.get('email', ''),
        'fever': request.form.get('fever', '0'),
        'tiredness': request.form.get('tiredness', '0'),
        'dry_cough': request.form.get('dry_cough', '0'),
        'difficulty_breathing': request.form.get('difficulty_breathing', '0'),
        'sore_throat': request.form.get('sore_throat', '0'),
        'no_other_symptoms': request.form.get('no_other_symptoms', '0'),
        'body_pain': request.form.get('body_pain', '0'),
        'nasal_congestion': request.form.get('nasal_congestion', '0'),
        'runny_nose': request.form.get('runny_nose', '0'),
        'diarrhea': request.form.get('diarrhea', '0'),
        'severity': request.form.get('severity', ''),
        'oxygen_level': request.form.get('oxygen_level', '0.0')
    }

    # Convert fields to their appropriate types (integers, floats)
    for key in ['fever', 'tiredness', 'dry_cough', 'difficulty_breathing', 'sore_throat',
                'no_other_symptoms', 'body_pain', 'nasal_congestion', 'runny_nose', 'diarrhea']:
        try:
            patient_data[key] = int(patient_data[key])  # Convert to integer
        except ValueError:
            patient_data[key] = 0  # Default to 0 if conversion fails

    # Convert 'oxygen_level' to float and 'age' to int
    try:
        patient_data['oxygen_level'] = float(patient_data['oxygen_level'])
    except ValueError:
        patient_data['oxygen_level'] = 0.0  # Default to 0.0 if conversion fails

    try:
        patient_data['age'] = int(patient_data['age'])
    except ValueError:
        patient_data['age'] = 0  # Default to 0 if conversion fails

    # Insert patient data into the database
    conn = sqlite3.connect('patient.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patients (name, age, gender, contact, email, fever, tiredness, dry_cough, difficulty_breathing, sore_throat,
        no_other_symptoms, body_pain, nasal_congestion, runny_nose, diarrhea, severity, oxygen_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(patient_data.values()))
    conn.commit()
    conn.close()

    # Prepare data for model prediction (excluding name, contact, email)
    prediction_data = {
        'fever': patient_data['fever'],
        'tiredness': patient_data['tiredness'],
        'dry_cough': patient_data['dry_cough'],
        'difficulty_breathing': patient_data['difficulty_breathing'],
        'sore_throat': patient_data['sore_throat'],
        'no_other_symptoms': patient_data['no_other_symptoms'],
        'body_pain': patient_data['body_pain'],
        'nasal_congestion': patient_data['nasal_congestion'],
        'runny_nose': patient_data['runny_nose'],
        'diarrhea': patient_data['diarrhea'],
        'severity': patient_data['severity'],
        'oxygen_level': patient_data['oxygen_level'],
        'age': patient_data['age'],
        'gender': patient_data['gender']
    }

    # Get model prediction
    avg_percentage = compare_models(prediction_data)

    # Determine the result based on the average prediction
    if avg_percentage > 70:
        result = f"Likely to be diagnosed with COVID (Average: {avg_percentage:.2f}%)"
    else:
        result = f"Unlikely to be diagnosed with COVID (Average: {avg_percentage:.2f}%)"

    return render_template('index.html', result=result)

