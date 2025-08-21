from fastapi import FastAPI, Path, HTTPException, Query
import json
app = FastAPI(title="Doctor API", description="API to manage patient details and health information", version="1.0")

def load_data():
    with open("patients.json","r") as f:
        return json.load(f)

@app.get("/")
async def root():
    return {"message": "Welcome to the Doctor API! Use /patients to know about patient methods or refer /docs."}

@app.get("/patients")
async def instructions():
    return {
        "message": "To get information about a patient, use /patients/name/{name} or /patients/id/{pid} or /patients/view/sort?sort_by={height,weight,age,bmi}&order_by={asc,desc} => to view all patients and /sort is optional"
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


