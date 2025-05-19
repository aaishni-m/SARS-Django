# COVID-19 Symptom Prediction App

## Overview

This application is designed to predict COVID-19 severity levels based on user input, including personal details, symptoms, and uploaded test reports. Users can select symptoms through checkboxes, and the backend processes this data to create or update a patient record and provide predictions.

---

## Features

1. **User Input**:

   * Personal details: Name, Age, Gender, Email, Contact.
   * Symptoms: A set of predefined symptoms to choose from.
   * Severity level and oxygen level.
   * Option to upload a medical test report.

2. **Symptom Parsing**:

   * Frontend provides checkboxes for symptoms with `name="symptoms"`.
   * Backend processes selected symptoms and maps them to boolean fields for prediction.

3. **Database Integration**:

   * Saves user data and symptoms in a `Patient` model.

4. **Prediction Logic**:

   * Uses the uploaded test report and input data to predict COVID-19 severity.

---

## File Descriptions

### Backend (`views.py`)

* **Symptom Parsing**:

  * `request.POST.getlist('symptoms')` is used to collect the selected symptoms as a list.
  * Maps the list of selected symptoms to predefined boolean fields (`fever`, `dry_cough`, etc.).

* **Patient Model Updates**:
  The boolean values are assigned to the `Patient` model's fields and saved to the database.

* **Prediction Logic**:
  The processed data is used for severity prediction (logic not detailed here).

## Installation and Setup

### Prerequisites

1. Python 3.8+
2. Django Framework
3. Any database supported by Django (e.g., SQLite, PostgreSQL)

## How It Works

1. User fills in the form, selecting symptoms, severity, and oxygen level.
2. Upon form submission:

   * Symptoms are parsed as a list of checked values.
   * These values are mapped to corresponding boolean fields.
   * Patient information is saved to the database.
3. Backend processes the input for predictions and returns the results.

---

## Future Enhancements

1. Incorporate advanced prediction models.
2. Provide a downloadable report of predictions.
3. Enhance the UI with real-time form validation.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
