from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field 
from typing import Literal,Annotated
import pandas as pd
import pickle

with open("insurance_model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI(
    title="🛡️ Insurance Risk Predictor API",
    description="""
    Welcome to the Insurance Risk Predictor API — your intelligent gateway to assessing insurance risk profiles 
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

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

class UserData(BaseModel):
    age: Annotated[int, Field(gt=0,It=120, description="Age of the user in years", example=30)]
    height: Annotated[float, Field(gt=0, description="Height of the user in meters", example=1.75)]
    weight: Annotated[float, Field(gt=0, description="Weight of the user in kilograms", example=70)]
    income_lpa: Annotated[float, Field(gt=0, description="Annual income of the user in lakhs per annum", example=10.5)]
    smoker: Annotated[bool, Field(description="Smoking status of the user", example=False)]
    city: Annotated[str, Field(description="City of residence of the user", example="Chennai")]
    occupation: Annotated[Literal["retired", "student", "unemployed", "business_owner", "private_job", "government_job", "freelancer"],Field(description="Occupation of the user", example="private_job")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        return "high" if self.smoker and self.bmi > 30 else "medium" if self.smoker or self.bmi > 27 else "low"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
    
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
@app.post("/predict")
def predict_premium(user_data: UserData):
    input_df = pd.DataFrame([{
        'bmi': user_data.bmi,
        'age_group': user_data.age_group,
        'lifestyle_risk': user_data.lifestyle_risk,
        'city_tier': user_data.city_tier,
        'income_lpa': user_data.income_lpa,
        'occupation': user_data.occupation
    }])

    prediction = model.predict(input_df)[0]
    return JSONResponse(status_code=200, content= {"predicted_category":prediction})