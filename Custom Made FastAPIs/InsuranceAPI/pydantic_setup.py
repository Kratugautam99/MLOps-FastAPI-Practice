from Cities_Data import tier_1_cities, tier_2_cities
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal,Annotated

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
    
    @field_validator("city")
    def validate_city(cls, value):
        return value.strip().title()
    