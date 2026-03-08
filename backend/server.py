from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from integrated_system import get_comprehensive_report

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientData(BaseModel):
    age: int
    gender: int  
    heartRate: float
    spo2: float
    systolic: float
    diastolic: float
    temperature: float

# --- NEW: This acts as our live cloud database ---
latest_patient_data = {
    "vitals": None,
    "report": None
}

# 1. Simulator POSTS data here
@app.post("/api/analyze")
async def analyze_vitals(data: PatientData):
    derived_map = (data.systolic + (2 * data.diastolic)) / 3
    derived_pp = data.systolic - data.diastolic
    derived_hrv = round(random.uniform(0.02, 0.10), 3) 

    patient_vitals_list = [
        data.age, data.gender, data.heartRate, data.spo2, 
        data.systolic, data.diastolic, data.temperature, 
        derived_hrv, derived_map, derived_pp
    ]

    report = get_comprehensive_report(patient_vitals_list)
    
    # Save the latest data into memory
    latest_patient_data["vitals"] = data.dict()
    latest_patient_data["report"] = report
    
    return report

# --- NEW: 2. React Dashboard GETS data from here ---
@app.get("/api/livedata")
async def get_live_data():
    return latest_patient_data