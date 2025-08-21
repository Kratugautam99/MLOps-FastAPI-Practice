import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: #f0f0f0;
    }
    h1, h2, h3 {
        color: #00bfff !important;
    }
    label, .stMarkdown, .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: #f0f0f0 !important;
        font-weight: bold;
    }
    input, select, textarea {
        background-color: #111 !important;
        color: #00bfff !important;
        border: 1px solid #00bfff !important;
        border-radius: 5px !important;
    }
    .stTextInput > div > input,
    .stNumberInput > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > textarea {
        background-color: #111 !important;
        color: #00bfff !important;
        border: 1px solid #00bfff !important;
        border-radius: 5px !important;
    }
    .stButton > button {
        background-color: #00bfff !important;
        color: #000 !important;
        font-weight: bold;
        border-radius: 5px;
        transition: background 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0090cc !important;
        color: #fff !important;
    }
    .stSuccess {
        background-color: #003366 !important;
        border-left: 5px solid #00bfff !important;
        color: #f0f0f0 !important;
    }
    .stError {
        background-color: #330000 !important;
        border-left: 5px solid #ff4b4b !important;
        color: #f0f0f0 !important;
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
    ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job']
, key="occupation_input")

if st.button("Predict Premium Category"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        if response.status_code == 200 and "predicted_category" in result:
            st.success(f"Predicted Insurance Premium Category: **{result['predicted_category']}**")
        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")
