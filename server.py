import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://your-frontend.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Read JSON credentials from environment variable
creds_json = os.getenv("GOOGLE_CREDENTIALS")
creds_dict = json.loads(creds_json)

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open sheet by name (replace "Attendance" with your sheet name)
sheet = client.open("Attendance").sheet1


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

@app.post("/students")
async def get_students(data: EnrollmentRequest):
    result = {i: students.get(i, "Not Found") for i in data.ids}
    # Save attendance in Google Sheets
    for i in data.ids:
        sheet.append_row([i, students.get(i, "Not Found")])
    return result

@app.get("/attendance")
async def get_attendance():
    records = sheet.get_all_records()
    return {"attendance": records}

@app.get("/")
async def read_root():
    return {"Hello": "World"}
