import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.markdown("""
    <style>
    /* Main background with futuristic gradient */
    .stApp {
        background: linear-gradient(135deg, #000428 0%, #004e92 100%);
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Futuristic header with glow effect */
    .main-header {
        font-size: 3rem;
        color: #00c6ff;
        text-align: center;
        margin-bottom: 1.5rem;
        text-shadow: 0 0 10px #00c6ff, 0 0 20px #00c6ff, 0 0 30px #0072ff;
        font-weight: 800;
        letter-spacing: 1px;
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Subheaders with cyberpunk style */
    .subheader {
        font-size: 1.5rem;
        color: #00c6ff;
        margin-bottom: 1rem;
        font-weight: 600;
        text-shadow: 0 0 5px #00c6ff;
        letter-spacing: 0.5px;
    }
    
    /* Glassmorphism input sections */
    .input-section {
        background: rgba(0, 10, 30, 0.7);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(0, 198, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 114, 255, 0.2);
    }
    
    /* Futuristic input fields */
    .stNumberInput, .stTextInput, .stSelectbox {
        background-color: rgba(0, 20, 40, 0.8) !important;
        border-radius: 10px;
        padding: 0.5rem;
        border: 1px solid #00c6ff;
        color: #ffffff;
        box-shadow: 0 0 10px rgba(0, 198, 255, 0.3);
    }
    
    /* Slider styling */
    .stSlider div[data-testid="stSlider"] > div {
        color: #00c6ff;
    }
    
    /* Neon button with glow effect */
    .stButton>button {
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
        color: #000;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: bold;
        margin-top: 1.5rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.7);
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #00deff 0%, #0082ff 100%);
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(0, 198, 255, 0.9);
    }
    
    /* Success message with futuristic style */
    .success-box {
        background: rgba(0, 30, 60, 0.7);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(0, 198, 255, 0.5);
        margin: 1.5rem 0;
        box-shadow: 0 0 20px rgba(0, 114, 255, 0.3);
    }
    
    /* Metric boxes */
    .metric-box {
        background: rgba(0, 20, 40, 0.7);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #00c6ff;
        box-shadow: 0 0 10px rgba(0, 198, 255, 0.2);
    }
    
    /* Label styling */
    .stNumberInput label, .stTextInput label, .stSelectbox label {
        color: #00c6ff !important;
        font-weight: 500;
        text-shadow: 0 0 3px rgba(0, 198, 255, 0.5);
    }
    
    /* JSON display */
    .stJson {
        background-color: rgba(0, 20, 40, 0.8) !important;
        border: 1px solid #00c6ff;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 198, 255, 0.2);
    }
    
    /* Custom divider */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #00c6ff, transparent);
        margin: 1.5rem 0;
    }
    
    /* Futuristic card style */
    .futuristic-card {
        background: rgba(0, 15, 35, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 198, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 114, 255, 0.2);
        margin-bottom: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Insurance Premium Category Predictor")
st.markdown("Enter your details below:")

age = st.number_input("Age", min_value=1, max_value=119, value=30, key="age_input")
weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0, key="weight_input")
height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7, key="height_input")
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0, key="income_input")
smoker = st.selectbox("Are you a smoker?", options=[True, False], key="smoker_input")
city = st.text_input("City", value="Mumbai", key="city_input")
occupation = st.selectbox(
    "Occupation",
    ['Retired', 'Freelancer', 'Student', 'Government_job', 'Business_owner', 'Unemployed', 'Private_job']
, key="occupation_input")

if st.button("Predict Premium Category"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation.lower()
    }

    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        if response.status_code == 200 and "response" in result:
            prediction = result["response"]
            st.success(f"Predicted Insurance Premium Category: **{prediction['predicted_category']}**")
            st.write("🔍 Confidence:", prediction["confidence"])
            st.write("📊 Class Probabilities:")
            st.json(prediction["class_probabilities"])

        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")