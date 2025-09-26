import logging
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

# CRITICAL: Stage access control security functions
def get_problem_type(problem_id: str) -> str:
    """Extract problem type from problem ID"""
    if 'prep' in problem_id and 'examprep' not in problem_id:
        return 'preparation'
    elif 'explanation' in problem_id:
        return 'explanation'
    elif 'practice' in problem_id:
        return 'practice'
    elif 'assessment' in problem_id:
        return 'assessment'
    elif 'examprep' in problem_id:
        return 'examprep'
    return 'unknown'

def get_section_from_problem_id(problem_id: str) -> str:
    """Extract section ID from problem ID"""
    import re
    match = re.search(r'(\d+)', problem_id)
    if match:
        section_num = match.group(1)
        return f"section{section_num}"
    return "section1"  # default

async def check_stage_access_security(username: str, problem_id: str) -> dict:
    """
    CRITICAL SECURITY: Check if student has access to requested stage
    Prevents cheating by enforcing proper learning progression
    """
    try:
        problem_type = get_problem_type(problem_id)
        section_id = get_section_from_problem_id(problem_id)
        
        # Get student's current progress
        progress_list = await get_student_progress(username)
        
        # Convert to dictionary for easier access
        progress_dict = {}
        for progress in progress_list:
            progress_dict[progress.problem_id] = {
                "completed": progress.completed,
                "score": progress.score,
                "attempts": progress.attempts
            }
        
        # SECURITY RULE 1: Lock Assessment and Exam Prep until ALL practice stages are completed
        if problem_type in ['assessment', 'examprep']:
            section_num = section_id.replace('section', '')
            
            # Define expected practice problems for each section
            if section_num == '1':
                expected_practice = ['practice1_1', 'practice1_2']
            elif section_num == '2':
                expected_practice = ['practice2_1', 'practice2_2']
            else:
                expected_practice = [f'practice{section_num}_1', f'practice{section_num}_2']
            
            # Check if all expected practice problems are completed
            incomplete_practice = []
            for practice_id in expected_practice:
                if not progress_dict.get(practice_id, {}).get("completed", False):
                    incomplete_practice.append(practice_id)
            
            if incomplete_practice:
                return {
                    "access": False,
                    "error": "practice_incomplete",
                    "message": f"You must complete all practice stages first. Incomplete: {', '.join(incomplete_practice)}",
                    "status_code": 403
                }
        
        # SECURITY RULE 2: Lock Exam Prep until Assessment is completed
        if problem_type == 'examprep':
            section_num = section_id.replace('section', '')
            assessment_id = f"assessment{section_num}"
            
            assessment_complete = progress_dict.get(assessment_id, {}).get("completed", False)
            
            if not assessment_complete:
                return {
                    "access": False,
                    "error": "assessment_incomplete", 
                    "message": f"You must complete the Assessment stage first (assessment{section_num})",
                    "status_code": 403
                }
        
        # Access granted
        return {"access": True}
        
    except Exception as e:
        # Log error but don't block access in case of system errors
        print(f"Stage access check error: {e}")
        return {"access": True}

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
    """Get student progress for all problems across all sections"""
    try:
        progress_list = await get_student_progress(username)
        
        # Convert to dictionary format expected by frontend - support all sections
        progress_dict = {}
        
        # Initialize sections 1-5 with default values
        for section_num in range(1, 6):
            section_key = f"section{section_num}"
            progress_dict[section_key] = {}
            
            # Default problems for each section
            default_problems = [
                f"prep{section_num}", 
                f"explanation{section_num}", 
                f"practice{section_num}_1", 
                f"practice{section_num}_2", 
                f"assessment{section_num}", 
                f"examprep{section_num}"
            ]
            
            # Handle legacy naming for section 1
            if section_num == 1:
                default_problems = ["prep1", "explanation1", "practice1_1", "practice1_2", "assessment1", "examprep1"]
            
            # Handle section 2 naming
            if section_num == 2:
                default_problems = ["prep2", "explanation2", "practice2_1", "practice2_2", "assessment2", "examprep2"]
            
            for problem_id in default_problems:
                progress_dict[section_key][problem_id] = {
                    "completed": False,
                    "score": 0,
                    "attempts": 0
                }
        
        # Update with actual progress
        for progress in progress_list:
            # Determine which section this problem belongs to
            problem_id = progress.problem_id
            section_num = 1  # default
            
            # Extract section number from problem ID
            import re
            match = re.search(r'(\d+)', problem_id)
            if match:
                section_num = int(match.group(1))
            
            section_key = f"section{section_num}"
            
            if section_key in progress_dict:
                progress_dict[section_key][problem_id] = {
                    "completed": progress.completed,
                    "score": progress.score,
                    "attempts": progress.attempts
                }
        
        # Calculate total points and badges (for section 1 compatibility)
        try:
            problems = await get_section_problems("section1")
            problems_dict = {p.id: {"weight": p.weight} for p in problems}
            
            total_points = calculate_total_points(progress_dict["section1"], problems_dict)
            badges = calculate_badges(progress_dict["section1"])
        except:
            total_points = 0
            badges = []
        
        return {
            "progress": progress_dict,
            "total_points": total_points,
            "badges": badges
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.post("/updateProgress")
async def update_progress_endpoint(progress_update: dict):
    """Update progress status for stage completion"""
    try:
        username = progress_update.get("username")
        section = progress_update.get("section")
        stage = progress_update.get("stage")
        status = progress_update.get("status")
        
        if not all([username, section, stage, status]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Get current progress for the stage
        current_progress = await get_student_progress(username)
        stage_progress = next(
            (p for p in current_progress if p.problem_id == stage), 
            None
        )
        
        # Update the stage as completed
        section_id = f"section{section}"
        progress_data = {
            "student_username": username,
            "section_id": section_id,
            "problem_id": stage,
            "completed": status == 'complete',
            "score": stage_progress.score if stage_progress else 100,
            "attempts": stage_progress.attempts if stage_progress else 1,
            "hints_used": stage_progress.hints_used if stage_progress else 0
        }
        
        updated_progress = await update_progress(username, stage, progress_data)
        
        return {
            "success": True,
            "message": f"Progress updated for {stage}",
            "progress": updated_progress
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.post("/students/{username}/attempt")
async def submit_attempt(username: str, attempt: ProblemAttempt):
    """Submit a problem attempt with stage access control"""
    try:
        # CRITICAL SECURITY: Check stage access before allowing attempt
        access_check = await check_stage_access_security(username, attempt.problem_id)
        if not access_check["access"]:
            raise HTTPException(
                status_code=access_check["status_code"], 
                detail={
                    "error": access_check["error"],
                    "message": access_check["message"],
                    "locked": True
                }
            )
        
        # Get the problem to check answer
        problem = await get_problem(attempt.problem_id)
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")
        
        # Get section from problem ID for dynamic section support
        section_id = get_section_from_problem_id(attempt.problem_id)
        
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
            "section_id": section_id,  # Dynamic section support
            "problem_id": attempt.problem_id,
            "completed": is_now_completed,
            "score": score if is_correct else (current_problem_progress.score if current_problem_progress else 0),
            "attempts": new_attempts,
            "hints_used": attempt.hints_used
        }
        
        updated_progress = await update_progress(username, attempt.problem_id, progress_data)
        await handle_section_completion(username, section_id, attempt.problem_id)
        
        return {
            "correct": is_correct,
            "score": score,
            "attempts": new_attempts,
            "progress": updated_progress
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Problems endpoints
@api_router.get("/problems/section/{section_id}", response_model=list[Problem])
async def get_section_problems_endpoint(section_id: str):
    """Get all problems for a section"""
    try:
        logging.warning(f"--- DEBUG: Received request for section_id: {section_id} ---")
        
        problems = await get_section_problems(section_id)
        return problems
    except Exception as e:
        # This will log the full error and send the error message back to the browser
        logging.error(f"--- ERROR in get_section_problems_endpoint: {e} ---", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Error fetching problems: {str(e)}")

@api_router.get("/problems/{problem_id}", response_model=Problem)
async def get_problem_endpoint(problem_id: str, username: str = None):
    """Get specific problem details with stage access control"""
    try:
        # CRITICAL SECURITY: Require username for protected stages (assessment, examprep)
        problem_type = get_problem_type(problem_id)
        if problem_type in ['assessment', 'examprep'] and not username:
            raise HTTPException(
                status_code=403, 
                detail={
                    "error": "authentication_required",
                    "message": "Username required to access assessment and exam prep stages",
                    "locked": True
                }
            )
        
        # CRITICAL SECURITY: Check stage access if username is provided
        if username:
            access_check = await check_stage_access_security(username, problem_id)
            if not access_check["access"]:
                raise HTTPException(
                    status_code=access_check["status_code"], 
                    detail={
                        "error": access_check["error"],
                        "message": access_check["message"],
                        "locked": True
                    }
                )
        
        problem = await get_problem(problem_id)
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")
        return problem
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
async def handle_section_completion(username: str, section_id: str, problem_id: str):
    """
    Handle the transition when a student completes a section's final exam prep
    This prevents database corruption when moving between sections
    """
    try:
        # Check if this is an examprep completion
        if problem_id.startswith('examprep'):
            current_section_num = int(section_id.replace('section', ''))
            
            # If completing any examprep, prepare for next section
            if current_section_num < 5:
                next_section = f'section{current_section_num + 1}'
                next_prep = f'prep{current_section_num + 1}'
                
                # Get student to get their ID
                student = await get_student(username)
                if not student:
                    return
                
                # Check current progress structure
                current_progress = await get_student_progress(username)
                
                # Create initial progress entry for next section's prep stage
                # This prevents the corruption issue
                next_prep_progress = {
                    "student_username": username,
                    "section_id": next_section,
                    "problem_id": next_prep,
                    "completed": False,
                    "score": 0,
                    "attempts": 0,
                    "hints_used": 0
                }
                
                # Check if next section prep already exists
                existing = next(
                    (p for p in current_progress if p.problem_id == next_prep), 
                    None
                )
                
                if not existing:
                    # Create the progress entry for next section
                    await update_progress(username, next_prep, next_prep_progress)
                    logging.info(f"Initialized {next_section} prep stage for student {username}")
                    
    except Exception as e:
        logging.error(f"Error in handle_section_completion: {e}")
        # Don't raise - just log the error to prevent breaking the flow

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
