from database import create_patient_table, add_patient, get_all_patients, update_patient_contact, delete_patient

# Ensure the table is created
create_patient_table()

# Example interaction
if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1. Add a new patient")
        print("2. View all patients")
        print("3. Update patient contact")
        print("4. Delete a patient")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name: ")
            age = input("Enter age: ")
            while not age.isdigit():
                print("Invalid age. Please enter a valid number.")
                age = input("Enter age: ")
            age = int(age)

            gender = input("Enter gender (male/female/other): ")
            contact = input("Enter contact: ")
            email = input("Enter email: ")

            fever = input("Fever (yes/no): ").strip().lower()
            tiredness = input("Tiredness (yes/no): ").strip().lower()
            dry_cough = input("Dry cough (yes/no): ").strip().lower()
            difficulty_breathing = input("Difficulty breathing (yes/no): ").strip().lower()
            sore_throat = input("Sore throat (yes/no): ").strip().lower()
            no_other_symptoms = input("No other symptoms (yes/no): ").strip().lower()
            body_pain = input("Body pain (yes/no): ").strip().lower()
            nasal_congestion = input("Nasal congestion (yes/no): ").strip().lower()
            runny_nose = input("Runny nose (yes/no): ").strip().lower()
            diarrhea = input("Diarrhea (yes/no): ").strip().lower()

            # Validate severity input (should be 1, 2, or 3)
            severity = input("Severity of symptoms (1 = Mild, 2 = Moderate, 3 = Severe): ")
            while severity not in ["1", "2", "3"]:
                print("Invalid severity. Please enter 1, 2, or 3.")
                severity = input("Severity of symptoms (1 = Mild, 2 = Moderate, 3 = Severe): ")
            severity = int(severity)

            # Validate oxygen level input (should be a valid float)
            oxygen_level = input("Enter oxygen level (in percentage, e.g., 98.5): ")
            while not oxygen_level.replace('.', '', 1).isdigit():
                print("Invalid oxygen level. Please enter a valid float (e.g., 98.5).")
                oxygen_level = input("Enter oxygen level (in percentage, e.g., 98.5): ")
            oxygen_level = float(oxygen_level)

            add_patient((name, age, gender, contact, email, fever, tiredness, dry_cough, difficulty_breathing, 
                         sore_throat, no_other_symptoms, body_pain, nasal_congestion, 
                         runny_nose, diarrhea, severity, oxygen_level))
            print("Patient added successfully!")

        elif choice == "2":
            patients = get_all_patients()
            if not patients:
                print("No patients found.")
            for patient in patients:
                print(patient)

        elif choice == "3":
            email = input("Enter the patient's email to update: ")
            new_contact = input("Enter the new contact number: ")
            update_patient_contact(email, new_contact)
            print("Contact updated successfully!")

        elif choice == "4":
            email = input("Enter the patient's email to delete: ")
            delete_patient(email)
            print("Patient deleted successfully!")

        elif choice == "5":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Try again!")
