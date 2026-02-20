
import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os
import sys
import hashlib
from datetime import datetime

# Fix imports
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Set page config
st.set_page_config(
    page_title="Medical Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
RECORDS_FILE = 'data/patient_records.csv'

# Custom CSS for Hospital Theme
def apply_custom_style():
    st.markdown("""
        <style>
        /* Force Background Color - Soft Teal Medical Background */
        [data-testid="stAppViewContainer"] {
            background-color: #F5F7FA !important;
            font-family: 'Inter', 'Roboto', 'Segoe UI', sans-serif;
            color: #212529;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #2A9D8F !important;
            border-right: 1px solid #2A9D8F;
        }
        [data-testid="stSidebarNav"] {
            background-color: transparent !important;
        }
        [data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }
        [data-testid="stSidebar"] a:hover {
            opacity: 0.85;
        }
        
        /* Streamlit Widgets in Sidebar */
        [data-testid="stSidebar"] .stSelectbox, [data-testid="stSidebar"] .stRadio {
            background-color: rgba(255,255,255,0.1) !important;
            border-radius: 8px;
            padding: 5px;
            border: 1px solid rgba(255,255,255,0.2);
        }

        /* Header Background (Top Bar) */
        [data-testid="stHeader"] {
            background-color: #2A9D8F !important;
            color: #FFFFFF !important;
        }

        /* Main Content Container */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #212529 !important;
            font-weight: 700;
        }
        
        /* Text */
        p, label, .stMarkdown {
            color: #212529 !important;
        }

        /* Buttons - Soft Teal (#2A9D8F) */
        div.stButton > button {
            background-color: #2A9D8F !important;
            color: #ffffff !important;
            border-radius: 6px;
            border: none;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            display: inline-flex !important;
        }
        div.stButton > button:hover {
            opacity: 0.9;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(42, 157, 143, 0.2);
        }
        
        /* Input Fields - White Modals/Forms */
        .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
            border-radius: 6px;
            border: 1px solid #ADB5BD;
            background-color: #FFFFFF !important;
            color: #212529 !important;
            font-weight: 500;
        }
        
        /* Cards/Containers - Pure White on Light Gray */
        .patient-card, .css-1r6slb0, [data-testid="stVerticalBlock"] > div > div > .stVerticalBlock, [data-testid="stForm"] {
            background-color: #FFFFFF !important;
            padding: 30px !important;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03) !important;
            border: 1px solid #E5EAF0 !important;
            margin-bottom: 24px;
        }
        
        /* Custom Classes */
        .hospital-header {
            background: #2A9D8F;
            padding: 35px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 8px 20px rgba(42, 157, 143, 0.15);
            text-align: center;
            color: #FFFFFF;
        }
        .hospital-header h1 {
            color: #FFFFFF !important;
            margin: 0;
            font-size: 2.5em;
        }
        .hospital-header p {
            color: rgba(255,255,255,0.9) !important;
            margin: 5px 0 0 0;
            font-weight: 500;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}

        /* Digital ID Card Styling */
        .id-card {
            background: linear-gradient(135deg, #2A9D8F 0%, #264653 100%);
            border: 2px solid white;
            border-radius: 12px;
            padding: 25px;
            width: 380px;
            margin: 20px auto;
            position: relative;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(42, 157, 143, 0.25);
            color: white;
            font-family: 'Inter', sans-serif;
        }
        .id-card::before {
            content: "OFFICIAL MEDICAL ID";
            position: absolute;
            top: 15px;
            right: -35px;
            background: white;
            color: #2A9D8F;
            padding: 5px 45px;
            transform: rotate(45deg);
            font-size: 0.7em;
            font-weight: bold;
        }

        /* Metric Styling */
        [data-testid="stMetric"] {
            background: #FFFFFF !important;
            padding: 15px !important;
            border-radius: 8px !important;
            border-left: 5px solid #2A9D8F !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Helper Functions
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

# Database Integration
from src.database import save_patient_record, load_all_records, save_appointment, load_all_appointments

# Initialize session state for login and flow
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'reg_complete' not in st.session_state:
    st.session_state['reg_complete'] = False
if 'patient_reg_info' not in st.session_state:
    st.session_state['patient_reg_info'] = {}
if 'ct_result' not in st.session_state:
    st.session_state['ct_result'] = None
if 'ct_scanning' not in st.session_state:
    st.session_state['ct_scanning'] = False

# --- Pages ---

def login_page():
    apply_custom_style()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class='hospital-header'>
                <h1>🏥 Dashboard</h1>
                <p>Advanced Medical Diagnostics Portal</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("### 🔐 Secure Access")
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
            
            submitted = st.form_submit_button("🚀 Authenticate & Login", use_container_width=True)
            
            if submitted:
                if username == "admin" and password == "admin": 
                    st.session_state['logged_in'] = True
                    st.toast("👋 Welcome back, Dr. Admin!")
                    st.rerun()
                else:
                    st.error("❌ Access Denied: Invalid credentials")
        
        st.markdown("""
            <div style='text-align: center; color: #64748B; font-size: 0.8em; margin-top: 20px;'>Medical Dashboard System | Authorized Use Only</div>
        """, unsafe_allow_html=True)

def main_app():
    apply_custom_style()
    
    st.markdown("""
        <div class='hospital-header'>
            <h1>🏥 Medical Dashboard</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Live Statistics
    records = load_all_records()
    if not records.empty:
        total_patients = len(records)
        high_risk = len(records[records['Risk'] == 'High'])
        low_risk = len(records[records['Risk'] == 'Low'])
        high_risk_pct = (high_risk / total_patients * 100)
    else:
        total_patients, high_risk, low_risk, high_risk_pct = 0, 0, 0, 0

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Patients", total_patients)
    with col2: st.metric("High Risk", high_risk, delta_color="inverse")
    with col3: st.metric("Low Risk", low_risk)
    with col4: st.metric("Risk Rate", f"{high_risk_pct:.1f}%")

    st.sidebar.markdown("### 👨‍⚕️ Medical Menu")
    menu_options = {
        "Predictor": "📝 Patient Assessment",
        "Archive": "📂 Patient Records",
        "Analytics": "📊 Analytics",
        "CT Scan": "🖼️ Imaging Analysis",
        "Schedule": "🗓️ Appointments",
        "Dr. AI": "🤖 Virtual Assistant"
    }
    choice = st.sidebar.radio("Navigation", list(menu_options.keys()), format_func=lambda x: menu_options[x])
    
    if st.sidebar.button("🔒 Logout"):
        st.session_state['logged_in'] = False
        st.rerun()
    
    # --- Content ---
    if choice == "Predictor":
        st.markdown("### 📝 Patient Assessment")
        model_path = 'models/lung_cancer_model.pkl'
        
        if not os.path.exists(model_path):
            st.error("⚠️ Model error.")
        else:
            # Phase 1: Registration
            if not st.session_state['reg_complete']:
                with st.form("reg_form"):
                    st.markdown("#### Step 1: Patient Registration")
                    r1, r2 = st.columns(2)
                    with r1:
                        p_name = st.text_input("Full Patient Name")
                        phone = st.text_input("Phone Number")
                    with r2:
                        location = st.text_input("Location / Address")
                        gender = st.selectbox("Gender", ["Male", "Female"])
                    
                    age = st.slider("Patient Age", 18, 100, 50)
                    
                    if st.form_submit_button("✅ Register Patient"):
                        if not p_name or not phone:
                            st.warning("⚠️ Please provide Patient Name and Phone Number.")
                        else:
                            st.session_state['patient_reg_info'] = {
                                'Patient Name': p_name,
                                'Phone': phone,
                                'Location': location,
                                'GENDER': 1 if gender == "Male" else 0,
                                'AGE': age,
                                'Gender_Str': gender # For display
                            }
                            st.session_state['reg_complete'] = True
                            st.success(f"🎊 Patient {p_name} registered successfully!")
                            st.rerun()
            
            # Phase 2: Clinical Assessment
            else:
                p_info = st.session_state['patient_reg_info']
                st.info(f"📋 Assessing: **{p_info['Patient Name']}** | {p_info['Gender_Str']}, {p_info['AGE']} yrs")
                
                with st.form("assessment_form"):
                    st.markdown("#### Step 2: Clinical Questions")
                    smoking = st.selectbox("Smoking History", ["No", "Yes"])
                    alcohol = st.selectbox("Alcohol Consumption", ["No", "Yes"])
                    
                    feat_list = ["Yellow Fingers", "Anxiety", "Peer Pressure", "Chronic Disease", "Fatigue", "Allergy", "Wheezing", "Coughing", "Shortness of Breath", "Swallowing Difficulty", "Chest Pain"]
                    user_vals = {}
                    c1, c2 = st.columns(2)
                    for i, f in enumerate(feat_list):
                        with (c1 if i < len(feat_list)//2 else c2):
                            user_vals[f] = st.selectbox(f, ["No", "Yes"])
                    
                    col_btn1, col_btn2 = st.columns([1, 4])
                    with col_btn1:
                        if st.form_submit_button("⬅️ Back"):
                            st.session_state['reg_complete'] = False
                            st.rerun()
                    with col_btn2:
                        submit_asmt = st.form_submit_button("🚀 Run Risk Analysis")

                    if submit_asmt:
                        model = joblib.load(model_path)
                        # Exact Mapping
                        feature_mapping = {
                            "Smoking": "SMOKING", "Yellow Fingers": "YELLOW_FINGERS", "Anxiety": "ANXIETY",
                            "Peer Pressure": "PEER_PRESSURE", "Chronic Disease": "CHRONIC DISEASE",
                            "Fatigue": "FATIGUE ", "Allergy": "ALLERGY ", "Wheezing": "WHEEZING",
                            "Alcohol": "ALCOHOL CONSUMING", "Coughing": "COUGHING",
                            "Shortness of Breath": "SHORTNESS OF BREATH", "Swallowing Difficulty": "SWALLOWING DIFFICULTY",
                            "Chest Pain": "CHEST PAIN"
                        }
                        
                        # Build full data row
                        input_row = {
                            'GENDER': p_info['GENDER'], 
                            'AGE': p_info['AGE'], 
                            'SMOKING': 1 if smoking=="Yes" else 0, 
                            'ALCOHOL CONSUMING': 1 if alcohol=="Yes" else 0
                        }
                        for k, v in user_vals.items():
                            input_row[feature_mapping.get(k, k.upper())] = 1 if v=="Yes" else 0
                        
                        df = pd.DataFrame([input_row])
                        
                        # Reorder columns to match the model's expected order
                        expected_features = [
                            'GENDER', 'AGE', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY', 
                            'PEER_PRESSURE', 'CHRONIC DISEASE', 'FATIGUE ', 'ALLERGY ', 
                            'WHEEZING', 'ALCOHOL CONSUMING', 'COUGHING', 
                            'SHORTNESS OF BREATH', 'SWALLOWING DIFFICULTY', 'CHEST PAIN'
                        ]
                        df = df[expected_features]
                        
                        pred = model.predict(df)[0]
                        prob = model.predict_proba(df)[0][1]
                        
                        # Save result to session state to show outside form
                        st.session_state['last_result'] = {
                            'pred': pred,
                            'prob': prob,
                            'p_name': p_info['Patient Name']
                        }
                        
                        # Save to DB
                        final_record = {
                            **p_info,
                            **input_row,
                            'Risk': 'High' if pred==1 else 'Low',
                            'Probability': prob
                        }
                        final_record.pop('Gender_Str', None)
                        save_patient_record(final_record)
                        st.toast("✅ Record archived successfully.")
                        st.rerun()

                # Display Results Outside Form
                if 'last_result' in st.session_state:
                    res = st.session_state['last_result']
                    st.divider()
                    if res['pred'] == 1: 
                        st.markdown(f"""
                            <div style='background-color: #E76F51; color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 10px 20px rgba(231, 111, 81, 0.2); font-weight: bold; font-size: 16px; border-left: 8px solid #FFFFFF;'>
                                <span style='background: white; color: #E76F51; padding: 4px 12px; border-radius: 6px; margin-right: 12px;'>🚨 CRITICAL: HIGH RISK</span> Patient Assessment Result
                                <div style='font-size: 28px; margin-top: 10px; color: #FFFFFF;'>Probability: {res['prob']:.1%}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    elif res['prob'] > 0.4:
                        st.markdown(f"""
                            <div style='background-color: #6C757D; color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 10px 20px rgba(108, 117, 125, 0.2); font-weight: bold; font-size: 16px; border-left: 8px solid #ADB5BD;'>
                                <span style='background: white; color: #6C757D; padding: 4px 12px; border-radius: 6px; margin-right: 12px;'>⚠️ WARNING: MEDIUM RISK</span> Patient Assessment Result
                                <div style='font-size: 28px; margin-top: 10px; color: #FFFFFF;'>Probability: {res['prob']:.1%}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    else: 
                        st.markdown(f"""
                            <div style='background-color: #6A994E; color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 10px 20px rgba(106, 153, 78, 0.2); font-weight: bold; font-size: 16px; border-left: 8px solid #FFFFFF;'>
                                <span style='background: white; color: #6A994E; padding: 4px 12px; border-radius: 6px; margin-right: 12px;'>✅ STABLE: LOW RISK</span> Patient Assessment Result
                                <div style='font-size: 28px; margin-top: 10px; color: #FFFFFF;'>Probability: {res['prob']:.1%}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    if st.button("🔄 Start New Assessment"):
                        st.session_state['reg_complete'] = False
                        st.session_state['patient_reg_info'] = {}
                        del st.session_state['last_result']
                        st.rerun()

    elif choice == "Archive":
        st.markdown("### 📂 Patient Records")
        st.dataframe(load_all_records(), use_container_width=True)

    elif choice == "Analytics":
        st.markdown("### 📊 Analytics")
        from src.analytics import AnalyticsDashboard
        analytics = AnalyticsDashboard("")
        if not records.empty:
            st.plotly_chart(analytics.get_risk_distribution(records), use_container_width=True)
            st.plotly_chart(analytics.get_risk_cluster_nebula(records), use_container_width=True)

    elif choice == "CT Scan":
        st.markdown("### 🖼️ CT Imaging Analysis")
        uploaded_file = st.file_uploader("Upload Medical Scan (CT/X-Ray)", type=["jpg", "png", "jpeg"])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Scan for Analysis", width=500)
            
            # Reset result if a new file is uploaded (optional logic)
            # if 'uploaded_file_name' in st.session_state and st.session_state['uploaded_file_name'] != uploaded_file.name:
            #     st.session_state['ct_result'] = None
            # st.session_state['uploaded_file_name'] = uploaded_file.name

            if st.button("🚀 Execute Diagnostic Scan"):
                st.session_state['ct_scanning'] = True
                st.rerun()

            if st.session_state.get('ct_scanning'):
                with st.spinner("🔍 AI Analysis in progress..."):
                    import time
                    from src.image_model import predict_image
                    
                    time.sleep(2)
                    # Run actual prediction
                    prob = predict_image(uploaded_file)
                    st.session_state['ct_result'] = prob
                
                st.session_state['ct_scanning'] = False
                st.rerun()

            # Display Persistent Result
            if st.session_state.get('ct_result') is not None:
                prob = st.session_state['ct_result']
                st.divider()
                
                # Level Classification Logic
                if prob > 0.7:
                    level = "HIGH LEVEL"
                    desc = "Critical malignant signatures detected. Immediate specialist intervention required."
                    color = "#E76F51" # Soft Red
                    icon = "🚨"
                elif prob > 0.4:
                    level = "MEDIUM LEVEL"
                    desc = "Suspicious radiographic signatures identified. Further diagnostic screening recommended."
                    color = "#F59E0B" # Amber
                    icon = "⚠️"
                else:
                    level = "LOW LEVEL"
                    desc = "Benign study. No immediate malignant indicators found. Regular follow-up protocol suggested."
                    color = "#6A994E" # Muted Green
                    icon = "✅"

                st.markdown(f"""
                    <div style='background-color: {color}; color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 15px 30px rgba(0,0,0,0.1); font-weight: bold; border-left: 10px solid #FFFFFF;'>
                        <div style='font-size: 0.9em; text-transform: uppercase; margin-bottom: 5px; opacity: 0.9;'>Diagnostic Analysis Result</div>
                        <div style='font-size: 26px;'>{icon} {level}: {prob:.1%} Match</div>
                        <div style='margin-top: 10px; font-weight: 500; font-size: 14px;'>{desc}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("🗑️ Clear Result"):
                    st.session_state['ct_result'] = None
                    st.rerun()

    elif choice == "Schedule":
        st.markdown("### 🗓️ Appointments")
        appts = load_all_appointments()
        st.dataframe(appts, use_container_width=True)

    elif choice == "Dr. AI":
        st.markdown("### 🤖 Dr. AI Assistant")
        if query := st.chat_input("Ask Dr. AI..."):
            with st.chat_message("user"): st.write(query)
            with st.chat_message("assistant"):
                from src.chatbot import DrAIChatbot
                st.write(DrAIChatbot().get_response(query))

    st.markdown("<div style='text-align: center; color: #64748B; font-size: 0.8em; margin-top: 20px;'>Medical Dashboard System | 2026</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    if not st.session_state.get('logged_in'): login_page()
    else: main_app()