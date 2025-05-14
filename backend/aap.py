import os
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'patients.db')  # Database file location

# Function to create the patients table
def create_table():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            contact TEXT,
            department TEXT
        );
        """)
        conn.commit()
        conn.close()
        print("Patients table created successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")
# About route
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
        department = request.form.get('department')  # Get department value


        # Server-side validation: Ensure contact is a 10-digit number
        if len(contact) != 10 or not contact.isdigit():
            error_message = "Contact number must be exactly 10 digits."
            return render_template('add_patient.html', error_message=error_message)

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            print(f"Adding patient: Name={name}, Age={age}, Contact={contact}, Department={department}")
            cursor.execute("INSERT INTO patients (name, age, contact, department) VALUES (?, ?, ?, ?)", 
                           (name, age, contact, department))
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
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"Error retrieving patients: {e}")
        patients = []

    return render_template('view_patients.html', patients=patients)


# Delete patient route
@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE id=?", (id,))
        conn.commit()
        conn.close()
        print(f"Patient with ID {id} deleted successfully!")
    except Exception as e:
        print(f"Error deleting patient: {e}")

    return redirect(url_for('view_patients'))

# Call the create_table function to ensure the table is created when the app starts
if __name__ == '__main__':
    create_table()
    app.run(debug=True)
