# Medical Record Database Module
import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_FILE = 'data/medical_records.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Create Patients Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            patient_name TEXT,
            patient_id TEXT,
            gender TEXT,
            age INTEGER,
            smoking TEXT,
            yellow_fingers TEXT,
            anxiety TEXT,
            peer_pressure TEXT,
            chronic_disease TEXT,
            fatigue TEXT,
            allergy TEXT,
            wheezing TEXT,
            alcohol TEXT,
            coughing TEXT,
            shortness_of_breath TEXT,
            swallowing_difficulty TEXT,
            chest_pain TEXT,
            phone TEXT,
            location TEXT,
            risk_level TEXT,
            malignancy_probability REAL
        )
    ''')
    
    # Migration: Check if columns exist, if not add them
    try:
        c.execute("ALTER TABLE patients ADD COLUMN phone TEXT")
    except sqlite3.OperationalError:
        pass # Column already exists
    
    try:
        c.execute("ALTER TABLE patients ADD COLUMN location TEXT")
    except sqlite3.OperationalError:
        pass # Column already exists
    
    # Create Users Table (for future auth)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT DEFAULT 'staff'
        )
    ''')
    
    # Create Appointments Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            patient_id TEXT,
            date TEXT,
            time TEXT,
            type TEXT,
            status TEXT DEFAULT 'Scheduled'
        )
    ''')
    
    conn.commit()
    conn.close()

def save_patient_record(data_dict):
    """
    Saves a single patient record (dictionary) to the database.
    Argument 'data_dict' should match the table schema columns.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Extract values in correct order
    params = (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data_dict.get('Patient Name'),
        data_dict.get('Patient ID'),
        # Map input features (Assuming input keys match DB columns roughly or we map them)
        # We need to be careful with key matching. In app.py we have keys like 'GENDER', 'AGE'.
        # Let's standardize on standard keys or map them here.
        # Actually, let's just dump the raw mapped values from app.py
        str(data_dict.get('GENDER', '')),
        int(data_dict.get('AGE', 0)),
        str(data_dict.get('SMOKING', '')),
        str(data_dict.get('YELLOW_FINGERS', '')),
        str(data_dict.get('ANXIETY', '')),
        str(data_dict.get('PEER_PRESSURE', '')),
        str(data_dict.get('CHRONIC DISEASE', '')),
        str(data_dict.get('FATIGUE ', '')), # Note space in key from app.py
        str(data_dict.get('ALLERGY ', '')), # Note space
        str(data_dict.get('WHEEZING', '')),
        str(data_dict.get('ALCOHOL CONSUMING', '')),
        str(data_dict.get('COUGHING', '')),
        str(data_dict.get('SHORTNESS OF BREATH', '')),
        str(data_dict.get('SWALLOWING DIFFICULTY', '')),
        str(data_dict.get('CHEST PAIN', '')),
        str(data_dict.get('Phone', '')),
        str(data_dict.get('Location', '')),
        data_dict.get('Risk'),
        float(data_dict.get('Probability', 0.0))
    )
    
    try:
        c.execute('''
            INSERT INTO patients (
                date, patient_name, patient_id, gender, age, smoking, 
                yellow_fingers, anxiety, peer_pressure, chronic_disease, 
                fatigue, allergy, wheezing, alcohol, coughing, 
                shortness_of_breath, swallowing_difficulty, chest_pain, 
                phone, location, risk_level, malignancy_probability
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', params)
        conn.commit()
        return True
    except Exception as e:
        print(f"DB Error: {e}")
        return False
    finally:
        conn.close()

def load_all_records():
    conn = sqlite3.connect(DB_FILE)
    try:
        # Load into DataFrame for compatibility with existing app logic
        df = pd.read_sql_query("SELECT * FROM patients ORDER BY id DESC", conn)
        
        if not df.empty:
            # Map DB columns back to UI/Analytics expected columns
            column_map = {
                'date': 'Date',
                'patient_name': 'Patient Name',
                'patient_id': 'Patient ID',
                'gender': 'GENDER',
                'age': 'AGE',
                'smoking': 'SMOKING',
                'yellow_fingers': 'YELLOW_FINGERS',
                'anxiety': 'ANXIETY',
                'peer_pressure': 'PEER_PRESSURE',
                'chronic_disease': 'CHRONIC DISEASE',
                'fatigue': 'FATIGUE ', # Note space
                'allergy': 'ALLERGY ', # Note space
                'wheezing': 'WHEEZING',
                'alcohol': 'ALCOHOL CONSUMING',
                'coughing': 'COUGHING',
                'shortness_of_breath': 'SHORTNESS OF BREATH',
                'swallowing_difficulty': 'SWALLOWING DIFFICULTY',
                'chest_pain': 'CHEST PAIN',
                'phone': 'Phone',
                'location': 'Location',
                'risk_level': 'Risk',
                'malignancy_probability': 'Probability'
            }
            df = df.rename(columns=column_map)
            
        return df
    except Exception as e:
        print(f"DB Load Error: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def save_appointment(appt_dict):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    params = (
        appt_dict.get('Patient Name'),
        appt_dict.get('Patient ID'),
        appt_dict.get('Date'),
        appt_dict.get('Time'),
        appt_dict.get('Type'),
        appt_dict.get('Status', 'Scheduled')
    )
    try:
        c.execute('''
            INSERT INTO appointments (patient_name, patient_id, date, time, type, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', params)
        conn.commit()
        return True
    except Exception as e:
        print(f"Appt DB Error: {e}")
        return False
    finally:
        conn.close()

def load_all_appointments():
    conn = sqlite3.connect(DB_FILE)
    try:
        df = pd.read_sql_query("SELECT * FROM appointments ORDER BY date ASC, time ASC", conn)
        return df
    except Exception as e:
        print(f"Appt Load Error: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# Initialize on module load
if not os.path.exists(os.path.dirname(DB_FILE)):
    os.makedirs(os.path.dirname(DB_FILE))

init_db()

