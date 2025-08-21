from fastapi.responses import JSONResponse
from typing import Annotated, Literal, Optional
from pydantic import BaseModel, Field, computed_field
from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI(title="🩺 Doctor API: Comprehensive Patient Data Management", description="""
The Doctor API is a RESTful interface built to streamline the handling of patient records and health-related data within clinical or healthcare applications. It provides a robust set of endpoints for retrieving, sorting, searching, and adding patient information, ensuring that healthcare providers can access and manage data efficiently and securely.

This API adheres to the OpenAPI 3.1 specification, offering clear documentation and schema validation for consistent integration across platforms. It is ideal for use in electronic health record (EHR) systems, telemedicine platforms, and hospital management software.

✨ Key Functionalities
Patient Retrieval: Fetch all patient records or view enriched details for individual patients using unique identifiers or names.

Data Sorting: Organize patient data based on specific attributes (e.g., age, name) to support clinical workflows and reporting.

Record Creation: Add new patient entries with structured health and contact information using validated request bodies.

Schema Validation: Ensures data integrity through strict adherence to predefined models like Patient_Details, reducing errors and improving reliability.

Error Handling: Implements standardized validation error responses (HTTPValidationError, ValidationError) for seamless debugging and user feedback.

🧠 Use Case Scenarios
Hospital Dashboards: Populate patient lists and enable quick access to individual profiles.

Clinical Decision Support: Sort and filter patients based on health metrics or demographics.

Patient Intake Systems: Automate onboarding of new patients with structured data capture.

Health Analytics: Aggregate and analyze patient data for trends, outcomes, and resource planning.

This API is designed with extensibility in mind, allowing developers to build upon its foundation with additional endpoints for updating, deleting, or analyzing patient health summaries. It supports modern backend frameworks like FastAPI and integrates seamlessly with frontend tools and cloud deployments.""", version="2.0")

def load_data():
    with open("patients.json","r") as f:
        return json.load(f)
    
def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)

class Patient_Details(BaseModel):
    id: Annotated[str, Field(..., description="Unique patient ID", example="P001")]
    name: Annotated[str, Field(..., description="Full name of the patient", example="Ananya Verma")]
    city: Annotated[str, Field(..., description="City of residence", example="Delhi")]
    age: Annotated[int, Field(..., description="Age of the patient", ge=0, le=120, example=30)]
    gender: Annotated[Literal["Male","Female","Others"], Field(..., description="Gender of the patient", example="Male")]
    height: Annotated[float, Field(..., description="Height in meters", ge=0.0, example=1.75)]
    weight: Annotated[float, Field(..., description="Weight in kilograms", ge=0.0, example=70.0)]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal"  
        elif 25 <= self.bmi < 29.9:
            return "Overweight" 
        else:
            return "Obese"
        
class Patient_Update(BaseModel):
    name: Annotated[Optional[str], Field(None, description="Full name of the patient", example="New Name")]
    city: Annotated[Optional[str], Field(None, description="City of residence", example="New City")]
    age: Annotated[Optional[int], Field(None, description="Age of the patient", ge=0, le=120, example=1)] 
    gender: Annotated[Optional[Literal["Male","Female","Others"]], Field(None, description="Gender of the patient", example="Change Gender")]
    height: Annotated[Optional[float], Field(None, description="Height in meters", ge=0.0, example=1)]
    weight: Annotated[Optional[float], Field(None, description="Weight in kilograms", ge=0.0, example=1)]
    
@app.get("/")
async def root():
    return {"message": "Welcome to the Doctor API! Use /patients to know about patient methods or refer /docs."}

@app.get("/patients")
async def instructions():
    return {
        "message": "To get information about a patient, use /patients/name/{name} or /patients/add or /patients/edit or /patients/delete or /patients/id/{pid} or /patients/view/sort?sort_by={height,weight,age,bmi}&order_by={asc,desc} => to view all patients and /sort is optional"
    }

@app.get("/patients/view")
async def get_patients():
    patients = load_data()
    return {"patients": patients}

@app.get("/patients/view/sort")
async def sort_patients(sort_by: str = Query(..., description="Sort patients by height, weight, bmi or age.", example="height"), order_by: str = Query("asc", description="Order of sorting: 'asc' for ascending and 'desc' for descending.", example="asc")):
    if sort_by not in ["height", "weight", "bmi", "age"]:
        raise HTTPException(status_code=400, detail="Invalid sort parameter. Use 'height', 'weight', 'bmi', or 'age'.")
    if order_by not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order parameter. Use 'asc' or 'desc' only.")
    patients = load_data()
    sorted_patients = sorted(patients.items(), key=lambda x: x[1][sort_by], reverse=(order_by == "desc"))
    return sorted_patients
    

@app.get("/patients/id/{pid}")
async def patient(pid: str = Path(..., description="Enter the patient ID to get their details.", example="P001")):
    patients = load_data()
    if pid in patients:
        info = patients[pid]
        return {
            "message": f"The Registered patient with ID = {pid} and Name = {info['name']} have some important details like City = {info['city']}, Age = {info['age']}, Gender = {info['gender']}, Height = {info['height']}, Weight = {info['weight']}, Body-Mass Index = {info['bmi']}, Verdict = {info['verdict']}."
        }
    raise HTTPException(status_code=404, detail="Patient not found with the given ID.")

@app.get("/patients/name/{name}")
async def doctor(name: str = Path(..., description="Enter the name of the patient to get their details.", example="Ananya Verma")):
    patients = load_data()
    for pid, info in patients.items():
        if info["name"].lower() == name.lower():
            return {
                "message": f"Hello, {info['name']}! You are a registered patient. ID = {pid} with Important Details like City = {info['city']}, Age = {info['age']}, Gender = {info['gender']}, Height = {info['height']}, Weight = {info['weight']}, Body-Mass Index = {info['bmi']}, Verdict = {info['verdict']}."
            }
    raise HTTPException(status_code=404, detail="Patient not found with the given name.")

@app.post("/patients/add")
async def add_patient(patient: Patient_Details):
    patients = load_data()
    if patient.id in patients:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.") 
    patients[patient.id] = patient.model_dump(exclude=["id"])
    save_data(patients)
    return JSONResponse(status_code=201, content={"message": f"Patient {patient.name} with ID {patient.id} has been added successfully."})

@app.put("/patients/edit")
async def update_patient(patient_update: Patient_Update, pid: str = Query(..., description="Write Patient ID to edit", example="P001")):
    patients = load_data()
    if pid not in patients:
        raise HTTPException(status_code=404, detail="Patient not found with the given ID.")
    prev_info = patients[pid]
    updated_info = patient_update.model_dump(exclude_unset=True)
    prev_info.update(updated_info)
    prev_info["id"] = pid  
    pydantic_patient = Patient_Details(**prev_info)
    patients[pid] = pydantic_patient.model_dump(exclude=["id"])
    save_data(patients)
    return JSONResponse(status_code=200, content={"message": f"Patient {prev_info['name']} with ID {pid} has been updated successfully."})

@app.delete("/patients/delete")
async def delete_patient(pid: str = Query(..., description="Write Patient ID to delete", example="P001")):
    patients = load_data()
    if pid not in patients:
        raise HTTPException(status_code=404, detail="Patient not found with the given ID.")
    del patients[pid]
    save_data(patients)
    return JSONResponse(status_code=200, content={"message": f"Patient with ID {pid} has been deleted successfully."})