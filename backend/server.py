from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from typing import List, Dict
from datetime import datetime

# Import custom modules
from models import (
    Student, StudentCreate, Progress, ProgressUpdate, ProblemAttempt,
    Problem, Section, TeacherAuth, StudentStats, TeacherDashboard
)
from database import (
    init_database, create_student, get_student, get_student_progress,
    update_progress, get_section_problems, get_problem, get_all_students_stats
)
from utils import normalize_answer, calculate_score, calculate_badges, calculate_total_points

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app without a prefix
app = FastAPI(title="Math Tutoring API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Authentication endpoints
@api_router.post("/auth/student-login", response_model=Student)
async def student_login(student_data: StudentCreate):
    """Student login with username only"""
    try:
        student = await create_student(student_data.username)
        return student
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.post("/auth/teacher-login")
async def teacher_login(auth_data: TeacherAuth):
    """Teacher login with access code"""
    if auth_data.access_code != "teacher2024":
        raise HTTPException(status_code=401, detail="Invalid access code")
    
    return {"message": "Teacher authenticated successfully", "role": "teacher"}

@api_router.post("/auth/logout")
async def logout():
    """Logout user"""
    return {"message": "Logged out successfully"}

# Student progress endpoints
@api_router.get("/students/{username}/progress")
async def get_progress(username: str):
    """Get student progress for all problems"""
    try:
        progress_list = await get_student_progress(username)
        
        # Convert to dictionary format expected by frontend
        progress_dict = {"section1": {}}
        
        # Initialize all problems with default values
        default_problems = ["prep1", "explanation1", "practice1", "practice2", "assessment1", "examprep1"]
        for problem_id in default_problems:
            progress_dict["section1"][problem_id] = {
                "completed": False,
                "score": 0,
                "attempts": 0
            }
        
        # Update with actual progress
        for progress in progress_list:
            progress_dict["section1"][progress.problem_id] = {
                "completed": progress.completed,
                "score": progress.score,
                "attempts": progress.attempts
            }
        
        # Calculate total points and badges
        problems = await get_section_problems("section1")
        problems_dict = {p.id: {"weight": p.weight} for p in problems}
        
        total_points = calculate_total_points(progress_dict["section1"], problems_dict)
        badges = calculate_badges(progress_dict["section1"])
        
        return {
            "progress": progress_dict,
            "total_points": total_points,
            "badges": badges
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.post("/students/{username}/attempt")
async def submit_attempt(username: str, attempt: ProblemAttempt):
    """Submit a problem attempt"""
    try:
        # Get the problem to check answer
        problem = await get_problem(attempt.problem_id)
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")
        
        # Get current progress
        current_progress = await get_student_progress(username)
        current_problem_progress = next(
            (p for p in current_progress if p.problem_id == attempt.problem_id), 
            None
        )
        
        # Calculate attempts
        current_attempts = current_problem_progress.attempts if current_problem_progress else 0
        new_attempts = current_attempts + 1
        
        # Check if answer is correct
        normalized_answer = normalize_answer(attempt.answer)
        normalized_correct = normalize_answer(problem.answer)
        is_correct = normalized_answer == normalized_correct
        
        # Calculate score
        score = calculate_score(new_attempts, attempt.hints_used, is_correct)
        
        # Update progress
        progress_data = {
            "student_username": username,
            "section_id": "section1",
            "problem_id": attempt.problem_id,
            "completed": is_correct,
            "score": score if is_correct else (current_problem_progress.score if current_problem_progress else 0),
            "attempts": new_attempts,
            "hints_used": attempt.hints_used
        }
        
        updated_progress = await update_progress(username, attempt.problem_id, progress_data)
        
        return {
            "correct": is_correct,
            "score": score,
            "attempts": new_attempts,
            "progress": updated_progress
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Problems endpoints
@api_router.get("/problems/section/{section_id}", response_model=List[Problem])
async def get_section_problems_endpoint(section_id: str):
    """Get all problems for a section"""
    try:
        problems = await get_section_problems(section_id)
        return problems
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.get("/problems/{problem_id}", response_model=Problem)
async def get_problem_endpoint(problem_id: str):
    """Get specific problem details"""
    try:
        problem = await get_problem(problem_id)
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")
        return problem
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Teacher dashboard endpoints
@api_router.get("/teacher/students")
async def get_teacher_dashboard():
    """Get all student statistics for teacher dashboard"""
    try:
        students_stats = await get_all_students_stats()
        
        if not students_stats:
            return {
                "total_students": 0,
                "average_progress": 0,
                "completed_problems": 0,
                "average_score": 0,
                "students": []
            }
        
        # Calculate overall statistics
        total_students = len(students_stats)
        average_progress = sum(s["progress_percentage"] for s in students_stats) / total_students
        completed_problems = sum(s["completed_problems"] for s in students_stats)
        average_score = sum(s["weighted_score"] for s in students_stats) / total_students
        
        return {
            "total_students": total_students,
            "average_progress": round(average_progress),
            "completed_problems": completed_problems,
            "average_score": round(average_score),
            "students": students_stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "Math Tutoring API is running", "version": "1.0.0"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    pass
