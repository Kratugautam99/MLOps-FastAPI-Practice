from pydantic import BaseModel, Field
from typing import Dict

class PredictedResponse(BaseModel):
    predicted_category: str = Field(description="The predicted insurance risk category for the user.", example="medium")
    confidence: float = Field(description="Confidence level of the prediction.", example=0.85)
    class_probabilities: Dict[str, float] = Field(description="Probabilities for each risk category.", example={"low": 0.1, "medium": 0.85, "high": 0.05})
    