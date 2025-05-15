import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_file
from io import BytesIO
from reportlab.pdfgen import canvas
from flask import send_file
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'patients.db')
# report download
@app.route('/download_report/<int:patient_id>')
def download_report(patient_id):
    # Connect to DB and fetch patient details and related records
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
    patient = cursor.fetchone()

    if not patient:
        return "Patient not found", 404

    # Fetch other records like medicines, tests, doctor notes for this patient
    # Example: cursor.execute("SELECT * FROM records WHERE patient_id=?", (patient_id,))
    # records = cursor.fetchall()

    # Create PDF in memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # Write patient info
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, f"Patient Report for {patient[1]} (ID: {patient[0]})")

    p.setFont("Helvetica", 12)
    p.drawString(100, 780, f"Age: {patient[2]}")
    p.drawString(100, 760, f"Contact: {patient[3]}")
    p.drawString(100, 740, f"Department: {patient[4]}")

    # TODO: Add medicines, tests, doctor recommendations here in PDF format

    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"Patient_{patient_id}_Report.pdf", mimetype='application/pdf')

#about
@app.route('/about')
def about():
    return render_template('about.html')

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Add patient route
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        contact = request.form.get('contact')
        department = request.form.get('department')

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO patients (name, age, contact, department) VALUES (?, ?, ?, ?)", (name, age, contact, department))
            conn.commit()
            conn.close()
            print("Patient added successfully!")
        except Exception as e:
            print(f"Error adding patient: {e}")
        return redirect(url_for('view_patients'))
    return render_template('add_patient.html')

# View patients route
@app.route('/view_patients')
def view_patients():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return render_template('view_patients.html', patients=patients)

# Download records route
@app.route('/download_records/<int:patient_id>')
def download_records(patient_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()
    conn.close()

    if patient:
        pdf_buffer = BytesIO()
        pdf = canvas.Canvas(pdf_buffer)
        pdf.drawString(100, 750, f"Patient ID: {patient[0]}")
        pdf.drawString(100, 730, f"Name: {patient[1]}")
        pdf.drawString(100, 710, f"Age: {patient[2]}")
        pdf.drawString(100, 690, f"Contact: {patient[3]}")
        pdf.drawString(100, 670, f"Department: {patient[4]}")
        pdf.showPage()
        pdf.save()
        pdf_buffer.seek(0)
        return send_file(pdf_buffer, as_attachment=True, download_name=f"patient_{patient_id}_record.pdf", mimetype='application/pdf')
    return "Patient record not found."

if __name__ == '__main__':
    app.run(debug=True)
