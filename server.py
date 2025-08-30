from typing import List
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # your frontend URL
    allow_credentials=True,
    allow_methods=["*"],   # allow POST, GET, etc.
    allow_headers=["*"],   # allow headers like Content-Type
)


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
    return result

@app.get("/")
async def read_root():
    return {"Hello": "World"}