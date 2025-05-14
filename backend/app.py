import os
import sqlite3

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
            department TEXT  -- added department column
        );
        """)
        conn.commit()
        conn.close()
        print("Patients table created successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")

# Call the create_table function to ensure the table is created when the app starts
if __name__ == "__main__":
    create_table()
