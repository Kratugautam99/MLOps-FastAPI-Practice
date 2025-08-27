from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic_setup import UserData
from response_model import PredictedResponse
from model_functions import predict_from_model, MODEL_VERSION, model

app = FastAPI(
    title="🛡️ Insurance Premium Category Predictor API",
    description="""
    Welcome to the Insurance Premium Category Predictor API — your intelligent gateway to assessing insurance premium category profiles 
    using machine learning. This API transforms user health and lifestyle data into actionable insights, 
    helping insurers and analysts make smarter, faster decisions.

    🚀 Features:
    - BMI auto-calculation from height and weight
    - City tier classification for regional risk modeling
    - Occupation-based risk segmentation
    - Seamless integration with trained ML models

    Built for speed. Designed for clarity. Ready for production.
    """.strip(),
    version="1.0"
)

@app.get("/")
def home():
    return {"message": "Welcome to the Insurance Premium Predictor API. Use the /predict endpoint to get predictions."}

@app.get("/health")
def health_check():
    return {"status": "OK", "version": MODEL_VERSION, "model_version": model is not None}

@app.post("/predict", response_model=PredictedResponse)
def predict_premium(user_data: UserData):
    inputs = {
        'bmi': user_data.bmi,
        'age_group': user_data.age_group,
        'lifestyle_risk': user_data.lifestyle_risk,
        'city_tier': user_data.city_tier,
        'income_lpa': user_data.income_lpa,
        'occupation': user_data.occupation
    }
    
    prediction = predict_from_model(inputs)
    return JSONResponse(status_code=200, content= {"response":prediction})