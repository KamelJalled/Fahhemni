#!/usr/bin/env python3
"""
Complete Math Tutoring App Database Migration Script
This script populates MongoDB with ALL sections (1-5) with updated content.

Usage:
1. Install dependencies: pip install motor python-dotenv
2. Set your MongoDB connection string in MONGO_URL environment variable
3. Run: python complete_database_migration.py

OR set the connection string directly in the script below.
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os

# CONFIGURATION - Update these values for your production database
MONGO_URL = "mongodb+srv://kamalaljallad_db_user:<db_password>@cluster0.dip2jyt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Replace with your production MongoDB URL
DB_NAME = "mathtutor"           # Replace with your database name

# You can also use environment variables instead:
# MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
# DB_NAME = os.environ.get('DB_NAME', 'math_tutoring_app')

async def migrate_database():
    """Complete database migration with all 5 sections"""
    
    print("🚀 Starting complete database migration...")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Collections
    students_collection = db.students
    progress_collection = db.progress
    problems_collection = db.problems
    sections_collection = db.sections
    
    print(f"📡 Connected to database: {DB_NAME}")
    
    # Clear existing data (optional - remove these lines if you want to keep existing data)
    print("🗑️ Clearing existing problems and sections...")
    await problems_collection.delete_many({})
    await sections_collection.delete_many({})
    
    # Section definitions
    sections_data = [
        {
            "id": "section1",
            "title_en": "Addition/Subtraction Inequalities",
            "title_ar": "متباينات الجمع والطرح",
            "description_en": "Learn to solve inequalities involving addition and subtraction operations",
            "description_ar": "تعلم حل المتباينات التي تتضمن عمليات الجمع والطرح",
            "order": 1
        },
        {
            "id": "section2", 
            "title_en": "Multiplication/Division Inequalities",
            "title_ar": "متباينات الضرب والقسمة",
            "description_en": "Master inequalities with multiplication and division, including sign flipping",
            "description_ar": "اتقن المتباينات مع الضرب والقسمة، بما في ذلك قلب الإشارة",
            "order": 2
        },
        {
            "id": "section3",
            "title_en": "Multi-Step Inequalities", 
            "title_ar": "المتباينات متعددة الخطوات",
            "description_en": "Solve complex inequalities requiring multiple operations",
            "description_ar": "حل المتباينات المعقدة التي تتطلب عمليات متعددة",
            "order": 3
        },
        {
            "id": "section4",
            "title_en": "Compound Inequalities",
            "title_ar": "المتباينات المركبة", 
            "description_en": "Work with AND and OR compound inequalities",
            "description_ar": "العمل مع المتباينات المركبة و و أو",
            "order": 4
        },
        {
            "id": "section5",
            "title_en": "Absolute Value Inequalities",
            "title_ar": "متباينات القيمة المطلقة",
            "description_en": "Solve inequalities involving absolute values",
            "description_ar": "حل المتباينات التي تتضمن القيم المطلقة",
            "order": 5
        }
    ]
    
    # Insert sections
    print("📚 Inserting sections...")
    await sections_collection.insert_many(sections_data)
    
    # SECTION 1 PROBLEMS
    section1_problems = [
        {
            "id": "prep1",
            "section_id": "section1",
            "type": "preparation",
            "weight": 10,
            "question_en": "x - 5 > 10",
            "question_ar": "س - ٥ > ١٠",
            "answer": "x > 15",
            "answer_ar": "س > ١٥",
            "explanation_en": "This is a review problem for solving inequalities.",
            "explanation_ar": "هذه مسألة مراجعة لحل المتباينات.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Add 5 to both sides",
                    "step_ar": "أضف ٥ إلى الطرفين", 
                    "possible_answers": [
                        "x - 5 + 5 > 10 + 5",
                        "x > 10 + 5",
                        "x > 15"
                    ],
                    "possible_answers_ar": [
                        "س - ٥ + ٥ > ١٠ + ٥",
                        "س > ١٠ + ٥", 
                        "س > ١٥"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "What operation cancels out subtraction?",
                "Add 5 to both sides to isolate x."
            ],
            "hints_ar": [
                "ما العملية التي تلغي الطرح؟",
                "أضف ٥ إلى الطرفين لعزل س."
            ]
        },
        {
            "id": "explanation1",
            "section_id": "section1", 
            "type": "explanation",
            "weight": 0,
            "question_en": "Learn Addition/Subtraction Inequalities",
            "question_ar": "تعلم متباينات الجمع والطرح",
            "answer": "",
            "answer_ar": "",
            "show_full_solution": False,
            "hide_answer": False,
            "explanation_en": "Learn to solve inequalities involving addition and subtraction",
            "explanation_ar": "تعلم حل المتباينات التي تتضمن الجمع والطرح",
            "interactive_examples": [
                {
                    "title_en": "Level 1: Simple (Example 1A - System Solved)",
                    "title_ar": "المستوى ١: بسيط (المثال ١أ - حل النظام)",
                    "problem_en": "x - 8 > 2",
                    "problem_ar": "س - ٨ > ٢",
                    "solution_en": "Original inequality: x - 8 > 2\\n\\nStep 1: x - 8 + 8 > 2 + 8\\nStep 2: x > 10",
                    "solution_ar": "المتباينة الأصلية: س - ٨ > ٢\\n\\nالخطوة ١: س - ٨ + ٨ > ٢ + ٨\\nالخطوة ٢: س > ١٠"
                },
                {
                    "title_en": "Level 2: Addition (Example 1B)",
                    "title_ar": "المستوى ٢: الجمع (المثال ١ب)",
                    "problem_en": "y + 7 ≤ 12",
                    "problem_ar": "ص + ٧ ≤ ١٢",
                    "solution_en": "Original inequality: y + 7 ≤ 12\\n\\nStep 1: y + 7 - 7 ≤ 12 - 7\\nStep 2: y ≤ 5",
                    "solution_ar": "المتباينة الأصلية: ص + ٧ ≤ ١٢\\n\\nالخطوة ١: ص + ٧ - ٧ ≤ ١٢ - ٧\\nالخطوة ٢: ص ≤ ٥"
                }
            ],
            "hints_en": [
                "Remember: Addition and subtraction don't change the inequality sign",
                "Think about what operation undoes the operation in the problem"
            ],
            "hints_ar": [
                "تذكر: الجمع والطرح لا يغيران إشارة المتباينة",
                "فكر في العملية التي تلغي العملية الموجودة في المسألة"
            ]
        },
        {
            "id": "practice1",
            "section_id": "section1",
            "type": "practice",
            "weight": 30,
            "question_en": "Solve: m + 12 ≤ 25",
            "question_ar": "حل: م + ١٢ ≤ ٢٥",
            "answer": "m <= 13",
            "answer_ar": "م ≤ ١٣",
            "explanation_en": "Practice solving inequalities with addition and subtraction.",
            "explanation_ar": "تدرب على حل المتباينات مع الجمع والطرح.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Subtract 12 from both sides",
                    "step_ar": "اطرح ١٢ من كلا الطرفين",
                    "possible_answers": [
                        "m + 12 - 12 <= 25 - 12",
                        "m <= 25 - 12",
                        "m <= 13"
                    ],
                    "possible_answers_ar": [
                        "م + ١٢ - ١٢ ≤ ٢٥ - ١٢",
                        "م ≤ ٢٥ - ١٢",
                        "م ≤ ١٣"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "What operation cancels out +12?",
                "Subtract 12 from both sides"
            ],
            "hints_ar": [
                "ما العملية التي تلغي +١٢؟",
                "اطرح ١٢ من كلا الطرفين"
            ]
        },
        {
            "id": "assessment1", 
            "section_id": "section1",
            "type": "assessment",
            "weight": 40,
            "question_en": "Solve: k - 7 > 8",
            "question_ar": "حل: ك - ٧ > ٨",
            "answer": "k > 15",
            "answer_ar": "ك > ١٥",
            "explanation_en": "Assessment for addition/subtraction inequalities.",
            "explanation_ar": "تقييم متباينات الجمع والطرح.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Add 7 to both sides",
                    "step_ar": "أضف ٧ إلى كلا الطرفين",
                    "possible_answers": [
                        "k - 7 + 7 > 8 + 7",
                        "k > 8 + 7", 
                        "k > 15"
                    ],
                    "possible_answers_ar": [
                        "ك - ٧ + ٧ > ٨ + ٧",
                        "ك > ٨ + ٧",
                        "ك > ١٥"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "What operation cancels subtraction?",
                "Add 7 to both sides to isolate k"
            ],
            "hints_ar": [
                "ما العملية التي تلغي الطرح؟",
                "أضف ٧ إلى كلا الطرفين لعزل ك"
            ]
        },
        {
            "id": "examprep1",
            "section_id": "section1", 
            "type": "examprep",
            "weight": 20,
            "question_en": "Final Review: Solve n + 9 < 20",
            "question_ar": "المراجعة النهائية: حل ن + ٩ < ٢٠",
            "answer": "n < 11",
            "answer_ar": "ن < ١١",
            "explanation_en": "Comprehensive review of addition/subtraction inequalities.",
            "explanation_ar": "مراجعة شاملة لمتباينات الجمع والطرح.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Subtract 9 from both sides",
                    "step_ar": "اطرح ٩ من كلا الطرفين",
                    "possible_answers": [
                        "n + 9 - 9 < 20 - 9",
                        "n < 20 - 9",
                        "n < 11"
                    ],
                    "possible_answers_ar": [
                        "ن + ٩ - ٩ < ٢٠ - ٩",
                        "ن < ٢٠ - ٩",
                        "ن < ١١"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "Remember the properties of inequalities with addition/subtraction",
                "Subtract 9 from both sides"
            ],
            "hints_ar": [
                "تذكر خصائص المتباينات مع الجمع/الطرح",
                "اطرح ٩ من كلا الطرفين"
            ]
        }
    ]
    
    # SECTION 2 PROBLEMS 
    section2_problems = [
        {
            "id": "prep2",
            "section_id": "section2",
            "type": "preparation",
            "weight": 10,
            "question_en": "Solve: 3x > 18",
            "question_ar": "حل: ٣س > ١٨",
            "answer": "x > 6",
            "answer_ar": "س > ٦",
            "explanation_en": "This is a review problem for multiplication inequalities.",
            "explanation_ar": "هذه مسألة مراجعة لمتباينات الضرب.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Divide both sides by 3",
                    "step_ar": "اقسم كلا الطرفين على ٣",
                    "possible_answers": [
                        "3x / 3 > 18 / 3",
                        "x > 18 / 3",
                        "x > 6"
                    ],
                    "possible_answers_ar": [
                        "٣س / ٣ > ١٨ / ٣",
                        "س > ١٨ / ٣",
                        "س > ٦"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "When dividing by a positive number, keep the same inequality sign",
                "Divide both sides by 3"
            ],
            "hints_ar": [
                "عند القسمة على عدد موجب، احتفظ بنفس إشارة المتباينة",
                "اقسم كلا الطرفين على ٣"
            ]
        },
        {
            "id": "explanation2",
            "section_id": "section2",
            "type": "explanation",
            "weight": 0,
            "question_en": "Learn Multiplication/Division Inequalities",
            "question_ar": "تعلم متباينات الضرب والقسمة",
            "answer": "",
            "answer_ar": "",
            "show_full_solution": False,
            "hide_answer": False,
            "explanation_en": "Master inequalities with multiplication and division, including when to flip the sign",
            "explanation_ar": "اتقن المتباينات مع الضرب والقسمة، بما في ذلك متى تقلب الإشارة",
            "interactive_examples": [
                {
                    "title_en": "Level 1: Positive Coefficient",
                    "title_ar": "المستوى ١: المعامل الموجب",
                    "problem_en": "4x > 20",
                    "problem_ar": "٤س > ٢٠",
                    "solution_en": "Original inequality: 4x > 20\\n\\nStep 1: Divide by 4 (positive)\\nStep 2: 4x/4 > 20/4\\nStep 3: x > 5",
                    "solution_ar": "المتباينة الأصلية: ٤س > ٢٠\\n\\nالخطوة ١: اقسم على ٤ (موجب)\\nالخطوة ٢: ٤س/٤ > ٢٠/٤\\nالخطوة ٣: س > ٥"
                },
                {
                    "title_en": "Level 2: Negative Coefficient - FLIP THE SIGN!",
                    "title_ar": "المستوى ٢: المعامل السالب - اقلب الإشارة!",
                    "problem_en": "-2y < 10",
                    "problem_ar": "-٢ص < ١٠",
                    "solution_en": "Original inequality: -2y < 10\\n\\nStep 1: Divide by -2 (negative) - FLIP SIGN!\\nStep 2: -2y/-2 > 10/-2\\nStep 3: y > -5",
                    "solution_ar": "المتباينة الأصلية: -٢ص < ١٠\\n\\nالخطوة ١: اقسم على -٢ (سالب) - اقلب الإشارة!\\nالخطوة ٢: -٢ص/-٢ > ١٠/-٢\\nالخطوة ٣: ص > -٥"
                }
            ],
            "hints_en": [
                "RULE: When multiplying/dividing by negative, FLIP the inequality sign!",
                "Positive coefficient: keep sign. Negative coefficient: flip sign."
            ],
            "hints_ar": [
                "القاعدة: عند الضرب/القسمة على سالب، اقلب إشارة المتباينة!",
                "المعامل الموجب: احتفظ بالإشارة. المعامل السالب: اقلب الإشارة."
            ]
        },
        {
            "id": "practice2",
            "section_id": "section2",
            "type": "practice", 
            "weight": 30,
            "question_en": "Solve: -3k ≥ 15",
            "question_ar": "حل: -٣ك ≥ ١٥",
            "answer": "k <= -5",
            "answer_ar": "ك ≤ -٥",
            "explanation_en": "Practice with negative coefficients - remember to flip the sign!",
            "explanation_ar": "تدرب مع المعاملات السالبة - تذكر قلب الإشارة!",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Divide both sides by -3 (flip sign!)",
                    "step_ar": "اقسم كلا الطرفين على -٣ (اقلب الإشارة!)",
                    "possible_answers": [
                        "-3k / -3 <= 15 / -3",
                        "k <= 15 / -3",
                        "k <= -5"
                    ],
                    "possible_answers_ar": [
                        "-٣ك / -٣ ≤ ١٥ / -٣",
                        "ك ≤ ١٥ / -٣",
                        "ك ≤ -٥"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "You're dividing by a NEGATIVE number (-3)",
                "Remember to FLIP the inequality sign when dividing by negative!"
            ],
            "hints_ar": [
                "أنت تقسم على عدد سالب (-٣)",
                "تذكر قلب إشارة المتباينة عند القسمة على سالب!"
            ]
        },
        {
            "id": "assessment2",
            "section_id": "section2", 
            "type": "assessment",
            "weight": 40,
            "question_en": "Solve: -6m < 24",
            "question_ar": "حل: -٦م < ٢٤",
            "answer": "m > -4", 
            "answer_ar": "م > -٤",
            "explanation_en": "Assessment of multiplication/division inequalities with sign flipping.",
            "explanation_ar": "تقييم متباينات الضرب/القسمة مع قلب الإشارة.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Divide both sides by -6 (flip sign!)",
                    "step_ar": "اقسم كلا الطرفين على -٦ (اقلب الإشارة!)",
                    "possible_answers": [
                        "-6m / -6 > 24 / -6",
                        "m > 24 / -6",
                        "m > -4"
                    ],
                    "possible_answers_ar": [
                        "-٦م / -٦ > ٢٤ / -٦",
                        "م > ٢٤ / -٦", 
                        "م > -٤"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "What happens to the inequality sign when dividing by negative?",
                "Divide by -6 and flip the sign from < to >"
            ],
            "hints_ar": [
                "ماذا يحدث لإشارة المتباينة عند القسمة على سالب؟",
                "اقسم على -٦ واقلب الإشارة من < إلى >"
            ]
        },
        {
            "id": "examprep2",
            "section_id": "section2",
            "type": "examprep",
            "weight": 20,
            "question_en": "Final Review: Solve 5p ≤ -25",
            "question_ar": "المراجعة النهائية: حل ٥ع ≤ -٢٥",
            "answer": "p <= -5",
            "answer_ar": "ع ≤ -٥",
            "explanation_en": "Comprehensive review of multiplication/division inequalities.",
            "explanation_ar": "مراجعة شاملة لمتباينات الضرب/القسمة.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Divide both sides by 5 (positive - keep sign)",
                    "step_ar": "اقسم كلا الطرفين على ٥ (موجب - احتفظ بالإشارة)",
                    "possible_answers": [
                        "5p / 5 <= -25 / 5",
                        "p <= -25 / 5",
                        "p <= -5"
                    ],
                    "possible_answers_ar": [
                        "٥ع / ٥ ≤ -٢٥ / ٥",
                        "ع ≤ -٢٥ / ٥",
                        "ع ≤ -٥"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "Is 5 positive or negative? Do you need to flip the sign?",
                "Divide by positive 5 - no need to flip the sign"
            ],
            "hints_ar": [
                "هل ٥ موجب أم سالب؟ هل تحتاج لقلب الإشارة؟",
                "اقسم على ٥ الموجب - لا حاجة لقلب الإشارة"
            ]
        }
    ]
    
    # SECTION 3 PROBLEMS
    section3_problems = [
        {
            "id": "prep3",
            "section_id": "section3",
            "type": "preparation",
            "weight": 10,
            "question_en": "Solve the inequality: 2x + 5 > 15",
            "question_ar": "حل المتباينة: ٢س + ٥ > ١٥",
            "answer": "x > 5",
            "answer_ar": "س > ٥",
            "explanation_en": "This is a review problem for solving multi-step inequalities.",
            "explanation_ar": "هذه مسألة مراجعة لحل المتباينات متعددة الخطوات.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Subtract 5 from both sides",
                    "step_ar": "الخطوة ١: اطرح ٥ من كلا الطرفين",
                    "possible_answers": [
                        "2x + 5 - 5 > 15 - 5",
                        "2x > 15 - 5",
                        "2x > 10"
                    ],
                    "possible_answers_ar": [
                        "٢س + ٥ - ٥ > ١٥ - ٥",
                        "٢س > ١٥ - ٥",
                        "٢س > ١٠"
                    ]
                },
                {
                    "step_en": "Step 2: Divide by 2",
                    "step_ar": "الخطوة ٢: اقسم على ٢",
                    "possible_answers": [
                        "2x / 2 > 10 / 2",
                        "x > 10 / 2",
                        "x > 5"
                    ],
                    "possible_answers_ar": [
                        "٢س / ٢ > ١٠ / ٢",
                        "س > ١٠ / ٢",
                        "س > ٥"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "What operation cancels +5?",
                "Subtract 5 first, then divide by 2"
            ],
            "hints_ar": [
                "ما العملية التي تلغي +٥؟",
                "اطرح ٥ أولاً، ثم اقسم على ٢"
            ]
        },
        {
            "id": "explanation3",
            "section_id": "section3",
            "type": "explanation",
            "weight": 0,
            "question_en": "Learn Multi-Step Inequalities",
            "question_ar": "تعلم المتباينات متعددة الخطوات",
            "answer": "",
            "answer_ar": "",
            "show_full_solution": False,
            "hide_answer": False,
            "explanation_en": "Learn to solve inequalities that require multiple operations in sequence",
            "explanation_ar": "تعلم حل المتباينات التي تتطلب عدة عمليات متتالية",
            "interactive_examples": [
                {
                    "title_en": "Level 1: Addition then Division",
                    "title_ar": "المستوى ١: جمع ثم قسمة",
                    "problem_en": "3y - 4 ≥ 8",
                    "problem_ar": "٣ص - ٤ ≥ ٨",
                    "solution_en": "Original inequality: 3y - 4 ≥ 8\\n\\nStep 1: Add 4 to both sides\\n3y - 4 + 4 ≥ 8 + 4\\n3y ≥ 12\\n\\nStep 2: Divide by 3\\n3y/3 ≥ 12/3\\ny ≥ 4",
                    "solution_ar": "المتباينة الأصلية: ٣ص - ٤ ≥ ٨\\n\\nالخطوة ١: أضف ٤ إلى الطرفين\\n٣ص - ٤ + ٤ ≥ ٨ + ٤\\n٣ص ≥ ١٢\\n\\nالخطوة ٢: اقسم على ٣\\n٣ص/٣ ≥ ١٢/٣\\nص ≥ ٤"
                },
                {
                    "title_en": "Level 2: Distributive Property",
                    "title_ar": "المستوى ٢: خاصية التوزيع",
                    "problem_en": "2(x + 3) < 14",
                    "problem_ar": "٢(س + ٣) < ١٤",
                    "solution_en": "Original inequality: 2(x + 3) < 14\\n\\nStep 1: Distribute 2\\n2x + 6 < 14\\n\\nStep 2: Subtract 6\\n2x + 6 - 6 < 14 - 6\\n2x < 8\\n\\nStep 3: Divide by 2\\n2x/2 < 8/2\\nx < 4",
                    "solution_ar": "المتباينة الأصلية: ٢(س + ٣) < ١٤\\n\\nالخطوة ١: وزع ٢\\n٢س + ٦ < ١٤\\n\\nالخطوة ٢: اطرح ٦\\n٢س + ٦ - ٦ < ١٤ - ٦\\n٢س < ٨\\n\\nالخطوة ٣: اقسم على ٢\\n٢س/٢ < ٨/٢\\nس < ٤"
                }
            ],
            "hints_en": [
                "Follow the order of operations in reverse: undo addition/subtraction first, then multiplication/division",
                "Remember: when dividing by negative, flip the inequality sign!"
            ],
            "hints_ar": [
                "اتبع ترتيب العمليات بالعكس: ألغِ الجمع/الطرح أولاً، ثم الضرب/القسمة",
                "تذكر: عند القسمة على سالب، اقلب إشارة المتباينة!"
            ]
        },
        {
            "id": "practice3",
            "section_id": "section3",
            "type": "practice",
            "weight": 30,
            "question_en": "Solve: -2m + 7 ≤ 15",
            "question_ar": "حل: -٢م + ٧ ≤ ١٥",
            "answer": "m >= -4",
            "answer_ar": "م ≥ -٤",
            "explanation_en": "Practice multi-step inequalities with negative coefficients.",
            "explanation_ar": "تدرب على المتباينات متعددة الخطوات مع المعاملات السالبة.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Subtract 7 from both sides",
                    "step_ar": "الخطوة ١: اطرح ٧ من كلا الطرفين",
                    "possible_answers": [
                        "-2m + 7 - 7 <= 15 - 7",
                        "-2m <= 15 - 7",
                        "-2m <= 8"
                    ],
                    "possible_answers_ar": [
                        "-٢م + ٧ - ٧ ≤ ١٥ - ٧",
                        "-٢م ≤ ١٥ - ٧",
                        "-٢م ≤ ٨"
                    ]
                },
                {
                    "step_en": "Step 2: Divide by -2 (flip sign!)",
                    "step_ar": "الخطوة ٢: اقسم على -٢ (اقلب الإشارة!)",
                    "possible_answers": [
                        "-2m / -2 >= 8 / -2",
                        "m >= 8 / -2",
                        "m >= -4"
                    ],
                    "possible_answers_ar": [
                        "-٢م / -٢ ≥ ٨ / -٢",
                        "م ≥ ٨ / -٢",
                        "م ≥ -٤"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "First get all terms with m on one side",
                "Remember to flip the sign when dividing by -2!"
            ],
            "hints_ar": [
                "أولاً اجعل جميع الحدود التي تحتوي على م في طرف واحد",
                "تذكر قلب الإشارة عند القسمة على -٢!"
            ]
        },
        {
            "id": "practice_word3",
            "section_id": "section3",
            "type": "practice_word",
            "weight": 30,
            "question_en": "Sara has $250 and wants to buy books that cost $18 each. If she needs to keep at least $100 for other expenses, what is the maximum number of books she can buy?",
            "question_ar": "لدى سارة ٢٥٠ ريالاً وتريد شراء كتب تكلف ١٨ ريالاً للكتاب الواحد. إذا كانت بحاجة للاحتفاظ بما لا يقل عن ١٠٠ ريال للمصاريف الأخرى، فما هو أقصى عدد من الكتب يمكنها شراؤه؟",
            "answer": "k <= 8",
            "answer_ar": "ك ≤ ٨",
            "explanation_en": "Real-world application of multi-step inequalities.",
            "explanation_ar": "تطبيق من الواقع للمتباينات متعددة الخطوات.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Set up inequality (Money left ≥ 100)",
                    "step_ar": "الخطوة ١: ضع المتباينة (المال المتبقي ≥ ١٠٠)",
                    "possible_answers": [
                        "250 - 18k >= 100",
                        "250 - 18k ≥ 100"
                    ],
                    "possible_answers_ar": [
                        "٢٥٠ - ١٨ك ≥ ١٠٠"
                    ]
                },
                {
                    "step_en": "Step 2: Subtract 250 from both sides",
                    "step_ar": "الخطوة ٢: اطرح ٢٥٠ من كلا الطرفين",
                    "possible_answers": [
                        "250 - 18k - 250 >= 100 - 250",
                        "-18k >= 100 - 250",
                        "-18k >= -150"
                    ],
                    "possible_answers_ar": [
                        "٢٥٠ - ١٨ك - ٢٥٠ ≥ ١٠٠ - ٢٥٠",
                        "-١٨ك ≥ ١٠٠ - ٢٥٠",
                        "-١٨ك ≥ -١٥٠"
                    ]
                },
                {
                    "step_en": "Step 3: Divide by -18 (flip sign!)",
                    "step_ar": "الخطوة ٣: اقسم على -١٨ (اقلب الإشارة!)",
                    "possible_answers": [
                        "-18k / -18 <= -150 / -18",
                        "k <= -150 / -18",
                        "k <= 8.33",
                        "k <= 8"
                    ],
                    "possible_answers_ar": [
                        "-١٨ك / -١٨ ≤ -١٥٠ / -١٨",
                        "ك ≤ -١٥٠ / -١٨",
                        "ك ≤ ٨.٣٣",
                        "ك ≤ ٨"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "Let k = number of books. Money left = 250 - 18k",
                "She needs at least $100 left, so: 250 - 18k ≥ 100",
                "Remember to flip the sign when dividing by negative!"
            ],
            "hints_ar": [
                "دع ك = عدد الكتب. المال المتبقي = ٢٥٠ - ١٨ك",
                "تحتاج على الأقل ١٠٠ ريال متبقي، إذاً: ٢٥٠ - ١٨ك ≥ ١٠٠",
                "تذكر قلب الإشارة عند القسمة على سالب!"
            ]
        },
        {
            "id": "assessment3",
            "section_id": "section3",
            "type": "assessment",
            "weight": 40,
            "question_en": "Solve: 3(2x - 1) + 7 > 22",
            "question_ar": "حل: ٣(٢س - ١) + ٧ > ٢٢",
            "answer": "x > 3",
            "answer_ar": "س > ٣",
            "explanation_en": "Assessment of multi-step inequalities with distributive property.",
            "explanation_ar": "تقييم المتباينات متعددة الخطوات مع خاصية التوزيع.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Distribute 3",
                    "step_ar": "الخطوة ١: وزع ٣",
                    "possible_answers": [
                        "3(2x - 1) + 7 > 22",
                        "6x - 3 + 7 > 22",
                        "6x + 4 > 22"
                    ],
                    "possible_answers_ar": [
                        "٣(٢س - ١) + ٧ > ٢٢",
                        "٦س - ٣ + ٧ > ٢٢",
                        "٦س + ٤ > ٢٢"
                    ]
                },
                {
                    "step_en": "Step 2: Subtract 4 from both sides",
                    "step_ar": "الخطوة ٢: اطرح ٤ من كلا الطرفين",
                    "possible_answers": [
                        "6x + 4 - 4 > 22 - 4",
                        "6x > 22 - 4",
                        "6x > 18"
                    ],
                    "possible_answers_ar": [
                        "٦س + ٤ - ٤ > ٢٢ - ٤",
                        "٦س > ٢٢ - ٤",
                        "٦س > ١٨"
                    ]
                },
                {
                    "step_en": "Step 3: Divide by 6",
                    "step_ar": "الخطوة ٣: اقسم على ٦",
                    "possible_answers": [
                        "6x / 6 > 18 / 6",
                        "x > 18 / 6",
                        "x > 3"
                    ],
                    "possible_answers_ar": [
                        "٦س / ٦ > ١٨ / ٦",
                        "س > ١٨ / ٦",
                        "س > ٣"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "Start by distributing 3 to both terms inside parentheses",
                "Then combine like terms before isolating x"
            ],
            "hints_ar": [
                "ابدأ بتوزيع ٣ على كلا الحدين داخل الأقواس",
                "ثم اجمع الحدود المتشابهة قبل عزل س"
            ]
        },
        {
            "id": "examprep3",
            "section_id": "section3",
            "type": "examprep",
            "weight": 20,
            "question_en": "Final Review: Solve -4(x + 2) ≥ 12",
            "question_ar": "المراجعة النهائية: حل -٤(س + ٢) ≥ ١٢",
            "answer": "x <= -5",
            "answer_ar": "س ≤ -٥",
            "explanation_en": "Comprehensive review of multi-step inequalities.",
            "explanation_ar": "مراجعة شاملة للمتباينات متعددة الخطوات.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Distribute -4",
                    "step_ar": "الخطوة ١: وزع -٤",
                    "possible_answers": [
                        "-4(x + 2) >= 12",
                        "-4x - 8 >= 12"
                    ],
                    "possible_answers_ar": [
                        "-٤(س + ٢) ≥ ١٢",
                        "-٤س - ٨ ≥ ١٢"
                    ]
                },
                {
                    "step_en": "Step 2: Add 8 to both sides",
                    "step_ar": "الخطوة ٢: أضف ٨ إلى كلا الطرفين",
                    "possible_answers": [
                        "-4x - 8 + 8 >= 12 + 8",
                        "-4x >= 12 + 8",
                        "-4x >= 20"
                    ],
                    "possible_answers_ar": [
                        "-٤س - ٨ + ٨ ≥ ١٢ + ٨",
                        "-٤س ≥ ١٢ + ٨",
                        "-٤س ≥ ٢٠"
                    ]
                },
                {
                    "step_en": "Step 3: Divide by -4 (flip sign!)",
                    "step_ar": "الخطوة ٣: اقسم على -٤ (اقلب الإشارة!)",
                    "possible_answers": [
                        "-4x / -4 <= 20 / -4",
                        "x <= 20 / -4",
                        "x <= -5"
                    ],
                    "possible_answers_ar": [
                        "-٤س / -٤ ≤ ٢٠ / -٤",
                        "س ≤ ٢٠ / -٤",
                        "س ≤ -٥"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "Distribute the negative 4 carefully",
                "Remember to flip the inequality sign when dividing by -4"
            ],
            "hints_ar": [
                "وزع الـ ٤ السالب بعناية",
                "تذكر قلب إشارة المتباينة عند القسمة على -٤"
            ]
        }
    ]
    
    # SECTION 4 PROBLEMS
    section4_problems = [
        {
            "id": "prep4",
            "section_id": "section4",
            "type": "preparation",
            "weight": 10,
            "question_en": "Solve: 3 < x + 2 < 8",
            "question_ar": "حل: ٣ < س + ٢ < ٨",
            "answer": "1 < x < 6",
            "answer_ar": "١ < س < ٦",
            "explanation_en": "This is a compound inequality with AND condition.",
            "explanation_ar": "هذه متباينة مركبة بشرط و.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Subtract 2 from all parts",
                    "step_ar": "الخطوة ١: اطرح ٢ من جميع الأجزاء",
                    "possible_answers": [
                        "3 - 2 < x + 2 - 2 < 8 - 2",
                        "1 < x < 6"
                    ],
                    "possible_answers_ar": [
                        "٣ - ٢ < س + ٢ - ٢ < ٨ - ٢",
                        "١ < س < ٦"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "This is a compound inequality - work with all three parts",
                "Subtract 2 from each part of the inequality"
            ],
            "hints_ar": [
                "هذه متباينة مركبة - اعمل مع الأجزاء الثلاثة",
                "اطرح ٢ من كل جزء في المتباينة"
            ]
        },
        {
            "id": "explanation4",
            "section_id": "section4",
            "type": "explanation",
            "weight": 0,
            "question_en": "Learn Compound Inequalities",
            "question_ar": "تعلم المتباينات المركبة",
            "answer": "",
            "answer_ar": "",
            "show_full_solution": False,
            "hide_answer": False,
            "explanation_en": "Master AND and OR compound inequalities",
            "explanation_ar": "اتقن المتباينات المركبة و و أو",
            "interactive_examples": [
                {
                    "title_en": "Level 1: AND Compound (between values)",
                    "title_ar": "المستوى ١: مركبة و (بين القيم)",
                    "problem_en": "5 ≤ 2x + 1 ≤ 11",
                    "problem_ar": "٥ ≤ ٢س + ١ ≤ ١١",
                    "solution_en": "Original: 5 ≤ 2x + 1 ≤ 11\\n\\nStep 1: Subtract 1 from all parts\\n5 - 1 ≤ 2x + 1 - 1 ≤ 11 - 1\\n4 ≤ 2x ≤ 10\\n\\nStep 2: Divide all parts by 2\\n4/2 ≤ 2x/2 ≤ 10/2\\n2 ≤ x ≤ 5",
                    "solution_ar": "الأصلية: ٥ ≤ ٢س + ١ ≤ ١١\\n\\nالخطوة ١: اطرح ١ من جميع الأجزاء\\n٥ - ١ ≤ ٢س + ١ - ١ ≤ ١١ - ١\\n٤ ≤ ٢س ≤ ١٠\\n\\nالخطوة ٢: اقسم جميع الأجزاء على ٢\\n٤/٢ ≤ ٢س/٢ ≤ ١٠/٢\\n٢ ≤ س ≤ ٥"
                },
                {
                    "title_en": "Level 2: OR Compound (separate conditions)",
                    "title_ar": "المستوى ٢: مركبة أو (شروط منفصلة)",
                    "problem_en": "x - 3 < -5 OR x + 2 > 8",
                    "problem_ar": "س - ٣ < -٥ أو س + ٢ > ٨",
                    "solution_en": "Solve each inequality separately:\\n\\nPart 1: x - 3 < -5\\nx < -5 + 3\\nx < -2\\n\\nPart 2: x + 2 > 8\\nx > 8 - 2\\nx > 6\\n\\nFinal answer: x < -2 OR x > 6",
                    "solution_ar": "حل كل متباينة منفصلة:\\n\\nالجزء ١: س - ٣ < -٥\\nس < -٥ + ٣\\nس < -٢\\n\\nالجزء ٢: س + ٢ > ٨\\nس > ٨ - ٢\\nس > ٦\\n\\nالإجابة النهائية: س < -٢ أو س > ٦"
                }
            ],
            "hints_en": [
                "AND compound: x is between two values (a < x < b)",
                "OR compound: x satisfies either condition (x < a OR x > b)"
            ],
            "hints_ar": [
                "المركبة و: س بين قيمتين (أ < س < ب)",
                "المركبة أو: س يحقق أي من الشرطين (س < أ أو س > ب)"
            ]
        },
        {
            "id": "practice4",
            "section_id": "section4",
            "type": "practice",
            "weight": 30,
            "question_en": "Solve: -1 ≤ 3x - 4 ≤ 8",
            "question_ar": "حل: -١ ≤ ٣س - ٤ ≤ ٨",
            "answer": "1 <= x <= 4",
            "answer_ar": "١ ≤ س ≤ ٤",
            "explanation_en": "Practice compound inequalities with multiple operations.",
            "explanation_ar": "تدرب على المتباينات المركبة مع عدة عمليات.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Add 4 to all parts",
                    "step_ar": "الخطوة ١: أضف ٤ إلى جميع الأجزاء",
                    "possible_answers": [
                        "-1 + 4 <= 3x - 4 + 4 <= 8 + 4",
                        "3 <= 3x <= 12"
                    ],
                    "possible_answers_ar": [
                        "-١ + ٤ ≤ ٣س - ٤ + ٤ ≤ ٨ + ٤",
                        "٣ ≤ ٣س ≤ ١٢"
                    ]
                },
                {
                    "step_en": "Step 2: Divide all parts by 3",
                    "step_ar": "الخطوة ٢: اقسم جميع الأجزاء على ٣",
                    "possible_answers": [
                        "3/3 <= 3x/3 <= 12/3",
                        "1 <= x <= 4"
                    ],
                    "possible_answers_ar": [
                        "٣/٣ ≤ ٣س/٣ ≤ ١٢/٣",
                        "١ ≤ س ≤ ٤"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "Work with all three parts of the compound inequality",
                "Apply the same operation to each part"
            ],
            "hints_ar": [
                "اعمل مع الأجزاء الثلاثة للمتباينة المركبة",
                "طبق نفس العملية على كل جزء"
            ]
        },
        {
            "id": "practice_word4",
            "section_id": "section4",
            "type": "practice_word",
            "weight": 30,
            "question_en": "A company's monthly profit P (in thousands) follows: 20 ≤ 2P + 8 ≤ 36. What is the range of possible monthly profits?",
            "question_ar": "ربح شركة شهري ر (بالآلاف) يتبع: ٢٠ ≤ ٢ر + ٨ ≤ ٣٦. ما هو نطاق الأرباح الشهرية الممكنة؟",
            "answer": "6 <= P <= 14",
            "answer_ar": "٦ ≤ ر ≤ ١٤",
            "explanation_en": "Real-world application of compound inequalities.",
            "explanation_ar": "تطبيق من الواقع للمتباينات المركبة.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Start with given compound inequality",
                    "step_ar": "الخطوة ١: ابدأ بالمتباينة المركبة المعطاة",
                    "possible_answers": [
                        "20 <= 2P + 8 <= 36"
                    ],
                    "possible_answers_ar": [
                        "٢٠ ≤ ٢ر + ٨ ≤ ٣٦"
                    ]
                },
                {
                    "step_en": "Step 2: Subtract 8 from all parts",
                    "step_ar": "الخطوة ٢: اطرح ٨ من جميع الأجزاء",
                    "possible_answers": [
                        "20 - 8 <= 2P + 8 - 8 <= 36 - 8",
                        "12 <= 2P <= 28"
                    ],
                    "possible_answers_ar": [
                        "٢٠ - ٨ ≤ ٢ر + ٨ - ٨ ≤ ٣٦ - ٨",
                        "١٢ ≤ ٢ر ≤ ٢٨"
                    ]
                },
                {
                    "step_en": "Step 3: Divide all parts by 2",
                    "step_ar": "الخطوة ٣: اقسم جميع الأجزاء على ٢",
                    "possible_answers": [
                        "12/2 <= 2P/2 <= 28/2",
                        "6 <= P <= 14"
                    ],
                    "possible_answers_ar": [
                        "١٢/٢ ≤ ٢ر/٢ ≤ ٢٨/٢",
                        "٦ ≤ ر ≤ ١٤"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "The inequality 20 ≤ 2P + 8 ≤ 36 describes the range",
                "Solve for P by isolating it in the middle",
                "The answer represents thousands, so P is between 6,000 and 14,000"
            ],
            "hints_ar": [
                "المتباينة ٢٠ ≤ ٢ر + ٨ ≤ ٣٦ تصف النطاق",
                "حل من أجل ر بعزله في الوسط",
                "الإجابة تمثل الآلاف، إذاً ر بين ٦٠٠٠ و ١٤٠٠٠"
            ]
        },
        {
            "id": "assessment4",
            "section_id": "section4",
            "type": "assessment",
            "weight": 40,
            "question_en": "Solve: x + 3 < 1 OR 2x - 5 ≥ 7",
            "question_ar": "حل: س + ٣ < ١ أو ٢س - ٥ ≥ ٧",
            "answer": "x < -2 OR x >= 6",
            "answer_ar": "س < -٢ أو س ≥ ٦",
            "explanation_en": "Assessment of OR compound inequalities.",
            "explanation_ar": "تقييم المتباينات المركبة أو.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Solve first inequality x + 3 < 1",
                    "step_ar": "الخطوة ١: حل المتباينة الأولى س + ٣ < ١",
                    "possible_answers": [
                        "x + 3 < 1",
                        "x + 3 - 3 < 1 - 3",
                        "x < -2"
                    ],
                    "possible_answers_ar": [
                        "س + ٣ < ١",
                        "س + ٣ - ٣ < ١ - ٣",
                        "س < -٢"
                    ]
                },
                {
                    "step_en": "Step 2: Solve second inequality 2x - 5 ≥ 7",
                    "step_ar": "الخطوة ٢: حل المتباينة الثانية ٢س - ٥ ≥ ٧",
                    "possible_answers": [
                        "2x - 5 >= 7",
                        "2x - 5 + 5 >= 7 + 5",
                        "2x >= 12",
                        "x >= 6"
                    ],
                    "possible_answers_ar": [
                        "٢س - ٥ ≥ ٧",
                        "٢س - ٥ + ٥ ≥ ٧ + ٥",
                        "٢س ≥ ١٢",
                        "س ≥ ٦"
                    ]
                },
                {
                    "step_en": "Step 3: Combine with OR",
                    "step_ar": "الخطوة ٣: ادمج بـ أو",
                    "possible_answers": [
                        "x < -2 OR x >= 6"
                    ],
                    "possible_answers_ar": [
                        "س < -٢ أو س ≥ ٦"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "Solve each inequality separately",
                "The final answer uses OR to connect both solutions"
            ],
            "hints_ar": [
                "حل كل متباينة منفصلة",
                "الإجابة النهائية تستخدم أو لربط الحلين"
            ]
        },
        {
            "id": "examprep4",
            "section_id": "section4",
            "type": "examprep",
            "weight": 20,
            "question_en": "Final Review: Solve -2 ≤ (3x + 6)/2 < 4",
            "question_ar": "المراجعة النهائية: حل -٢ ≤ (٣س + ٦)/٢ < ٤",
            "answer": "-6 <= x < 2",
            "answer_ar": "-٦ ≤ س < ٢",
            "explanation_en": "Comprehensive review of compound inequalities with fractions.",
            "explanation_ar": "مراجعة شاملة للمتباينات المركبة مع الكسور.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Multiply all parts by 2",
                    "step_ar": "الخطوة ١: اضرب جميع الأجزاء في ٢",
                    "possible_answers": [
                        "-2 * 2 <= (3x + 6)/2 * 2 < 4 * 2",
                        "-4 <= 3x + 6 < 8"
                    ],
                    "possible_answers_ar": [
                        "-٢ * ٢ ≤ (٣س + ٦)/٢ * ٢ < ٤ * ٢",
                        "-٤ ≤ ٣س + ٦ < ٨"
                    ]
                },
                {
                    "step_en": "Step 2: Subtract 6 from all parts",
                    "step_ar": "الخطوة ٢: اطرح ٦ من جميع الأجزاء",
                    "possible_answers": [
                        "-4 - 6 <= 3x + 6 - 6 < 8 - 6",
                        "-10 <= 3x < 2"
                    ],
                    "possible_answers_ar": [
                        "-٤ - ٦ ≤ ٣س + ٦ - ٦ < ٨ - ٦",
                        "-١٠ ≤ ٣س < ٢"
                    ]
                },
                {
                    "step_en": "Step 3: Divide all parts by 3",
                    "step_ar": "الخطوة ٣: اقسم جميع الأجزاء على ٣",
                    "possible_answers": [
                        "-10/3 <= 3x/3 < 2/3",
                        "-3.33 <= x < 0.67",
                        "-6 <= x < 2"
                    ],
                    "possible_answers_ar": [
                        "-١٠/٣ ≤ ٣س/٣ < ٢/٣",
                        "-٣.٣٣ ≤ س < ٠.٦٧",
                        "-٦ ≤ س < ٢"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "First eliminate the fraction by multiplying by 2",
                "Then isolate x by subtracting 6 and dividing by 3"
            ],
            "hints_ar": [
                "أولاً ألغِ الكسر بالضرب في ٢",
                "ثم اعزل س بطرح ٦ والقسمة على ٣"
            ]
        }
    ]
    
    # SECTION 5 PROBLEMS
    section5_problems = [
        {
            "id": "prep5",
            "section_id": "section5",
            "type": "preparation",
            "weight": 10,
            "question_en": "Solve: |x| < 4",
            "question_ar": "حل: |س| < ٤",
            "answer": "-4 < x < 4",
            "answer_ar": "-٤ < س < ٤",
            "explanation_en": "This is a basic absolute value inequality.",
            "explanation_ar": "هذه متباينة قيمة مطلقة أساسية.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Convert to compound inequality",
                    "step_ar": "الخطوة ١: حول إلى متباينة مركبة",
                    "possible_answers": [
                        "|x| < 4 means -4 < x < 4",
                        "-4 < x < 4"
                    ],
                    "possible_answers_ar": [
                        "|س| < ٤ تعني -٤ < س < ٤",
                        "-٤ < س < ٤"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "|x| < a means -a < x < a",
                "The absolute value inequality creates a compound inequality"
            ],
            "hints_ar": [
                "|س| < أ تعني -أ < س < أ",
                "متباينة القيمة المطلقة تُنشئ متباينة مركبة"
            ]
        },
        {
            "id": "explanation5",
            "section_id": "section5",
            "type": "explanation",
            "weight": 0,
            "question_en": "Learn Absolute Value Inequalities",
            "question_ar": "تعلم متباينات القيمة المطلقة",
            "answer": "",
            "answer_ar": "",
            "show_full_solution": False,
            "hide_answer": False,
            "explanation_en": "Master absolute value inequalities and their conversion to compound inequalities",
            "explanation_ar": "اتقن متباينات القيمة المطلقة وتحويلها إلى متباينات مركبة",
            "interactive_examples": [
                {
                    "title_en": "Level 1: Basic |x| < a (less than)",
                    "title_ar": "المستوى ١: أساسي |س| < أ (أصغر من)",
                    "problem_en": "|x| ≤ 3",
                    "problem_ar": "|س| ≤ ٣",
                    "solution_en": "Original: |x| ≤ 3\\n\\nRule: |x| ≤ a means -a ≤ x ≤ a\\n\\nSolution: -3 ≤ x ≤ 3\\n\\nMeaning: x is between -3 and 3 (inclusive)",
                    "solution_ar": "الأصلية: |س| ≤ ٣\\n\\nالقاعدة: |س| ≤ أ تعني -أ ≤ س ≤ أ\\n\\nالحل: -٣ ≤ س ≤ ٣\\n\\nالمعنى: س بين -٣ و ٣ (شامل)"
                },
                {
                    "title_en": "Level 2: |x| > a (greater than)",
                    "title_ar": "المستوى ٢: |س| > أ (أكبر من)",
                    "problem_en": "|x| > 2",
                    "problem_ar": "|س| > ٢",
                    "solution_en": "Original: |x| > 2\\n\\nRule: |x| > a means x < -a OR x > a\\n\\nSolution: x < -2 OR x > 2\\n\\nMeaning: x is outside the interval [-2, 2]",
                    "solution_ar": "الأصلية: |س| > ٢\\n\\nالقاعدة: |س| > أ تعني س < -أ أو س > أ\\n\\nالحل: س < -٢ أو س > ٢\\n\\nالمعنى: س خارج الفترة [-٢، ٢]"
                },
                {
                    "title_en": "Level 3: Complex |ax + b| < c",
                    "title_ar": "المستوى ٣: معقد |أس + ب| < ج",
                    "problem_en": "|2x - 6| < 4",
                    "problem_ar": "|٢س - ٦| < ٤",
                    "solution_en": "Original: |2x - 6| < 4\\n\\nStep 1: Apply rule |expr| < a means -a < expr < a\\n-4 < 2x - 6 < 4\\n\\nStep 2: Add 6 to all parts\\n-4 + 6 < 2x - 6 + 6 < 4 + 6\\n2 < 2x < 10\\n\\nStep 3: Divide by 2\\n1 < x < 5",
                    "solution_ar": "الأصلية: |٢س - ٦| < ٤\\n\\nالخطوة ١: طبق القاعدة |تعبير| < أ تعني -أ < تعبير < أ\\n-٤ < ٢س - ٦ < ٤\\n\\nالخطوة ٢: أضف ٦ لجميع الأجزاء\\n-٤ + ٦ < ٢س - ٦ + ٦ < ٤ + ٦\\n٢ < ٢س < ١٠\\n\\nالخطوة ٣: اقسم على ٢\\n١ < س < ٥"
                }
            ],
            "hints_en": [
                "Key Rules: |x| < a → -a < x < a (AND/between)",
                "Key Rules: |x| > a → x < -a OR x > a (OR/outside)",
                "For |expression| inequalities, first apply the rule, then solve the resulting compound inequality"
            ],
            "hints_ar": [
                "القواعد الأساسية: |س| < أ ← -أ < س < أ (و/بين)",
                "القواعد الأساسية: |س| > أ ← س < -أ أو س > أ (أو/خارج)",
                "لمتباينات |تعبير|، أولاً طبق القاعدة، ثم حل المتباينة المركبة الناتجة"
            ]
        },
        {
            "id": "practice5",
            "section_id": "section5",
            "type": "practice",
            "weight": 30,
            "question_en": "Solve: |3x + 9| ≤ 12",
            "question_ar": "حل: |٣س + ٩| ≤ ١٢",
            "answer": "-7 <= x <= 1",
            "answer_ar": "-٧ ≤ س ≤ ١",
            "explanation_en": "Practice absolute value inequalities with expressions inside.",
            "explanation_ar": "تدرب على متباينات القيمة المطلقة مع تعابير بالداخل.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Apply absolute value rule for ≤",
                    "step_ar": "الخطوة ١: طبق قاعدة القيمة المطلقة لـ ≤",
                    "possible_answers": [
                        "|3x + 9| <= 12 means -12 <= 3x + 9 <= 12",
                        "-12 <= 3x + 9 <= 12"
                    ],
                    "possible_answers_ar": [
                        "|٣س + ٩| ≤ ١٢ تعني -١٢ ≤ ٣س + ٩ ≤ ١٢",
                        "-١٢ ≤ ٣س + ٩ ≤ ١٢"
                    ]
                },
                {
                    "step_en": "Step 2: Subtract 9 from all parts",
                    "step_ar": "الخطوة ٢: اطرح ٩ من جميع الأجزاء",
                    "possible_answers": [
                        "-12 - 9 <= 3x + 9 - 9 <= 12 - 9",
                        "-21 <= 3x <= 3"
                    ],
                    "possible_answers_ar": [
                        "-١٢ - ٩ ≤ ٣س + ٩ - ٩ ≤ ١٢ - ٩",
                        "-٢١ ≤ ٣س ≤ ٣"
                    ]
                },
                {
                    "step_en": "Step 3: Divide all parts by 3",
                    "step_ar": "الخطوة ٣: اقسم جميع الأجزاء على ٣",
                    "possible_answers": [
                        "-21/3 <= 3x/3 <= 3/3",
                        "-7 <= x <= 1"
                    ],
                    "possible_answers_ar": [
                        "-٢١/٣ ≤ ٣س/٣ ≤ ٣/٣",
                        "-٧ ≤ س ≤ ١"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "Use the rule: |expression| ≤ a becomes -a ≤ expression ≤ a",
                "Solve the compound inequality by isolating x"
            ],
            "hints_ar": [
                "استخدم القاعدة: |تعبير| ≤ أ تصبح -أ ≤ تعبير ≤ أ",
                "حل المتباينة المركبة بعزل س"
            ]
        },
        {
            "id": "practice_word5",
            "section_id": "section5",
            "type": "practice_word",
            "weight": 30,
            "question_en": "The temperature T in a laboratory must stay within 3°C of 20°C for experiments. Write and solve the absolute value inequality to find the acceptable temperature range.",
            "question_ar": "يجب أن تبقى درجة الحرارة د في المختبر ضمن ٣°م من ٢٠°م للتجارب. اكتب وحل متباينة القيمة المطلقة لإيجاد نطاق درجة الحرارة المقبولة.",
            "answer": "17 <= T <= 23",
            "answer_ar": "١٧ ≤ د ≤ ٢٣",
            "explanation_en": "Real-world application of absolute value inequalities for tolerance ranges.",
            "explanation_ar": "تطبيق من الواقع لمتباينات القيمة المطلقة لنطاقات التحمل.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Set up absolute value inequality",
                    "step_ar": "الخطوة ١: ضع متباينة القيمة المطلقة",
                    "possible_answers": [
                        "|T - 20| <= 3",
                        "|T - 20| ≤ 3"
                    ],
                    "possible_answers_ar": [
                        "|د - ٢٠| ≤ ٣"
                    ]
                },
                {
                    "step_en": "Step 2: Apply absolute value rule",
                    "step_ar": "الخطوة ٢: طبق قاعدة القيمة المطلقة",
                    "possible_answers": [
                        "|T - 20| <= 3 means -3 <= T - 20 <= 3",
                        "-3 <= T - 20 <= 3"
                    ],
                    "possible_answers_ar": [
                        "|د - ٢٠| ≤ ٣ تعني -٣ ≤ د - ٢٠ ≤ ٣",
                        "-٣ ≤ د - ٢٠ ≤ ٣"
                    ]
                },
                {
                    "step_en": "Step 3: Add 20 to all parts",
                    "step_ar": "الخطوة ٣: أضف ٢٠ لجميع الأجزاء",
                    "possible_answers": [
                        "-3 + 20 <= T - 20 + 20 <= 3 + 20",
                        "17 <= T <= 23"
                    ],
                    "possible_answers_ar": [
                        "-٣ + ٢٠ ≤ د - ٢٠ + ٢٠ ≤ ٣ + ٢ـ",
                        "١٧ ≤ د ≤ ٢٣"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "The phrase 'within 3°C of 20°C' means |T - 20| ≤ 3",
                "This represents all temperatures that are at most 3 degrees away from 20°C",
                "The answer shows the temperature must be between 17°C and 23°C"
            ],
            "hints_ar": [
                "العبارة 'ضمن ٣°م من ٢٠°م' تعني |د - ٢٠| ≤ ٣",
                "هذا يمثل جميع درجات الحرارة التي تبعد على الأكثر ٣ درجات عن ٢٠°م",
                "الإجابة تظهر أن درجة الحرارة يجب أن تكون بين ١٧°م و ٢٣°م"
            ]
        },
        {
            "id": "assessment5",
            "section_id": "section5",
            "type": "assessment",
            "weight": 40,
            "question_en": "Solve: |2x - 8| > 6",
            "question_ar": "حل: |٢س - ٨| > ٦",
            "answer": "x < 1 OR x > 7",
            "answer_ar": "س < ١ أو س > ٧",
            "explanation_en": "Assessment of absolute value inequalities with OR condition.",
            "explanation_ar": "تقييم متباينات القيمة المطلقة مع شرط أو.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Apply absolute value rule for >",
                    "step_ar": "الخطوة ١: طبق قاعدة القيمة المطلقة لـ >",
                    "possible_answers": [
                        "|2x - 8| > 6 means 2x - 8 < -6 OR 2x - 8 > 6",
                        "2x - 8 < -6 OR 2x - 8 > 6"
                    ],
                    "possible_answers_ar": [
                        "|٢س - ٨| > ٦ تعني ٢س - ٨ < -٦ أو ٢س - ٨ > ٦",
                        "٢س - ٨ < -٦ أو ٢س - ٨ > ٦"
                    ]
                },
                {
                    "step_en": "Step 2: Solve first inequality 2x - 8 < -6",
                    "step_ar": "الخطوة ٢: حل المتباينة الأولى ٢س - ٨ < -٦",
                    "possible_answers": [
                        "2x - 8 + 8 < -6 + 8",
                        "2x < 2",
                        "x < 1"
                    ],
                    "possible_answers_ar": [
                        "٢س - ٨ + ٨ < -٦ + ٨",
                        "٢س < ٢",
                        "س < ١"
                    ]
                },
                {
                    "step_en": "Step 3: Solve second inequality 2x - 8 > 6",
                    "step_ar": "الخطوة ٣: حل المتباينة الثانية ٢س - ٨ > ٦",
                    "possible_answers": [
                        "2x - 8 + 8 > 6 + 8",
                        "2x > 14",
                        "x > 7"
                    ],
                    "possible_answers_ar": [
                        "٢س - ٨ + ٨ > ٦ + ٨",
                        "٢س > ١٤",
                        "س > ٧"
                    ]
                },
                {
                    "step_en": "Step 4: Combine with OR",
                    "step_ar": "الخطوة ٤: ادمج بـ أو",
                    "possible_answers": [
                        "x < 1 OR x > 7"
                    ],
                    "possible_answers_ar": [
                        "س < ١ أو س > ٧"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "Use the rule: |expression| > a means expression < -a OR expression > a",
                "Solve each inequality separately, then combine with OR"
            ],
            "hints_ar": [
                "استخدم القاعدة: |تعبير| > أ تعني تعبير < -أ أو تعبير > أ",
                "حل كل متباينة منفصلة، ثم ادمج بـ أو"
            ]
        },
        {
            "id": "examprep5",
            "section_id": "section5",
            "type": "examprep",
            "weight": 20,
            "question_en": "Final Review: Solve |4 - 3x| ≤ 8",
            "question_ar": "المراجعة النهائية: حل |٤ - ٣س| ≤ ٨",
            "answer": "-4/3 <= x <= 4",
            "answer_ar": "-٤/٣ ≤ س ≤ ٤",
            "explanation_en": "Comprehensive review of absolute value inequalities.",
            "explanation_ar": "مراجعة شاملة لمتباينات القيمة المطلقة.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Apply absolute value rule for ≤",
                    "step_ar": "الخطوة ١: طبق قاعدة القيمة المطلقة لـ ≤",
                    "possible_answers": [
                        "|4 - 3x| <= 8 means -8 <= 4 - 3x <= 8",
                        "-8 <= 4 - 3x <= 8"
                    ],
                    "possible_answers_ar": [
                        "|٤ - ٣س| ≤ ٨ تعني -٨ ≤ ٤ - ٣س ≤ ٨",
                        "-٨ ≤ ٤ - ٣س ≤ ٨"
                    ]
                },
                {
                    "step_en": "Step 2: Subtract 4 from all parts",
                    "step_ar": "الخطوة ٢: اطرح ٤ من جميع الأجزاء",
                    "possible_answers": [
                        "-8 - 4 <= 4 - 3x - 4 <= 8 - 4",
                        "-12 <= -3x <= 4"
                    ],
                    "possible_answers_ar": [
                        "-٨ - ٤ ≤ ٤ - ٣س - ٤ ≤ ٨ - ٤",
                        "-١٢ ≤ -٣س ≤ ٤"
                    ]
                },
                {
                    "step_en": "Step 3: Divide by -3 (flip signs!)",
                    "step_ar": "الخطوة ٣: اقسم على -٣ (اقلب الإشارات!)",
                    "possible_answers": [
                        "-12/-3 >= -3x/-3 >= 4/-3",
                        "4 >= x >= -4/3",
                        "-4/3 <= x <= 4"
                    ],
                    "possible_answers_ar": [
                        "-١٢/-٣ ≥ -٣س/-٣ ≥ ٤/-٣",
                        "٤ ≥ س ≥ -٤/٣",
                        "-٤/٣ ≤ س ≤ ٤"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "Remember to flip inequality signs when dividing by negative",
                "The final answer can be written as -4/3 ≤ x ≤ 4 or -1.33 ≤ x ≤ 4"
            ],
            "hints_ar": [
                "تذكر قلب إشارات المتباينة عند القسمة على سالب",
                "الإجابة النهائية يمكن كتابتها كـ -٤/٣ ≤ س ≤ ٤ أو -١.٣٣ ≤ س ≤ ٤"
            ]
        }
    ]
    
    print("📝 Inserting Section 1 problems...")
    await problems_collection.insert_many(section1_problems)
    
    print("📝 Inserting Section 2 problems...")
    await problems_collection.insert_many(section2_problems)
    
    print("📝 Inserting Section 3 problems...")
    await problems_collection.insert_many(section3_problems)
    
    print("📝 Inserting Section 4 problems...")
    await problems_collection.insert_many(section4_problems)
    
    print("📝 Inserting Section 5 problems...")
    await problems_collection.insert_many(section5_problems)
    
    print("✅ Database migration completed successfully!")
    print(f"📊 Inserted {len(sections_data)} sections")
    print(f"📊 Inserted {len(section1_problems + section2_problems + section3_problems + section4_problems + section5_problems)} total problems")
    
    # Close connection
    client.close()
    print("🔌 Database connection closed")

if __name__ == "__main__":
    print("🚀 Starting Math Tutoring App Database Migration...")
    print("=" * 60)
    
    # Run the migration
    asyncio.run(migrate_database())
    
    print("=" * 60)
    print("✅ Migration completed! Your database now has all 5 sections with complete content.")
    print("📚 Each section includes: preparation, explanation, practice, assessment, and exam prep problems")
    print("🎯 All problems include hints, step-by-step solutions, and Arabic translations")