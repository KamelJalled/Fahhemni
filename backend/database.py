from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, List, Optional
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from models import Student, Progress, Problem, Section, ProblemType

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Collections
students_collection = db.students
progress_collection = db.progress
problems_collection = db.problems
sections_collection = db.sections

async def init_database():
    """Initialize database with all sections"""
    
    # Check if data already exists
    existing_section = await sections_collection.find_one({"id": "section1"})
    if existing_section:
        # Check if we need to add new sections
        existing_section5 = await sections_collection.find_one({"id": "section5"})
        if existing_section5:
            return  # All data already initialized
    
    # Section 1 problems data
    section1_problems = [
        {
            "id": "prep1",
            "section_id": "section1",
            "type": ProblemType.PREPARATION,
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
        },
        {
            "id": "explanation1",
            "section_id": "section1", 
            "type": ProblemType.EXPLANATION,
            "weight": 0,
            "question_en": "Learn Inequality Solving",
            "question_ar": "تعلم حل المتباينات",
            "answer": "",
            "answer_ar": "",
            "show_full_solution": False,
            "hide_answer": False,
            "interactive_examples": [
                {
                    "title_en": "Example 1: Addition/Subtraction",
                    "title_ar": "المثال الأول: الجمع/الطرح",
                    "problem_en": "x + 7 > 10",
                    "problem_ar": "س + ٧ > ١٠",
                    "solution_en": "Step 1: Subtract 7 from both sides\nx + 7 - 7 > 10 - 7\nStep 2: Simplify\nx > 3",
                    "solution_ar": "الخطوة ١: اطرح ٧ من الطرفين\nس + ٧ - ٧ > ١٠ - ٧\nالخطوة ٢: بسط\nس > ٣",
                    "practice_question_en": "Now try: x + 4 ≤ 9",
                    "practice_question_ar": "الآن جرب: س + ٤ ≤ ٩",
                    "practice_answer": "x ≤ 5",
                    "practice_answer_ar": "س ≤ ٥"
                },
                {
                    "title_en": "Example 2: Multiplication/Division",
                    "title_ar": "المثال الثاني: الضرب/القسمة",
                    "problem_en": "3x ≤ 15",
                    "problem_ar": "٣س ≤ ١٥",
                    "solution_en": "Step 1: Divide both sides by 3\n3x ÷ 3 ≤ 15 ÷ 3\nStep 2: Simplify\nx ≤ 5",
                    "solution_ar": "الخطوة ١: اقسم الطرفين على ٣\n٣س ÷ ٣ ≤ ١٥ ÷ ٣\nالخطوة ٢: بسط\nس ≤ ٥",
                    "practice_question_en": "Now try: 2x > 8",
                    "practice_question_ar": "الآن جرب: ٢س > ٨",
                    "practice_answer": "x > 4",
                    "practice_answer_ar": "س > ٤"
                },
                {
                    "title_en": "Example 3: Negative Coefficient",  
                    "title_ar": "المثال الثالث: المعامل السالب",
                    "problem_en": "-2x > 8",
                    "problem_ar": "-٢س > ٨",
                    "solution_en": "Step 1: Divide both sides by -2 (FLIP the inequality sign!)\n-2x ÷ (-2) < 8 ÷ (-2)\nStep 2: Simplify\nx < -4\n\nREMEMBER: When dividing by negative, flip the sign!",
                    "solution_ar": "الخطوة ١: اقسم الطرفين على -٢ (اقلب إشارة المتباينة!)\n-٢س ÷ (-٢) < ٨ ÷ (-٢)\nالخطوة ٢: بسط\nس < -٤\n\nتذكر: عند القسمة على عدد سالب، اقلب الإشارة!",
                    "practice_question_en": "Now try: -3x ≤ 12",
                    "practice_question_ar": "الآن جرب: -٣س ≤ ١٢",
                    "practice_answer": "x ≥ -4",
                    "practice_answer_ar": "س ≥ -٤"
                }
            ],
            "hints_en": [],
            "hints_ar": []
        },
        {
            "id": "practice1",
            "section_id": "section1",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "question_en": "x - 3 ≤ 8",
            "question_ar": "س - ٣ ≤ ٨",
            "answer": "x ≤ 11",
            "answer_ar": "س ≤ ١١",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Add 3 to both sides", 
                    "step_ar": "أضف ٣ للطرفين", 
                    "possible_answers": [
                        "x - 3 + 3 ≤ 8 + 3",
                        "x ≤ 8 + 3", 
                        "x ≤ 11"
                    ],
                    "possible_answers_ar": [
                        "س - ٣ + ٣ ≤ ٨ + ٣",
                        "س ≤ ٨ + ٣",
                        "س ≤ ١١"
                    ]
                },
                {
                    "step_en": "Simplify the right side", 
                    "step_ar": "بسط الطرف الأيمن",
                    "possible_answers": [
                        "x ≤ 11"
                    ],
                    "possible_answers_ar": [
                        "س ≤ ١١"
                    ]
                }
            ],
            "hints_en": [
                "What operation cancels out subtraction?",
                "Combine the numbers on the right side."
            ],
            "hints_ar": [
                "ما العملية التي تلغي الطرح؟",
                "اجمع الأرقام في الطرف الأيمن."
            ]
        },
        {
            "id": "practice2",
            "section_id": "section1",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "question_en": "4x < 20",
            "question_ar": "٤س < ٢٠",
            "answer": "x < 5",
            "answer_ar": "س < ٥",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Divide both sides by 4", 
                    "step_ar": "اقسم الطرفين على ٤",
                    "possible_answers": [
                        "4x ÷ 4 < 20 ÷ 4",
                        "4x / 4 < 20 / 4",
                        "x < 20 / 4",
                        "x < 5"
                    ],
                    "possible_answers_ar": [
                        "٤س ÷ ٤ < ٢٠ ÷ ٤",
                        "٤س / ٤ < ٢٠ / ٤",
                        "س < ٢٠ / ٤",
                        "س < ٥"
                    ]
                },
                {
                    "step_en": "Simplify the division", 
                    "step_ar": "بسط القسمة",
                    "possible_answers": [
                        "x < 5"
                    ],
                    "possible_answers_ar": [
                        "س < ٥"
                    ]
                }
            ],
            "hints_en": [
                "What operation cancels out multiplication?",
                "Calculate 20 divided by 4."
            ],
            "hints_ar": [
                "ما العملية التي تلغي الضرب؟",
                "احسب ٢٠ مقسوماً على ٤."
            ]
        },
        {
            "id": "assessment1",
            "section_id": "section1",
            "type": ProblemType.ASSESSMENT,
            "weight": 30,
            "question_en": "6x ≥ 18",
            "question_ar": "٦س ≥ ١٨",
            "answer": "x ≥ 3",
            "answer_ar": "س ≥ ٣",
            "show_full_solution": False,
            "hide_answer": True,
            "hints_en": [
                "Think about what operation will help you solve for x.",
                "You need to isolate x by using division.",
                "That's all the hints available."
            ],
            "hints_ar": [
                "فكر في العملية التي ستساعدك في حل س.",
                "تحتاج إلى عزل س باستخدام القسمة.",
                "هذه كل الإرشادات المتاحة."
            ]
        },
        {
            "id": "examprep1",
            "section_id": "section1",
            "type": ProblemType.EXAMPREP,
            "weight": 30,
            "question_en": "-2x > 8",
            "question_ar": "-٢س > ٨",
            "answer": "x < -4",
            "answer_ar": "س < -٤",
            "show_full_solution": False,
            "hide_answer": True,
            "hints_en": [
                "What happens to the inequality when you divide by a negative number?",
                "The inequality sign flips when dividing by negative numbers.",
                "That's all the hints available."
            ],
            "hints_ar": [
                "ماذا يحدث للمتباينة عندما تقسم على عدد سالب؟",
                "تنقلب إشارة المتباينة عند القسمة على الأعداد السالبة.",
                "هذه كل الإرشادات المتاحة."
            ]
        }
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
    print("Database initialized with Section 1 problems")

# Student operations
async def create_student(username: str) -> Student:
    student_data = {
        "username": username,
        "created_at": datetime.utcnow(),
        "last_login": datetime.utcnow(),
        "total_points": 0,
        "badges": []
    }
    
    # Check if student already exists
    existing = await students_collection.find_one({"username": username})
    if existing:
        # Update last login
        await students_collection.update_one(
            {"username": username},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        return Student(**existing)
    
    await students_collection.insert_one(student_data)
    return Student(**student_data)

async def get_student(username: str) -> Optional[Student]:
    student = await students_collection.find_one({"username": username})
    return Student(**student) if student else None

# Progress operations
async def get_student_progress(username: str) -> List[Progress]:
    progress_list = await progress_collection.find({"student_username": username}).to_list(None)
    return [Progress(**p) for p in progress_list]

async def update_progress(username: str, problem_id: str, progress_data: Dict) -> Progress:
    filter_query = {"student_username": username, "problem_id": problem_id}
    update_data = {
        **progress_data,
        "last_attempt": datetime.utcnow()
    }
    
    result = await progress_collection.find_one_and_update(
        filter_query,
        {"$set": update_data},
        upsert=True,
        return_document=True
    )
    
    return Progress(**result)

# Problem operations
async def get_section_problems(section_id: str) -> List[Problem]:
    problems = await problems_collection.find({"section_id": section_id}).to_list(None)
    return [Problem(**p) for p in problems]

async def get_problem(problem_id: str) -> Optional[Problem]:
    problem = await problems_collection.find_one({"id": problem_id})
    return Problem(**problem) if problem else None

# Teacher operations
async def get_all_students_stats() -> List[Dict]:
    """Get statistics for all students"""
    students = await students_collection.find().to_list(None)
    stats = []
    
    for student in students:
        username = student["username"]
        progress_list = await progress_collection.find({"student_username": username}).to_list(None)
        
        # Calculate stats
        total_problems = 6  # Section 1 has 6 problems
        completed_problems = len([p for p in progress_list if p.get("completed", False)])
        progress_percentage = (completed_problems / total_problems) * 100
        
        # Calculate weighted score
        total_score = 0
        total_weight = 0
        problems = await problems_collection.find({"section_id": "section1"}).to_list(None)
        
        for problem in problems:
            progress_item = next((p for p in progress_list if p["problem_id"] == problem["id"]), None)
            if progress_item and progress_item.get("completed", False):
                total_score += (progress_item.get("score", 0) * problem["weight"]) / 100
                total_weight += problem["weight"]
        
        weighted_score = (total_score / total_weight) * 100 if total_weight > 0 else 0
        total_attempts = sum(p.get("attempts", 0) for p in progress_list)
        
        # Create problems status
        problems_status = {}
        for problem in problems:
            progress_item = next((p for p in progress_list if p["problem_id"] == problem["id"]), None)
            problems_status[problem["id"]] = {
                "completed": progress_item.get("completed", False) if progress_item else False,
                "score": progress_item.get("score", 0) if progress_item else 0,
                "attempts": progress_item.get("attempts", 0) if progress_item else 0
            }
        
        stats.append({
            "username": username,
            "progress_percentage": progress_percentage,
            "completed_problems": completed_problems,
            "total_problems": total_problems,
            "weighted_score": weighted_score,
            "total_attempts": total_attempts,
            "last_activity": student.get("last_login"),
            "problems_status": problems_status
        })
    
    return stats