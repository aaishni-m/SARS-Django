import sqlite3

# Establish connection and create the table
def create_patient_table():
    conn = sqlite3.connect('patient.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER CHECK(age > 0) NOT NULL,
            gender TEXT CHECK(gender IN ('male', 'female', 'other')) NOT NULL,
            contact TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            fever TEXT CHECK(fever IN ('yes', 'no')) NOT NULL,
            tiredness TEXT CHECK(tiredness IN ('yes', 'no')) NOT NULL,
            dry_cough TEXT CHECK(dry_cough IN ('yes', 'no')) NOT NULL,
            difficulty_breathing TEXT CHECK(difficulty_breathing IN ('yes', 'no')) NOT NULL,
            sore_throat TEXT CHECK(sore_throat IN ('yes', 'no')) NOT NULL,
            no_other_symptoms TEXT CHECK(no_other_symptoms IN ('yes', 'no')) NOT NULL,
            body_pain TEXT CHECK(body_pain IN ('yes', 'no')) NOT NULL,
            nasal_congestion TEXT CHECK(nasal_congestion IN ('yes', 'no')) NOT NULL,
            runny_nose TEXT CHECK(runny_nose IN ('yes', 'no')) NOT NULL,
            diarrhea TEXT CHECK(diarrhea IN ('yes', 'no')) NOT NULL,
            severity TEXT CHECK(diarrhea IN ('Mild', 'Moderate', 'Severe')) NOT NULL, 
            oxygen_level FLOAT NOT NULL
         )
    ''')
    conn.commit()
    conn.close()

# Insert patient data
def add_patient(data):
    conn = sqlite3.connect('patient.db')
    cursor = conn.cursor()
    
    # Check if the email already exists
    cursor.execute('SELECT COUNT(*) FROM patients WHERE email = ?', (data[4],))
    if cursor.fetchone()[0] > 0:
        print(f"Error: A patient with email {data[4]} already exists.")
        conn.close()
        return
    
    # Insert the new patient data
    else:
        cursor.execute(''' 
            INSERT INTO patients (
                name, age, gender, contact, email, fever, tiredness, dry_cough, difficulty_breathing, 
                sore_throat, no_other_symptoms, body_pain, nasal_congestion, 
                runny_nose, diarrhea, severity, oxygen_level
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
        conn.close()
        print("Patient added successfully!")

# Fetch all patients
def get_all_patients():
    conn = sqlite3.connect('patient.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients')
    results = cursor.fetchall()
    conn.close()
    return results

# Update contact
def update_patient_contact(email, new_contact):
    conn = sqlite3.connect('patient.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE patients 
        SET contact = ? 
        WHERE email = ?
    ''', (new_contact, email))
    conn.commit()
    conn.close()

# Delete patient
def delete_patient(email):
    conn = sqlite3.connect('patient.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM patients WHERE email = ?', (email,))
    conn.commit()
    conn.close()
