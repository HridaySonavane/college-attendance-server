from typing import List
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---------------- FASTAPI SETUP ----------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- GOOGLE SHEETS SETUP ----------------
# Define scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials (replace 'credentials.json' with your downloaded JSON file)
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

# Authorize
client = gspread.authorize(creds)

# Open the sheet by name (or use `open_by_key` if you have the sheet ID)
sheet = client.open("Attendance").sheet1  # Change "Attendance" to your Google Sheet name


# ---------------- EXISTING STUDENT DATA ----------------
students = {
    272: "Aryan Pandey",
    282: "Dhanshri Patil",
    311: "Pulkit Sharma",
    318: "Sambhav Surana",
    319: "Sameer Chouhan",
    320: "Sanskar Rai",
    321: "Sarthak Jain",
    323: "Shiom",
    325: "Somya Verma",
    332: "Vanshika Tiwari",
    339: "Yogesh Singh",
    421: "Janak Marothiya"
}

class EnrollmentRequest(BaseModel):
    ids: List[int]


# ---------------- ROUTES ----------------
@app.post("/students")
async def get_students(data: EnrollmentRequest):
    result = {i: students.get(i, "Not Found") for i in data.ids}
    return result


@app.post("/attendance")
async def mark_attendance(data: EnrollmentRequest):
    """Mark attendance in Google Sheet for given IDs"""
    for student_id in data.ids:
        name = students.get(student_id, None)
        if name:
            # Append a new row [ID, Name, "Present"]
            sheet.append_row([student_id, name, "Present"])
        else:
            sheet.append_row([student_id, "Unknown", "Not Found"])
    return {"status": "Attendance marked successfully"}


@app.get("/attendance")
async def get_attendance():
    """Fetch all attendance records from Google Sheet"""
    records = sheet.get_all_records()
    return {"attendance": records}


@app.get("/")
async def read_root():
    return {"Hello": "World"}
