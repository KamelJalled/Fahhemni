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
    update_progress, get_section_problems, get_problem, get_all_students_stats,
    students_collection, progress_collection, problems_collection, sections_collection
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
    """Student login with username and class"""
    try:
        student = await create_student(student_data.username, student_data.class_name)
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

@api_router.delete("/admin/clear-all-data")
async def clear_all_data():
    """Clear all student records and progress data"""
    try:
        # Delete all students
        await students_collection.delete_many({})
        # Delete all progress records
        await progress_collection.delete_many({})
        
        return {"message": "All student data cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing data: {str(e)}")

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
        
        # Check if answer is correct - enhanced for preparation stage
        normalized_answer = normalize_answer(attempt.answer, problem.type, problem.answer)
        normalized_correct = normalize_answer(problem.answer, problem.type, problem.answer)
        is_correct = normalized_answer == normalized_correct
        
        # Calculate score
        score = calculate_score(new_attempts, attempt.hints_used, is_correct)
        
        # Update progress - once completed, it stays completed
        was_already_completed = current_problem_progress.completed if current_problem_progress else False
        is_now_completed = was_already_completed or is_correct
        
        progress_data = {
            "student_username": username,
            "section_id": "section1",
            "problem_id": attempt.problem_id,
            "completed": is_now_completed,
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
async def get_teacher_dashboard(class_filter: str = None):
    """Get all student statistics for teacher dashboard, optionally filtered by class"""
    try:
        students_stats = await get_all_students_stats(class_filter)
        
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

@api_router.get("/teacher/dashboard")
async def get_teacher_dashboard_new(class_filter: str = None):
    """Teacher dashboard with student statistics, optionally filtered by class"""
    try:
        stats = await get_all_students_stats(class_filter)
        
        if not stats:
            return {
                "total_students": 0,
                "average_progress": 0,
                "completed_problems": 0,
                "average_score": 0,
                "students": [],
                "class_filter": class_filter
            }
        
        total_students = len(stats)
        average_progress = sum(s["progress_percentage"] for s in stats) / total_students
        total_completed = sum(s["completed_problems"] for s in stats)
        average_score = sum(s["weighted_score"] for s in stats) / total_students
        
        return {
            "total_students": total_students,
            "average_progress": round(average_progress, 1),
            "completed_problems": total_completed,
            "average_score": round(average_score, 1),
            "students": stats,
            "class_filter": class_filter
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Admin endpoints
@api_router.post("/admin/clear-test-data")
async def clear_test_data(admin_key: str = "admin123"):
    """Clear all test data - for development only"""
    if admin_key != "admin123":  # Simple admin key for demo
        raise HTTPException(status_code=403, detail="Invalid admin key")
    
    try:
        # Clear all student data
        student_result = await students_collection.delete_many({})
        
        # Clear all progress data
        progress_result = await progress_collection.delete_many({})
        
        return {
            "message": "Test data cleared successfully",
            "students_deleted": student_result.deleted_count,
            "progress_deleted": progress_result.deleted_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing data: {str(e)}")

@api_router.get("/admin/stats")
async def get_admin_stats():
    """Get admin statistics about data storage"""
    try:
        student_count = await students_collection.count_documents({})
        progress_count = await progress_collection.count_documents({})
        problem_count = await problems_collection.count_documents({})
        section_count = await sections_collection.count_documents({})
        
        return {
            "total_students": student_count,
            "total_progress_records": progress_count,
            "total_problems": problem_count,
            "total_sections": section_count,
            "database_status": "connected"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "Math Tutoring API is running", "version": "1.0.0"}

# Admin endpoint to reset database
@api_router.post("/admin/reset-db")
async def reset_database():
    """Reset and reinitialize database - for development only"""
    try:
        from database import problems_collection, sections_collection, students_collection, progress_collection
        
        # Clear all collections
        await problems_collection.delete_many({})
        await sections_collection.delete_many({})
        await students_collection.delete_many({})
        await progress_collection.delete_many({})
        
        # Reinitialize
        await init_database()
        
        return {"message": "Database reset and reinitialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Include the router in the main app
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_database()

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
    """Cleanup on shutdown"""
    pass
