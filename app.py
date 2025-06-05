import streamlit as st
import numpy as np
import pickle
import time
import pandas as pd

# Set page configuration and styling
st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for fonts, colors, and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Montserrat:wght@300;400;500&display=swap');
    
    * {
        font-family: 'Montserrat', sans-serif;
        transition: all 0.4s ease-in-out;
    }
    
    /* 3D animation container for the entire app */
    .stApp {
        perspective: 1000px;
    }
    
    h1, h2, h3 {
        font-family: 'Cormorant Garamond', serif;
        color: #e6d2c9 !important;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    .main-header {
        font-size: 3.2rem;
        background: linear-gradient(135deg, #d7c0b0, #e6d2c9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        animation: fadeIn 1.8s ease-out, shimmer 8s infinite alternate, float 6s ease-in-out infinite;
        transform-style: preserve-3d;
        text-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    p, label, text {
        color: #d7c0b0 !important;
        letter-spacing: 0.3px;
    }
    
    .stButton > button {
        background-color: #c9ae9c;
        color: #1e1e1e !important;
        border-radius: 50px;
        padding: 0.5rem 2.5rem;
        font-weight: 500;
        letter-spacing: 1px;
        transition: all 0.3s;
        border: none;
        box-shadow: 0 4px 12px rgba(201, 174, 156, 0.2);
        animation: pulse 2s infinite;
        transform: translateZ(20px);
    }
    
    .stButton > button:hover {
        background-color: #d7c0b0;
        box-shadow: 0 6px 15px rgba(201, 174, 156, 0.3);
        transform: translateY(-3px) translateZ(30px) rotateX(5deg);
    }
    
    .form-container {
        background-color: rgba(201, 174, 156, 0.08);
        padding: 2.5rem;
        border-radius: 15px;
        border: 1px solid rgba(201, 174, 156, 0.15);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        animation: floatContainer 8s ease-in-out infinite, slideIn 1s ease-out;
        transform-style: preserve-3d;
        transform: perspective(1000px) rotateX(2deg) rotateY(1deg);
        transition: transform 0.5s ease;
    }
    
    .form-container:hover {
        transform: perspective(1000px) rotateX(-1deg) rotateY(-2deg);
    }
    
    .result-container {
        padding: 1.8rem;
        border-radius: 12px;
        margin-top: 2rem;
        animation: popIn 0.7s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        transition: transform 0.5s ease, box-shadow 0.5s ease;
        transform-style: preserve-3d;
        transform: perspective(800px) rotateX(2deg) translateZ(0);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    
    .result-container:hover {
        transform: perspective(800px) rotateX(7deg) rotateY(-3deg) translateZ(20px);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.2), 
                    -5px 0 15px rgba(201, 174, 156, 0.05),
                    5px 0 15px rgba(201, 174, 156, 0.05);
    }
    
    .positive-result {
        background-color: rgba(201, 174, 156, 0.15);
        border-left: 5px solid #d7b19b;
        box-shadow: 0 15px 30px rgba(215, 177, 155, 0.15);
    }
    
    .negative-result {
        background-color: rgba(169, 190, 169, 0.15);
        border-left: 5px solid #a9bea9;
        box-shadow: 0 15px 30px rgba(169, 190, 169, 0.15);
    }
    
    /* 3D styled input fields */
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 1px solid rgba(201, 174, 156, 0.3);
        background-color: rgba(201, 174, 156, 0.05);
        color: #d7c0b0 !important;
        transition: all 0.3s ease;
        transform: translateZ(0);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: rgba(201, 174, 156, 0.8);
        box-shadow: 0 0 0 2px rgba(201, 174, 156, 0.2), inset 0 2px 4px rgba(0,0,0,0.05);
        transform: translateZ(5px);
    }
    
    div[data-baseweb="base-input"] > input {
        color: #d7c0b0 !important;
    }
    
    .st-bq {
        color: #d7c0b0 !important;
    }
    
    div.stNumberInput label {
        color: #d7c0b0 !important;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    
    /* 3D-specific animations */
    @keyframes float {
        0%, 100% { transform: translateZ(0) translateY(0); }
        50% { transform: translateZ(20px) translateY(-10px); }
    }
    
    @keyframes floatContainer {
        0%, 100% { transform: perspective(1000px) rotateX(2deg) rotateY(1deg) translateZ(0); }
        50% { transform: perspective(1000px) rotateX(1deg) rotateY(2deg) translateZ(10px); }
    }
    
    /* Regular animations */
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    
    @keyframes slideIn {
        0% { opacity: 0; transform: translateY(30px) perspective(1000px) rotateX(10deg); }
        100% { opacity: 1; transform: translateY(0) perspective(1000px) rotateX(2deg) rotateY(1deg); }
    }
    
    @keyframes popIn {
        0% { opacity: 0; transform: scale(0.9) perspective(800px) rotateX(10deg); }
        100% { opacity: 1; transform: scale(1) perspective(800px) rotateX(2deg); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(201, 174, 156, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(201, 174, 156, 0); }
        100% { box-shadow: 0 0 0 0 rgba(201, 174, 156, 0); }
    }
    
    @keyframes shimmer {
        0% { background-position: -100% 0; }
        100% { background-position: 200% 0; }
    }
    
    /* 3D card flip effect for About section */
    .about-container {
        position: relative;
        width: 100%;
        height: 200px;
        margin-top: 3.5rem;
        perspective: 1500px;
    }
    
    .about-card {
        position: relative;
        width: 100%;
        height: 100%;
        transition: transform 0.8s;
        transform-style: preserve-3d;
    }
    
    .about-container:hover .about-card {
        transform: rotateY(180deg);
    }
    
    .about-front, .about-back {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        padding: 2rem;
        background-color: rgba(201, 174, 156, 0.08);
        border-radius: 12px;
        border: 1px solid rgba(201, 174, 156, 0.15);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }
    
    .about-back {
        transform: rotateY(180deg);
    }
    
    /* Streamlit elements styling */
    .element-container {
        opacity: 0;
        animation: fadeIn 0.8s ease-out forwards;
        transform-style: preserve-3d;
    }
    
    /* Staggered animation timing for elements */
    .element-container:nth-child(1) { animation-delay: 0.1s; }
    .element-container:nth-child(2) { animation-delay: 0.2s; }
    .element-container:nth-child(3) { animation-delay: 0.3s; }
    .element-container:nth-child(4) { animation-delay: 0.4s; }
    .element-container:nth-child(5) { animation-delay: 0.5s; }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.2rem;
        }
    }
    
    /* Make JSON container 3D */
    .json-container {
        background-color: rgba(201, 174, 156, 0.08);
        border-radius: 10px;
        border: 1px solid rgba(201, 174, 156, 0.15);
        padding: 5px;
        animation: fadeIn 1s ease-out;
        transform-style: preserve-3d;
        transform: perspective(800px) rotateX(2deg);
        transition: transform 0.5s ease;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    .json-container:hover {
        transform: perspective(800px) rotateX(5deg) rotateY(2deg);
    }
</style>
""", unsafe_allow_html=True)

# Load trained model
try:
    with open("model.pkl", "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("❌ model.pkl not found. Please make sure the trained model is saved in the same folder.")
    st.stop()

# App Title with animation effect
st.markdown("<h1 class='main-header'>🩺 Diabetes Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 1.1rem; color: #c9ae9c; margin-bottom: 2.5rem; font-weight: 300;'>Elegant analysis of your health parameters</p>", unsafe_allow_html=True)

# Animated progress
with st.container():
    placeholder = st.empty()
    placeholder.markdown("<div class='form-container'>", unsafe_allow_html=True)

# User Input Form with enhanced styling
with st.form("prediction_form"):
    st.markdown("<h3 style='color: #d7c0b0; margin-bottom: 1.8rem; font-size: 1.8rem;'>Patient Details</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:
        pregnancies = st.number_input("Number of Pregnancies", min_value=0, max_value=20, step=1)
        glucose = st.number_input("Glucose Level (mg/dL)", min_value=0.0, max_value=300.0, step=1.0)
        blood_pressure = st.number_input("Blood Pressure (mm Hg)", min_value=0.0, max_value=200.0, step=1.0)
        skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0.0, max_value=100.0, step=1.0)

    with col2:
        insulin = st.number_input("Insulin Level (μU/ml)", min_value=0.0, max_value=900.0, step=1.0)
        bmi = st.number_input("BMI (kg/m²)", min_value=0.0, max_value=100.0, step=0.1)
        dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, step=0.01)
        age = st.number_input("Age (years)", min_value=1, max_value=120, step=1)

    submitted = st.form_submit_button("Predict")

# Prediction with animation
if submitted:
    # Add a progress animation with an elegant feel
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Simulate processing time with more elegant messages
    for i in range(100):
        progress_bar.progress(i + 1)
        if i < 25:
            status_text.markdown("<p style='color: #c9ae9c;'>Analyzing health parameters...</p>", unsafe_allow_html=True)
        elif i < 50:
            status_text.markdown("<p style='color: #c9ae9c;'>Evaluating medical indicators...</p>", unsafe_allow_html=True)
        elif i < 75:
            status_text.markdown("<p style='color: #c9ae9c;'>Assessing risk profile...</p>", unsafe_allow_html=True)
        else:
            status_text.markdown("<p style='color: #c9ae9c;'>Finalizing your health assessment...</p>", unsafe_allow_html=True)
        time.sleep(0.015)  # Slightly slower for elegance
    
    # Clear the animation elements
    progress_bar.empty()
    status_text.empty()
    
    # Make the prediction
    feature_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    user_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
    
    # Create DataFrame with feature names to avoid the warning
    user_df = pd.DataFrame(user_data, columns=feature_names)
    prediction = model.predict(user_df)

    # Display result with animation
    if prediction[0] == 1:
        st.markdown("""
        <div class='result-container positive-result'>
            <h3 style='color: #d7b19b; font-size: 1.6rem;'>⚠️ Diabetes Risk Detected</h3>
            <p style='color: #c9ae9c !important; line-height: 1.6;'>Based on the provided parameters, this profile indicates a <b>higher likelihood of Diabetes</b>.</p>
            <p style='color: #c9ae9c !important; line-height: 1.6;'>A consultation with a healthcare professional is recommended for proper evaluation.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='result-container negative-result'>
            <h3 style='color: #a9bea9; font-size: 1.6rem;'>✅ Low Diabetes Risk</h3>
            <p style='color: #c9ae9c !important; line-height: 1.6;'>Based on the provided parameters, this profile indicates a <b>lower likelihood of Diabetes</b>.</p>
            <p style='color: #c9ae9c !important; line-height: 1.6;'>Maintaining a balanced lifestyle is always beneficial for long-term health.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display a summary of the input data
    st.markdown("<h3 style='margin-top: 2.5rem; color: #d7c0b0; font-size: 1.5rem;'>Parameter Summary</h3>", unsafe_allow_html=True)
    
    # Customize the JSON container style
    st.markdown("<div class='json-container'>", unsafe_allow_html=True)
    summary_data = {
        "Pregnancies": pregnancies,
        "Glucose Level": f"{glucose} mg/dL",
        "Blood Pressure": f"{blood_pressure} mm Hg",
        "Skin Thickness": f"{skin_thickness} mm",
        "Insulin Level": f"{insulin} μU/ml",
        "BMI": f"{bmi} kg/m²",
        "Diabetes Pedigree Function": dpf,
        "Age": f"{age} years"
    }
    
    st.json(summary_data)
    st.markdown("</div>", unsafe_allow_html=True)

# Add information section with 3D card effect
st.markdown("""
<div class="about-container">
    <div class="about-card">
        <div class="about-front">
            <h3 style='color: #d7c0b0; font-size: 1.5rem;'>About This Tool</h3>
            <p style='color: #c9ae9c !important; line-height: 1.6; font-weight: 300;'>This elegant diabetes prediction tool employs advanced machine learning to assess diabetes risk.</p>
            <p style='color: #c9ae9c !important; font-style: italic; text-align: center; margin-top: 20px;'>Hover to learn more...</p>
        </div>
        <div class="about-back">
            <h3 style='color: #d7c0b0; font-size: 1.5rem;'>How It Works</h3>
            <p style='color: #c9ae9c !important; line-height: 1.6; font-weight: 300;'>The analysis is based on a trained model and is designed to complement, not replace, professional medical guidance. The predictor analyzes multiple health factors to provide an assessment of diabetes risk.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Close the form container div
st.markdown("</div>", unsafe_allow_html=True)
