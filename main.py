from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List

app = FastAPI()

class Doctor(BaseModel):
    Name: str
    Specialization: str
    email: EmailStr
    is_active: bool = True

class Patient(BaseModel):
    Name: str
    Age: int = Field(..., gt=0)
    Phone: str

doctors_db: List[dict] = []
patients_db: List[dict] = []



@app.get("/Doctors")
def get_doctors():
    return doctors_db


@app.post("/Doctors")
def create_doctor(doctor: Doctor):
    for doc in doctors_db:
        if doc["email"] == doctor.email:
            raise HTTPException(status_code=400, detail="Email already exists")

    doctor_data = doctor.dict()
    doctor_data["id"] = len(doctors_db) + 1
    doctors_db.append(doctor_data)

    return {
        "message": "Doctor created successfully",
        "data": doctor_data
    }


@app.get("/Doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    for doctor in doctors_db:
        if doctor["id"] == doctor_id:
            return doctor

    raise HTTPException(status_code=404, detail="Doctor not found")


@app.post("/Patients")
def create_patient(patient: Patient):
    patient_data = patient.dict()
    patient_data["id"] = len(patients_db) + 1
    patients_db.append(patient_data)

    return {
        "message": "Patient created successfully",
        "data": patient_data
    }


@app.get("/Patients")
def get_patients():
    return patients_db


@app.get("/Home")
def home():
    return {"message": "API is running"}