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
    
    # Section 2: Two-Step Inequalities
    section2_problems = [
        {
            "id": "prep2",
            "section_id": "section2",
            "type": ProblemType.PREPARATION,
            "weight": 10,
            "question_en": "3x + 2 < 11",
            "question_ar": "٣س + ٢ < ١١",
            "answer": "x < 3",
            "answer_ar": "س < ٣",
            "explanation_en": "This is a two-step inequality. We need to undo addition first, then division.",
            "explanation_ar": "هذه متباينة ذات خطوتين. نحتاج إلى إلغاء الجمع أولاً، ثم القسمة.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Subtract 2 from both sides",
                    "step_ar": "اطرح ٢ من الطرفين",
                    "possible_answers": [
                        "3x + 2 - 2 < 11 - 2",
                        "3x < 11 - 2",
                        "3x < 9"
                    ],
                    "possible_answers_ar": [
                        "٣س + ٢ - ٢ < ١١ - ٢",
                        "٣س < ١١ - ٢",
                        "٣س < ٩"
                    ]
                },
                {
                    "step_en": "Divide both sides by 3",
                    "step_ar": "اقسم الطرفين على ٣",
                    "possible_answers": [
                        "3x / 3 < 9 / 3",
                        "x < 9 / 3",
                        "x < 3"
                    ],
                    "possible_answers_ar": [
                        "٣س / ٣ < ٩ / ٣",
                        "س < ٩ / ٣",
                        "س < ٣"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "Start by isolating the term with x",
                "What operation cancels out +2?",
                "Then isolate x by dividing"
            ],
            "hints_ar": [
                "ابدأ بعزل الحد الذي يحتوي على س",
                "ما العملية التي تلغي +٢؟", 
                "ثم اعزل س بالقسمة"
            ]
        },
        {
            "id": "explanation2",
            "section_id": "section2",
            "type": ProblemType.EXPLANATION,
            "weight": 0,
            "question_en": "Learn Two-Step Inequalities",
            "question_ar": "تعلم المتباينات ذات الخطوتين",
            "answer": "",
            "answer_ar": "",
            "show_full_solution": False,
            "hide_answer": False,
            "interactive_examples": [
                {
                    "title_en": "Example 1: Addition then Division",
                    "title_ar": "المثال الأول: الجمع ثم القسمة",
                    "problem_en": "2x - 5 ≥ 7",
                    "problem_ar": "٢س - ٥ ≥ ٧",
                    "solution_en": "Step 1: Add 5 to both sides\n2x - 5 + 5 ≥ 7 + 5\n2x ≥ 12\nStep 2: Divide both sides by 2\n2x ÷ 2 ≥ 12 ÷ 2\nx ≥ 6",
                    "solution_ar": "الخطوة ١: أضف ٥ للطرفين\n٢س - ٥ + ٥ ≥ ٧ + ٥\n٢س ≥ ١٢\nالخطوة ٢: اقسم الطرفين على ٢\n٢س ÷ ٢ ≥ ١٢ ÷ ٢\nس ≥ ٦",
                    "practice_question_en": "Now try: 3x + 1 > 10",
                    "practice_question_ar": "الآن جرب: ٣س + ١ > ١٠",
                    "practice_answer": "x > 3",
                    "practice_answer_ar": "س > ٣"
                },
                {
                    "title_en": "Example 2: Subtraction then Division",
                    "title_ar": "المثال الثاني: الطرح ثم القسمة",
                    "problem_en": "4x + 8 ≤ 20",
                    "problem_ar": "٤س + ٨ ≤ ٢٠",
                    "solution_en": "Step 1: Subtract 8 from both sides\n4x + 8 - 8 ≤ 20 - 8\n4x ≤ 12\nStep 2: Divide both sides by 4\n4x ÷ 4 ≤ 12 ÷ 4\nx ≤ 3",
                    "solution_ar": "الخطوة ١: اطرح ٨ من الطرفين\n٤س + ٨ - ٨ ≤ ٢٠ - ٨\n٤س ≤ ١٢\nالخطوة ٢: اقسم الطرفين على ٤\n٤س ÷ ٤ ≤ ١٢ ÷ ٤\nس ≤ ٣",
                    "practice_question_en": "Now try: 5x - 3 < 17",
                    "practice_question_ar": "الآن جرب: ٥س - ٣ < ١٧",
                    "practice_answer": "x < 4",
                    "practice_answer_ar": "س < ٤"
                }
            ],
            "hints_en": [],
            "hints_ar": []
        },
        {
            "id": "practice2_1",
            "section_id": "section2",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "question_en": "4x + 3 ≤ 15",
            "question_ar": "٤س + ٣ ≤ ١٥",
            "answer": "x ≤ 3",
            "answer_ar": "س ≤ ٣",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Subtract 3 from both sides",
                    "step_ar": "اطرح ٣ من الطرفين",
                    "possible_answers": [
                        "4x + 3 - 3 ≤ 15 - 3",
                        "4x ≤ 15 - 3",
                        "4x ≤ 12"
                    ],
                    "possible_answers_ar": [
                        "٤س + ٣ - ٣ ≤ ١٥ - ٣",
                        "٤س ≤ ١٥ - ٣",
                        "٤س ≤ ١٢"
                    ]
                },
                {
                    "step_en": "Divide both sides by 4",
                    "step_ar": "اقسم الطرفين على ٤",
                    "possible_answers": [
                        "4x / 4 ≤ 12 / 4",
                        "x ≤ 12 / 4",
                        "x ≤ 3"
                    ],
                    "possible_answers_ar": [
                        "٤س / ٤ ≤ ١٢ / ٤",
                        "س ≤ ١٢ / ٤",
                        "س ≤ ٣"
                    ]
                }
            ],
            "hints_en": [
                "Start by removing the constant term",
                "What do you add or subtract to cancel +3?",
                "Then isolate x by dividing by the coefficient"
            ],
            "hints_ar": [
                "ابدأ بإزالة الحد الثابت",
                "ماذا تجمع أو تطرح لتلغي +٣؟",
                "ثم اعزل س بالقسمة على المعامل"
            ]
        },
        {
            "id": "practice2_2",
            "section_id": "section2",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "question_en": "5x - 2 > 18",
            "question_ar": "٥س - ٢ > ١٨",
            "answer": "x > 4",
            "answer_ar": "س > ٤",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Add 2 to both sides",
                    "step_ar": "أضف ٢ للطرفين",
                    "possible_answers": [
                        "5x - 2 + 2 > 18 + 2",
                        "5x > 18 + 2",
                        "5x > 20"
                    ],
                    "possible_answers_ar": [
                        "٥س - ٢ + ٢ > ١٨ + ٢",
                        "٥س > ١٨ + ٢",
                        "٥س > ٢٠"
                    ]
                },
                {
                    "step_en": "Divide both sides by 5",
                    "step_ar": "اقسم الطرفين على ٥",
                    "possible_answers": [
                        "5x / 5 > 20 / 5",
                        "x > 20 / 5",
                        "x > 4"
                    ],
                    "possible_answers_ar": [
                        "٥س / ٥ > ٢٠ / ٥",
                        "س > ٢٠ / ٥",
                        "س > ٤"
                    ]
                }
            ],
            "hints_en": [
                "What operation cancels out -2?",
                "Calculate 18 + 2",
                "Then divide both sides by 5"
            ],
            "hints_ar": [
                "ما العملية التي تلغي -٢؟",
                "احسب ١٨ + ٢",
                "ثم اقسم الطرفين على ٥"
            ]
        },
        {
            "id": "assessment2",
            "section_id": "section2",
            "type": ProblemType.ASSESSMENT,
            "weight": 30,
            "question_en": "3x + 7 ≥ 22",
            "question_ar": "٣س + ٧ ≥ ٢٢",
            "answer": "x ≥ 5",
            "answer_ar": "س ≥ ٥",
            "show_full_solution": False,
            "hide_answer": True,
            "hints_en": [
                "This is a two-step inequality. Start by isolating the x term.",
                "First subtract, then divide.",
                "Remember to keep the inequality sign in the same direction."
            ],
            "hints_ar": [
                "هذه متباينة ذات خطوتين. ابدأ بعزل حد س.",
                "اطرح أولاً، ثم اقسم.",
                "تذكر أن تحافظ على اتجاه إشارة المتباينة."
            ]
        },
        {
            "id": "examprep2",
            "section_id": "section2",
            "type": ProblemType.EXAMPREP,
            "weight": 30,
            "question_en": "6x - 4 < 20",
            "question_ar": "٦س - ٤ < ٢٠",
            "answer": "x < 4",
            "answer_ar": "س < ٤",
            "show_full_solution": False,
            "hide_answer": True,
            "hints_en": [
                "Follow the two-step process: first deal with the constant term.",
                "Add 4 to both sides, then divide by 6.",
                "Check your final answer by substituting back."
            ],
            "hints_ar": [
                "اتبع العملية ذات الخطوتين: تعامل مع الحد الثابت أولاً.",
                "أضف ٤ للطرفين، ثم اقسم على ٦.",
                "تحقق من إجابتك النهائية بالتعويض مرة أخرى."
            ]
        }
    ]
    
    await problems_collection.insert_many(section2_problems)
    
    section2 = {
        "id": "section2",
        "title_en": "Section 2: Two-Step Inequalities",
        "title_ar": "القسم الثاني: المتباينات ذات الخطوتين"
    }
    await sections_collection.insert_one(section2)
    
    print("Database initialized with all sections")

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