# Vercel serverless function entry point
from fastapi import FastAPI, APIRouter, HTTPException
from starlette.middleware.cors import CORSMiddleware
import os
from typing import List, Dict
from datetime import datetime

# Import custom modules
from models import (
    Student, StudentCreate, Progress, ProgressUpdate, ProblemAttempt,
    Problem, Section, TeacherAuth, StudentStats, TeacherDashboard
)
from utils import normalize_answer, calculate_score, calculate_badges, calculate_total_points

# MongoDB Atlas connection for production
from motor.motor_asyncio import AsyncIOMotorClient

# Environment variables for production
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'mathtutor')

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Collections
students_collection = db.students
progress_collection = db.progress
problems_collection = db.problems
sections_collection = db.sections

# Initialize database with problems
async def init_database():
    """Initialize database with Section 1 problems"""
    
    # Check if data already exists
    existing_section = await sections_collection.find_one({"id": "section1"})
    if existing_section:
        return  # Data already initialized
    
    # Section 1 problems data (same as in database.py)
    section1_problems = [
        {
            "id": "prep1",
            "section_id": "section1",
            "type": "preparation",
            "weight": 10,
            "question_en": "x + 8 = 15",
            "question_ar": "س + ٨ = ١٥",
            "answer": "7",
            "answer_ar": "٧",
            "explanation_en": "This is a review problem. We'll solve it step by step.",
            "explanation_ar": "هذه مسألة مراجعة. سنحلها خطوة بخطوة.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Subtract 8 from both sides",
                    "step_ar": "اطرح ٨ من الطرفين", 
                    "possible_answers": [
                        "x + 8 - 8 = 15 - 8",
                        "x = 15 - 8",
                        "x = 7"
                    ],
                    "possible_answers_ar": [
                        "س + ٨ - ٨ = ١٥ - ٨",
                        "س = ١٥ - ٨", 
                        "س = ٧"
                    ]
                },
                {
                    "step_en": "Simplify both sides",
                    "step_ar": "بسط الطرفين",
                    "possible_answers": [
                        "x = 7"
                    ],
                    "possible_answers_ar": [
                        "س = ٧"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "What operation cancels out addition?",
                "Calculate 15 minus 8."
            ],
            "hints_ar": [
                "ما العملية التي تلغي الجمع؟",
                "احسب ١٥ ناقص ٨."
            ]
        }
        # Add other problems here...
    ]
    
    # Insert problems
    await problems_collection.insert_many(section1_problems)
    
    # Create section
    section1 = {
        "id": "section1",
        "title_en": "Section 1: One-Step Inequalities",
        "title_ar": "القسم الأول: المتباينات أحادية الخطوة"
    }
    
    await sections_collection.insert_one(section1)

# Create the main app
app = FastAPI(title="Math Tutoring API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic endpoints (add all your endpoints from server.py here)
@api_router.get("/")
async def root():
    return {"message": "Math Tutoring API is running", "version": "1.0.0"}

@api_router.post("/auth/student-login", response_model=Student)
async def student_login(student_data: StudentCreate):
    """Student login with username only"""
    try:
        # Create or get student
        existing = await students_collection.find_one({"username": student_data.username})
        if existing:
            await students_collection.update_one(
                {"username": student_data.username},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            return Student(**existing)
        
        student_doc = {
            "username": student_data.username,
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow(),
            "total_points": 0,
            "badges": []
        }
        
        await students_collection.insert_one(student_doc)
        return Student(**student_doc)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Include the router in the main app
app.include_router(api_router)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_database()

# Vercel handler
handler = app