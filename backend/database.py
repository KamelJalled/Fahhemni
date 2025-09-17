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
    
    # Section 1 problems data - Updated with new curriculum content
    section1_problems = [
        {
            "id": "prep1",
            "section_id": "section1",
            "type": ProblemType.PREPARATION,
            "weight": 10,
            "question_en": "x - 5 > 10",
            "question_ar": "س - ٥ > ١٠",
            "answer": "x > 15",
            "answer_ar": "س > ١٥",
            "explanation_en": "This is a review problem for solving inequalities.",
            "explanation_ar": "هذه مسألة مراجعة لحل المتباينات.",
            "show_full_solution": True,
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
            "type": ProblemType.EXPLANATION,
            "weight": 0,
            "question_en": "Learn Addition/Subtraction Inequalities",
            "question_ar": "تعلم متباينات الجمع والطرح",
            "answer": "",
            "answer_ar": "",
            "show_full_solution": True,
            "hide_answer": False,
            "explanation_en": "Learn to solve inequalities involving addition and subtraction",
            "explanation_ar": "تعلم حل المتباينات التي تتضمن الجمع والطرح",
            "interactive_examples": [
                {
                    "title_en": "Level 1: Simple (Example 1A - System Solved)",
                    "title_ar": "المستوى ١: بسيط (المثال ١أ - حل النظام)",
                    "problem_en": "x - 8 > 2",
                    "problem_ar": "س - ٨ > ٢",
                    "solution_en": "Original inequality: x - 8 > 2\n\nStep 1: x - 8 + 8 > 2 + 8\nStep 2: x > 10",
                    "solution_ar": "المتباينة الأصلية: س - ٨ > ٢\n\nالخطوة ١: س - ٨ + ٨ > ٢ + ٨\nالخطوة ٢: س > ١٠",
                    "practice_question_en": "Now solve: y - 5 > 10",
                    "practice_question_ar": "الآن حل: ص - ٥ > ١٠",
                    "practice_answer": "y > 15",
                    "practice_answer_ar": "ص > ١٥"
                },
                {
                    "title_en": "Level 2: Medium (Example 2A - System Solved)",
                    "title_ar": "المستوى ٢: متوسط (المثال ٢أ - حل النظام)",
                    "problem_en": "12 ≤ k + 3",
                    "problem_ar": "١٢ ≤ ك + ٣",
                    "solution_en": "Original inequality: 12 ≤ k + 3\n\nStep 1: 12 - 3 ≤ k + 3 - 3\nStep 2: 9 ≤ k",
                    "solution_ar": "المتباينة الأصلية: ١٢ ≤ ك + ٣\n\nالخطوة ١: ١٢ - ٣ ≤ ك + ٣ - ٣\nالخطوة ٢: ٩ ≤ ك",
                    "practice_question_en": "Now solve: 20 ≤ m + 8",
                    "practice_question_ar": "الآن حل: ٢٠ ≤ م + ٨",
                    "practice_answer": "12 ≤ m",
                    "practice_answer_ar": "١٢ ≤ م"
                },
                {
                    "title_en": "Level 3: Advanced (Example 3A - System Solved)",
                    "title_ar": "المستوى ٣: متقدم (المثال ٣أ - حل النظام)",
                    "problem_en": "3n + 6 ≥ 2n + 9",
                    "problem_ar": "٣ن + ٦ ≥ ٢ن + ٩",
                    "solution_en": "Original inequality: 3n + 6 ≥ 2n + 9\n\nStep 1: 3n + 6 - 2n ≥ 2n + 9 - 2n\nStep 2: n + 6 ≥ 9\nStep 3: n + 6 - 6 ≥ 9 - 6\nStep 4: n ≥ 3",
                    "solution_ar": "المتباينة الأصلية: ٣ن + ٦ ≥ ٢ن + ٩\n\nالخطوة ١: ٣ن + ٦ - ٢ن ≥ ٢ن + ٩ - ٢ن\nالخطوة ٢: ن + ٦ ≥ ٩\nالخطوة ٣: ن + ٦ - ٦ ≥ ٩ - ٦\nالخطوة ٤: ن ≥ ٣",
                    "practice_question_en": "Now solve: 5k - 4 < 4k + 1",
                    "practice_question_ar": "الآن حل: ٥ك - ٤ < ٤ك + ١",
                    "practice_answer": "k < 5",
                    "practice_answer_ar": "ك < ٥"
                }
            ],
            "step_solutions": [
                {
                    "step_en": "Level 1B Step 1: Add 5 to both sides",
                    "step_ar": "المستوى ١ب الخطوة ١: أضف ٥ إلى كلا الطرفين",
                    "possible_answers": [
                        "y - 5 + 5 > 10 + 5",
                        "y > 15"
                    ],
                    "possible_answers_ar": [
                        "ص - ٥ + ٥ > ١٠ + ٥",
                        "ص > ١٥"
                    ]
                },
                {
                    "step_en": "Level 1B Step 2: Simplify",
                    "step_ar": "المستوى ١ب الخطوة ٢: بسّط",
                    "possible_answers": [
                        "y > 15"
                    ],
                    "possible_answers_ar": [
                        "ص > ١٥"
                    ]
                },
                {
                    "step_en": "Level 2B Step 1: Subtract 8 from both sides",
                    "step_ar": "المستوى ٢ب الخطوة ١: اطرح ٨ من كلا الطرفين",
                    "possible_answers": [
                        "20 - 8 ≤ m + 8 - 8",
                        "12 ≤ m"
                    ],
                    "possible_answers_ar": [
                        "٢٠ - ٨ ≤ م + ٨ - ٨",
                        "١٢ ≤ م"
                    ]
                },
                {
                    "step_en": "Level 2B Step 2: Write in standard form",
                    "step_ar": "المستوى ٢ب الخطوة ٢: اكتب بالشكل القياسي",
                    "possible_answers": [
                        "12 ≤ m",
                        "m ≥ 12"
                    ],
                    "possible_answers_ar": [
                        "١٢ ≤ م",
                        "م ≥ ١٢"
                    ]
                },
                {
                    "step_en": "Level 3B Step 1: Subtract 4k from both sides",
                    "step_ar": "المستوى ٣ب الخطوة ١: اطرح ٤ك من كلا الطرفين",
                    "possible_answers": [
                        "5k - 4k - 4 < 4k - 4k + 1",
                        "5k - 4 - 4k < 4k + 1 - 4k",
                        "k - 4 < 1"
                    ],
                    "possible_answers_ar": [
                        "٥ك - ٤ك - ٤ < ٤ك - ٤ك + ١",
                        "٥ك - ٤ - ٤ك < ٤ك + ١ - ٤ك",
                        "ك - ٤ < ١"
                    ]
                },
                {
                    "step_en": "Level 3B Step 2: Add 4 to both sides",
                    "step_ar": "المستوى ٣ب الخطوة ٢: أضف ٤ إلى كلا الطرفين",
                    "possible_answers": [
                        "k - 4 + 4 < 1 + 4",
                        "k < 1 + 4"
                    ],
                    "possible_answers_ar": [
                        "ك - ٤ + ٤ < ١ + ٤",
                        "ك < ١ + ٤"
                    ]
                },
                {
                    "step_en": "Level 3B Step 3: Simplify to get final answer",
                    "step_ar": "المستوى ٣ب الخطوة ٣: بسّط للحصول على الإجابة النهائية",
                    "possible_answers": [
                        "k < 5"
                    ],
                    "possible_answers_ar": [
                        "ك < ٥"
                    ]
                }
            ],
            "hints_en": [
                "للتخلص من الطرح، ما هي العملية العكسية التي يجب أن تستخدمها؟",
                "قم بتبسيط كلا طرفي المتباينة.",
                "لعزل المتغير 'م'، ماذا يجب أن تفعل بالرقم ٨؟",
                "ما هو ناتج ٢٠ - ٨؟",
                "ابدأ بجمع حدود 'ك' المتشابهة في طرف واحد.",
                "الآن اعزل ك بإضافة ٤ إلى كلا الطرفين."
            ],
            "hints_ar": [
                "To undo subtraction, what is the inverse operation you should use?",
                "Simplify both sides of the inequality.",
                "To isolate the variable 'm', what should you do with the number 8?",
                "What is the result of 20 - 8?",
                "Start by collecting the 'k' terms on one side.",
                "Now isolate k by adding 4 to both sides."
            ]
        },
        {
            "id": "practice1",
            "section_id": "section1",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "question_en": "m + 19 > 56",
            "question_ar": "م + ١٩ > ٥٦",
            "answer": "m > 37",
            "answer_ar": "م > ٣٧",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Subtract 19 from both sides", 
                    "step_ar": "اطرح ١٩ من الطرفين", 
                    "possible_answers": [
                        "m + 19 - 19 > 56 - 19",
                        "m > 56 - 19", 
                        "m > 37"
                    ],
                    "possible_answers_ar": [
                        "م + ١٩ - ١٩ > ٥٦ - ١٩",
                        "م > ٥٦ - ١٩",
                        "م > ٣٧"
                    ]
                },
                {
                    "step_en": "Simplify the calculation", 
                    "step_ar": "بسّط العملية الحسابية",
                    "possible_answers": [
                        "m > 37"
                    ],
                    "possible_answers_ar": [
                        "م > ٣٧"
                    ]
                }
            ],
            "hints_en": [
                "How can you isolate the variable 'm'?",
                "Simplify the calculation."
            ],
            "hints_ar": [
                "كيف يمكنك عزل المتغير 'م'؟",
                "قم بتبسيط العملية الحسابية."
            ]
        },
        {
            "id": "practice2",
            "section_id": "section1",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "question_en": "A school's goal is to collect at least SAR 500. They have SAR 210. How much more money (m) do they need?",
            "question_ar": "هدف مدرسة هو جمع ٥٠٠ ريال على الأقل. لقد جمعوا ٢١٠ ريالات. ما هو المبلغ الإضافي (م) الذي يحتاجون لجمعه؟",
            "answer": "m ≥ 290",
            "answer_ar": "م ≥ ٢٩٠",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Define m as the additional amount needed. Write an inequality showing that 210 + m must be at least 500", 
                    "step_ar": "عرّف م كالمبلغ الإضافي المطلوب. اكتب متباينة توضح أن ٢١٠ + م يجب أن يكون على الأقل ٥٠٠",
                    "possible_answers": [
                        "m + 210 ≥ 500",
                        "210 + m ≥ 500"
                    ],
                    "possible_answers_ar": [
                        "م + ٢١٠ ≥ ٥٠٠",
                        "٢١٠ + م ≥ ٥٠٠"
                    ]
                },
                {
                    "step_en": "Subtract 210 from both sides", 
                    "step_ar": "اطرح ٢١٠ من الطرفين",
                    "possible_answers": [
                        "m + 210 - 210 ≥ 500 - 210",
                        "m ≥ 500 - 210",
                        "210 + m - 210 ≥ 500 - 210"
                    ],
                    "possible_answers_ar": [
                        "م + ٢١٠ - ٢١٠ ≥ ٥٠٠ - ٢١٠",
                        "م ≥ ٥٠٠ - ٢١٠",
                        "٢١٠ + م - ٢١٠ ≥ ٥٠٠ - ٢١٠"
                    ]
                },
                {
                    "step_en": "Simplify to get final answer", 
                    "step_ar": "بسّط للحصول على الإجابة النهائية",
                    "possible_answers": [
                        "m ≥ 290"
                    ],
                    "possible_answers_ar": [
                        "م ≥ ٢٩٠"
                    ]
                }
            ],
            "hints_en": [
                "What inequality symbol does \"at least\" mean? (≥)",
                "Use subtraction to isolate 'm'."
            ],
            "hints_ar": [
                "كلمة \"على الأقل\" تعني أي رمز متباينة؟ (≥)",
                "استخدم عملية الطرح لعزل 'م'."
            ]
        },
        {
            "id": "assessment1",
            "section_id": "section1",
            "type": ProblemType.ASSESSMENT,
            "weight": 30,
            "question_en": "k - 9 ≥ 2",
            "question_ar": "ك - ٩ ≥ ٢",
            "answer": "k ≥ 11",
            "answer_ar": "ك ≥ ١١",
            "show_full_solution": False,
            "hide_answer": True,
            "hints_en": [
                "Think about what operation will help you solve for k.",
                "You need to isolate k by using addition.",
                "That's all the hints available."
            ],
            "hints_ar": [
                "فكر في العملية التي ستساعدك في حل ك.",
                "تحتاج إلى عزل ك باستخدام الجمع.",
                "هذه كل الإرشادات المتاحة."
            ]
        },
        {
            "id": "examprep1",
            "section_id": "section1",
            "type": ProblemType.EXAMPREP,
            "weight": 30,
            "question_en": "Sara has SAR 150 and wants to buy a gift that costs at least SAR 220. Write and solve an inequality to find the additional amount (m) she needs.",
            "question_ar": "لدى سارة ١٥٠ ريالاً وتريد شراء هدية تكلف على الأقل ٢٢٠ ريالاً. اكتب وحل متباينة لإيجاد المبلغ الإضافي (م) الذي تحتاجه.",
            "answer": "m ≥ 70",
            "answer_ar": "م ≥ ٧٠",
            "show_full_solution": False,
            "hide_answer": True,
            "hints_en": [
                "The inequality is 150 + m ≥ 220",
                "Subtract 150 from both sides to solve for m.",
                "That's all the hints available."
            ],
            "hints_ar": [
                "المتباينة هي ١٥٠ + م ≥ ٢٢٠",
                "اطرح ١٥٠ من الطرفين لحل م.",
                "هذه كل الإرشادات المتاحة."
            ]
        }
    ]
    
    # Insert problems
    await problems_collection.insert_many(section1_problems)
    
    # Create section
    section1 = {
        "id": "section1",
        "title_en": "Section 1: Solving Inequalities by Addition or Subtraction",
        "title_ar": "القسم الأول: حل المتباينات بالجمع أو بالطرح"
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
        "title_en": "Section 2: Solving Inequalities by Multiplication or Division",
        "title_ar": "القسم الثاني: حل المتباينات بالضرب أو بالقسمة"
    }
    await sections_collection.insert_one(section2)
    
    # Section 3: Multi-Step Inequalities with Parentheses
    section3_problems = [
        {
            "id": "prep3",
            "section_id": "section3",
            "type": ProblemType.PREPARATION,
            "weight": 10,
            "question_en": "2(x + 3) > 10",
            "question_ar": "٢(س + ٣) > ١٠",
            "answer": "x > 2",
            "answer_ar": "س > ٢",
            "explanation_en": "This inequality has parentheses. We need to distribute first, then solve.",
            "explanation_ar": "هذه المتباينة تحتوي على أقواس. نحتاج للتوزيع أولاً، ثم الحل.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Distribute 2 to terms inside parentheses",
                    "step_ar": "وزع ٢ على الحدود داخل الأقواس",
                    "possible_answers": [
                        "2(x + 3) > 10",
                        "2x + 6 > 10"
                    ],
                    "possible_answers_ar": [
                        "٢(س + ٣) > ١٠",
                        "٢س + ٦ > ١٠"
                    ]
                },
                {
                    "step_en": "Subtract 6 from both sides",
                    "step_ar": "اطرح ٦ من الطرفين",
                    "possible_answers": [
                        "2x + 6 - 6 > 10 - 6",
                        "2x > 10 - 6",
                        "2x > 4"
                    ],
                    "possible_answers_ar": [
                        "٢س + ٦ - ٦ > ١٠ - ٦",
                        "٢س > ١٠ - ٦",
                        "٢س > ٤"
                    ]
                },
                {
                    "step_en": "Divide both sides by 2",
                    "step_ar": "اقسم الطرفين على ٢",
                    "possible_answers": [
                        "2x / 2 > 4 / 2",
                        "x > 4 / 2",
                        "x > 2"
                    ],
                    "possible_answers_ar": [
                        "٢س / ٢ > ٤ / ٢",
                        "س > ٤ / ٢",
                        "س > ٢"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "Start by distributing (multiplying out the parentheses)",
                "Remember: 2(x + 3) = 2x + 6",
                "Then solve like a two-step inequality"
            ],
            "hints_ar": [
                "ابدأ بالتوزيع (ضرب ما داخل الأقواس)",
                "تذكر: ٢(س + ٣) = ٢س + ٦", 
                "ثم احل كمتباينة ذات خطوتين"
            ]
        },
        {
            "id": "explanation3",
            "section_id": "section3", 
            "type": ProblemType.EXPLANATION,
            "weight": 0,
            "question_en": "Learn Multi-Step Inequalities",
            "question_ar": "تعلم المتباينات متعددة الخطوات",
            "answer": "",
            "answer_ar": "",
            "show_full_solution": False,
            "hide_answer": False,
            "interactive_examples": [
                {
                    "title_en": "Example 1: Distribute then Solve",
                    "title_ar": "المثال الأول: وزع ثم احل",
                    "problem_en": "3(2x - 1) ≤ 15",
                    "problem_ar": "٣(٢س - ١) ≤ ١٥",
                    "solution_en": "Step 1: Distribute 3\n3(2x - 1) ≤ 15\n6x - 3 ≤ 15\nStep 2: Add 3 to both sides\n6x - 3 + 3 ≤ 15 + 3\n6x ≤ 18\nStep 3: Divide by 6\n6x ÷ 6 ≤ 18 ÷ 6\nx ≤ 3",
                    "solution_ar": "الخطوة ١: وزع ٣\n٣(٢س - ١) ≤ ١٥\n٦س - ٣ ≤ ١٥\nالخطوة ٢: أضف ٣ للطرفين\n٦س - ٣ + ٣ ≤ ١٥ + ٣\n٦س ≤ ١٨\nالخطوة ٣: اقسم على ٦\n٦س ÷ ٦ ≤ ١٨ ÷ ٦\nس ≤ ٣",
                    "practice_question_en": "Now try: 2(x + 4) < 14",
                    "practice_question_ar": "الآن جرب: ٢(س + ٤) < ١٤",
                    "practice_answer": "x < 3",
                    "practice_answer_ar": "س < ٣"
                },
                {
                    "title_en": "Example 2: More Complex Distribution",
                    "title_ar": "المثال الثاني: توزيع أكثر تعقيداً",
                    "problem_en": "4(x - 2) + 3 ≥ 11",
                    "problem_ar": "٤(س - ٢) + ٣ ≥ ١١",
                    "solution_en": "Step 1: Distribute 4\n4(x - 2) + 3 ≥ 11\n4x - 8 + 3 ≥ 11\nStep 2: Combine like terms\n4x - 5 ≥ 11\nStep 3: Add 5 to both sides\n4x ≥ 16\nStep 4: Divide by 4\nx ≥ 4",
                    "solution_ar": "الخطوة ١: وزع ٤\n٤(س - ٢) + ٣ ≥ ١١\n٤س - ٨ + ٣ ≥ ١١\nالخطوة ٢: اجمع الحدود المتشابهة\n٤س - ٥ ≥ ١١\nالخطوة ٣: أضف ٥ للطرفين\n٤س ≥ ١٦\nالخطوة ٤: اقسم على ٤\nس ≥ ٤",
                    "practice_question_en": "Now try: 3(x + 1) - 2 > 10",
                    "practice_question_ar": "الآن جرب: ٣(س + ١) - ٢ > ١٠",
                    "practice_answer": "x > 3",
                    "practice_answer_ar": "س > ٣"
                }
            ],
            "hints_en": [],
            "hints_ar": []
        },
        {
            "id": "practice3_1",
            "section_id": "section3",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "question_en": "2(x + 3) > 10",
            "question_ar": "٢(س + ٣) > ١٠",
            "answer": "x > 2",
            "answer_ar": "س > ٢",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Distribute 2",
                    "step_ar": "وزع ٢",
                    "possible_answers": [
                        "2x + 6 > 10"
                    ],
                    "possible_answers_ar": [
                        "٢س + ٦ > ١٠"
                    ]
                },
                {
                    "step_en": "Subtract 6 from both sides",
                    "step_ar": "اطرح ٦ من الطرفين",
                    "possible_answers": [
                        "2x > 10 - 6",
                        "2x > 4"
                    ],
                    "possible_answers_ar": [
                        "٢س > ١٠ - ٦",
                        "٢س > ٤"
                    ]
                },
                {
                    "step_en": "Divide by 2",
                    "step_ar": "اقسم على ٢",
                    "possible_answers": [
                        "x > 4 / 2",
                        "x > 2"
                    ],
                    "possible_answers_ar": [
                        "س > ٤ / ٢",
                        "س > ٢"
                    ]
                }
            ],
            "hints_en": [
                "First distribute the 2 across the parentheses",
                "Then solve the two-step inequality",
                "Remember order of operations"
            ],
            "hints_ar": [
                "أولاً وزع الـ ٢ على الأقواس",
                "ثم احل المتباينة ذات الخطوتين",
                "تذكر ترتيب العمليات"
            ]
        },
        {
            "id": "practice3_2",
            "section_id": "section3",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "question_en": "3(2x - 1) ≤ 15",
            "question_ar": "٣(٢س - ١) ≤ ١٥",
            "answer": "x ≤ 3",
            "answer_ar": "س ≤ ٣",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Distribute 3",
                    "step_ar": "وزع ٣",
                    "possible_answers": [
                        "6x - 3 ≤ 15"
                    ],
                    "possible_answers_ar": [
                        "٦س - ٣ ≤ ١٥"
                    ]
                },
                {
                    "step_en": "Add 3 to both sides",
                    "step_ar": "أضف ٣ للطرفين",
                    "possible_answers": [
                        "6x ≤ 15 + 3",
                        "6x ≤ 18"
                    ],
                    "possible_answers_ar": [
                        "٦س ≤ ١٥ + ٣",
                        "٦س ≤ ١٨"
                    ]
                },
                {
                    "step_en": "Divide by 6",
                    "step_ar": "اقسم على ٦",
                    "possible_answers": [
                        "x ≤ 18 / 6",
                        "x ≤ 3"
                    ],
                    "possible_answers_ar": [
                        "س ≤ ١٨ / ٦",
                        "س ≤ ٣"
                    ]
                }
            ],
            "hints_en": [
                "Distribute first: 3 × 2x = 6x and 3 × (-1) = -3",
                "Then solve step by step",
                "What's 18 ÷ 6?"
            ],
            "hints_ar": [
                "وزع أولاً: ٣ × ٢س = ٦س و ٣ × (-١) = -٣",
                "ثم احل خطوة بخطوة",
                "كم ١٨ ÷ ٦؟"
            ]
        },
        {
            "id": "assessment3",
            "section_id": "section3",
            "type": ProblemType.ASSESSMENT,
            "weight": 30,
            "question_en": "4(x - 1) + 2 ≥ 18",
            "question_ar": "٤(س - ١) + ٢ ≥ ١٨",
            "answer": "x ≥ 5",
            "answer_ar": "س ≥ ٥",
            "show_full_solution": False,
            "hide_answer": True,
            "hints_en": [
                "Start by distributing 4 across the parentheses",
                "Then combine like terms before solving",
                "Follow the order of operations carefully"
            ],
            "hints_ar": [
                "ابدأ بتوزيع ٤ على الأقواس",
                "ثم اجمع الحدود المتشابهة قبل الحل",
                "اتبع ترتيب العمليات بعناية"
            ]
        },
        {
            "id": "examprep3",
            "section_id": "section3",
            "type": ProblemType.EXAMPREP,
            "weight": 30,
            "question_en": "5(2 - x) < 20",
            "question_ar": "٥(٢ - س) < ٢٠",
            "answer": "x > -2",
            "answer_ar": "س > -٢",
            "show_full_solution": False,
            "hide_answer": True,
            "hints_en": [
                "Distribute 5 to both terms in parentheses",
                "Be careful with the negative coefficient of x",
                "Remember to flip the inequality when dividing by negative"
            ],
            "hints_ar": [
                "وزع ٥ على كلا الحدين في الأقواس",
                "كن حذراً مع المعامل السالب لـ س",
                "تذكر قلب المتباينة عند القسمة على عدد سالب"
            ]
        }
    ]
    
    await problems_collection.insert_many(section3_problems)
    
    section3 = {
        "id": "section3",
        "title_en": "Section 3: Solving Multi-Step Inequalities",
        "title_ar": "القسم الثالث: حل المتباينات المتعددة الخطوات"
    }
    await sections_collection.insert_one(section3)
    
    # Section 4: Variables on Both Sides
    section4_problems = [
        {
            "id": "prep4", 
            "section_id": "section4",
            "type": ProblemType.PREPARATION,
            "weight": 10,
            "question_en": "3x + 5 < 2x + 9",
            "question_ar": "٣س + ٥ < ٢س + ٩",
            "answer": "x < 4",
            "answer_ar": "س < ٤",
            "explanation_en": "This inequality has variables on both sides. We need to collect like terms.",
            "explanation_ar": "هذه المتباينة تحتوي على متغيرات في الطرفين. نحتاج لجمع الحدود المتشابهة.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Subtract 2x from both sides",
                    "step_ar": "اطرح ٢س من الطرفين",
                    "possible_answers": [
                        "3x - 2x + 5 < 2x - 2x + 9",
                        "3x - 2x + 5 < 9",
                        "x + 5 < 9"
                    ],
                    "possible_answers_ar": [
                        "٣س - ٢س + ٥ < ٢س - ٢س + ٩",
                        "٣س - ٢س + ٥ < ٩",
                        "س + ٥ < ٩"
                    ]
                },
                {
                    "step_en": "Subtract 5 from both sides",
                    "step_ar": "اطرح ٥ من الطرفين",
                    "possible_answers": [
                        "x + 5 - 5 < 9 - 5",
                        "x < 9 - 5",
                        "x < 4"
                    ],
                    "possible_answers_ar": [
                        "س + ٥ - ٥ < ٩ - ٥",
                        "س < ٩ - ٥",
                        "س < ٤"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "Move all x terms to one side",
                "Move all constant terms to the other side",
                "Subtract 2x from both sides first"
            ],
            "hints_ar": [
                "انقل جميع حدود س إلى جانب واحد",
                "انقل جميع الحدود الثابتة إلى الجانب الآخر",
                "اطرح ٢س من الطرفين أولاً"
            ]
        },
        {
            "id": "explanation4",
            "section_id": "section4",
            "type": ProblemType.EXPLANATION,
            "weight": 0,
            "question_en": "Learn Variables on Both Sides",
            "question_ar": "تعلم المتغيرات في الطرفين",
            "answer": "",
            "answer_ar": "",
            "show_full_solution": False,
            "hide_answer": False,
            "interactive_examples": [
                {
                    "title_en": "Example 1: Collect x terms on left",
                    "title_ar": "المثال الأول: اجمع حدود س على اليسار",
                    "problem_en": "5x - 2 > 3x + 6",
                    "problem_ar": "٥س - ٢ > ٣س + ٦",
                    "solution_en": "Step 1: Subtract 3x from both sides\n5x - 3x - 2 > 3x - 3x + 6\n2x - 2 > 6\nStep 2: Add 2 to both sides\n2x - 2 + 2 > 6 + 2\n2x > 8\nStep 3: Divide by 2\nx > 4",
                    "solution_ar": "الخطوة ١: اطرح ٣س من الطرفين\n٥س - ٣س - ٢ > ٣س - ٣س + ٦\n٢س - ٢ > ٦\nالخطوة ٢: أضف ٢ للطرفين\n٢س - ٢ + ٢ > ٦ + ٢\n٢س > ٨\nالخطوة ٣: اقسم على ٢\nس > ٤",
                    "practice_question_en": "Now try: 4x + 1 ≤ 2x + 7",
                    "practice_question_ar": "الآن جرب: ٤س + ١ ≤ ٢س + ٧",
                    "practice_answer": "x ≤ 3",
                    "practice_answer_ar": "س ≤ ٣"
                },
                {
                    "title_en": "Example 2: Collect x terms on right",
                    "title_ar": "المثال الثاني: اجمع حدود س على اليمين",
                    "problem_en": "2x + 8 ≤ 5x - 1",
                    "problem_ar": "٢س + ٨ ≤ ٥س - ١",
                    "solution_en": "Step 1: Subtract 2x from both sides\n2x - 2x + 8 ≤ 5x - 2x - 1\n8 ≤ 3x - 1\nStep 2: Add 1 to both sides\n8 + 1 ≤ 3x - 1 + 1\n9 ≤ 3x\nStep 3: Divide by 3\n3 ≤ x  or  x ≥ 3",
                    "solution_ar": "الخطوة ١: اطرح ٢س من الطرفين\n٢س - ٢س + ٨ ≤ ٥س - ٢س - ١\n٨ ≤ ٣س - ١\nالخطوة ٢: أضف ١ للطرفين\n٨ + ١ ≤ ٣س - ١ + ١\n٩ ≤ ٣س\nالخطوة ٣: اقسم على ٣\n٣ ≤ س  أو  س ≥ ٣",
                    "practice_question_en": "Now try: x + 3 > 4x - 6",
                    "practice_question_ar": "الآن جرب: س + ٣ > ٤س - ٦",
                    "practice_answer": "x < 3",
                    "practice_answer_ar": "س < ٣"
                }
            ],
            "hints_en": [],
            "hints_ar": []
        },
        {
            "id": "practice4_1",
            "section_id": "section4",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "question_en": "3x + 5 < 2x + 9",
            "question_ar": "٣س + ٥ < ٢س + ٩",
            "answer": "x < 4",
            "answer_ar": "س < ٤",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Subtract 2x from both sides",
                    "step_ar": "اطرح ٢س من الطرفين",
                    "possible_answers": [
                        "3x - 2x + 5 < 9",
                        "x + 5 < 9"
                    ],
                    "possible_answers_ar": [
                        "٣س - ٢س + ٥ < ٩",
                        "س + ٥ < ٩"
                    ]
                },
                {
                    "step_en": "Subtract 5 from both sides",
                    "step_ar": "اطرح ٥ من الطرفين",
                    "possible_answers": [
                        "x < 9 - 5",
                        "x < 4"
                    ],
                    "possible_answers_ar": [
                        "س < ٩ - ٥",
                        "س < ٤"
                    ]
                }
            ],
            "hints_en": [
                "Collect all x terms on one side",
                "Get the smaller coefficient on the side you want to eliminate",
                "Then isolate x"
            ],
            "hints_ar": [
                "اجمع جميع حدود س في جانب واحد",
                "احصل على المعامل الأصغر في الجانب الذي تريد إزالته",
                "ثم اعزل س"
            ]
        },
        {
            "id": "practice4_2", 
            "section_id": "section4",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "question_en": "5x - 2 > 3x + 6",
            "question_ar": "٥س - ٢ > ٣س + ٦",
            "answer": "x > 4",
            "answer_ar": "س > ٤",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Subtract 3x from both sides",
                    "step_ar": "اطرح ٣س من الطرفين",
                    "possible_answers": [
                        "5x - 3x - 2 > 6",
                        "2x - 2 > 6"
                    ],
                    "possible_answers_ar": [
                        "٥س - ٣س - ٢ > ٦",
                        "٢س - ٢ > ٦"
                    ]
                },
                {
                    "step_en": "Add 2 to both sides",
                    "step_ar": "أضف ٢ للطرفين",
                    "possible_answers": [
                        "2x > 6 + 2",
                        "2x > 8"
                    ],
                    "possible_answers_ar": [
                        "٢س > ٦ + ٢",
                        "٢س > ٨"
                    ]
                },
                {
                    "step_en": "Divide by 2",
                    "step_ar": "اقسم على ٢",
                    "possible_answers": [
                        "x > 8 / 2",
                        "x > 4"
                    ],
                    "possible_answers_ar": [
                        "س > ٨ / ٢",
                        "س > ٤"
                    ]
                }
            ],
            "hints_en": [
                "Move variable terms to one side first",
                "5x - 3x = 2x",
                "Then solve the two-step inequality"
            ],
            "hints_ar": [
                "انقل حدود المتغير إلى جانب واحد أولاً",
                "٥س - ٣س = ٢س",
                "ثم احل المتباينة ذات الخطوتين"
            ]
        },
        {
            "id": "assessment4",
            "section_id": "section4",
            "type": ProblemType.ASSESSMENT,
            "weight": 30,
            "question_en": "4x - 3 ≤ 2x + 5",
            "question_ar": "٤س - ٣ ≤ ٢س + ٥",
            "answer": "x ≤ 4",
            "answer_ar": "س ≤ ٤",
            "show_full_solution": False,
            "hide_answer": True,
            "hints_en": [
                "Collect variable terms on one side and constants on the other",
                "Start by subtracting 2x from both sides",
                "Then add or subtract to isolate x"
            ],
            "hints_ar": [
                "اجمع حدود المتغير في جانب والثوابت في الآخر",
                "ابدأ بطرح ٢س من الطرفين",
                "ثم اجمع أو اطرح لعزل س"
            ]
        },
        {
            "id": "examprep4",
            "section_id": "section4",
            "type": ProblemType.EXAMPREP,
            "weight": 30,
            "question_en": "7x + 2 ≥ 4x - 10",
            "question_ar": "٧س + ٢ ≥ ٤س - ١٠",
            "answer": "x ≥ -4",
            "answer_ar": "س ≥ -٤",
            "show_full_solution": False,
            "hide_answer": True,
            "hints_en": [
                "This involves negative numbers - be careful with your arithmetic",
                "Move all x terms to the left and constants to the right",
                "7x - 4x = 3x"
            ],
            "hints_ar": [
                "هذا يتضمن أرقام سالبة - كن حذراً مع الحساب",
                "انقل جميع حدود س إلى اليسار والثوابت إلى اليمين",
                "٧س - ٤س = ٣س"
            ]
        }
    ]
    
    await problems_collection.insert_many(section4_problems)
    
    section4 = {
        "id": "section4", 
        "title_en": "Section 4: Solving Compound Inequalities", 
        "title_ar": "القسم الرابع: حل المتباينات المركبة"
    }
    await sections_collection.insert_one(section4)
    
    # Section 5: Compound Inequalities  
    section5_problems = [
        {
            "id": "prep5",
            "section_id": "section5",
            "type": ProblemType.PREPARATION,
            "weight": 10,
            "question_en": "-3 < 2x + 1 ≤ 7",
            "question_ar": "-٣ < ٢س + ١ ≤ ٧",
            "answer": "-2 < x ≤ 3",
            "answer_ar": "-٢ < س ≤ ٣",
            "explanation_en": "This is a compound inequality. We solve both parts at the same time.",
            "explanation_ar": "هذه متباينة مركبة. نحل كلا الجزئين في نفس الوقت.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Subtract 1 from all parts",
                    "step_ar": "اطرح ١ من جميع الأجزاء",
                    "possible_answers": [
                        "-3 - 1 < 2x + 1 - 1 ≤ 7 - 1",
                        "-4 < 2x ≤ 6"
                    ],
                    "possible_answers_ar": [
                        "-٣ - ١ < ٢س + ١ - ١ ≤ ٧ - ١",
                        "-٤ < ٢س ≤ ٦"
                    ]
                },
                {
                    "step_en": "Divide all parts by 2",
                    "step_ar": "اقسم جميع الأجزاء على ٢",
                    "possible_answers": [
                        "-4 / 2 < 2x / 2 ≤ 6 / 2",
                        "-2 < x ≤ 3"
                    ],
                    "possible_answers_ar": [
                        "-٤ / ٢ < ٢س / ٢ ≤ ٦ / ٢",
                        "-٢ < س ≤ ٣"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "Apply the same operation to all three parts",
                "Keep the inequality signs in the same direction",
                "Work with all parts simultaneously"
            ],
            "hints_ar": [
                "طبق نفس العملية على الأجزاء الثلاثة",
                "احتفظ بإشارات المتباينة في نفس الاتجاه",
                "اعمل مع جميع الأجزاء بشكل متزامن"
            ]
        },
        {
            "id": "explanation5",
            "section_id": "section5",
            "type": ProblemType.EXPLANATION,
            "weight": 0,
            "question_en": "Learn Compound Inequalities",
            "question_ar": "تعلم المتباينات المركبة",
            "answer": "",
            "answer_ar": "",
            "show_full_solution": False,
            "hide_answer": False,
            "interactive_examples": [
                {
                    "title_en": "Example 1: Three-Part Inequality",
                    "title_ar": "المثال الأول: متباينة ثلاثية الأجزاء",
                    "problem_en": "1 ≤ 3x - 2 < 10",
                    "problem_ar": "١ ≤ ٣س - ٢ < ١٠",
                    "solution_en": "Step 1: Add 2 to all parts\n1 + 2 ≤ 3x - 2 + 2 < 10 + 2\n3 ≤ 3x < 12\nStep 2: Divide all parts by 3\n3 ÷ 3 ≤ 3x ÷ 3 < 12 ÷ 3\n1 ≤ x < 4",
                    "solution_ar": "الخطوة ١: أضف ٢ لجميع الأجزاء\n١ + ٢ ≤ ٣س - ٢ + ٢ < ١٠ + ٢\n٣ ≤ ٣س < ١٢\nالخطوة ٢: اقسم جميع الأجزاء على ٣\n٣ ÷ ٣ ≤ ٣س ÷ ٣ < ١٢ ÷ ٣\n١ ≤ س < ٤",
                    "practice_question_en": "Now try: 2 < x + 1 ≤ 5",
                    "practice_question_ar": "الآن جرب: ٢ < س + ١ ≤ ٥",
                    "practice_answer": "1 < x ≤ 4",
                    "practice_answer_ar": "١ < س ≤ ٤"
                },
                {
                    "title_en": "Example 2: With Negative Division",
                    "title_ar": "المثال الثاني: مع القسمة السالبة",
                    "problem_en": "0 ≤ -2x + 6 < 8",
                    "problem_ar": "٠ ≤ -٢س + ٦ < ٨",
                    "solution_en": "Step 1: Subtract 6 from all parts\n0 - 6 ≤ -2x + 6 - 6 < 8 - 6\n-6 ≤ -2x < 2\nStep 2: Divide by -2 (FLIP signs!)\n-6 ÷ (-2) ≥ -2x ÷ (-2) > 2 ÷ (-2)\n3 ≥ x > -1\nRewrite: -1 < x ≤ 3",
                    "solution_ar": "الخطوة ١: اطرح ٦ من جميع الأجزاء\n٠ - ٦ ≤ -٢س + ٦ - ٦ < ٨ - ٦\n-٦ ≤ -٢س < ٢\nالخطوة ٢: اقسم على -٢ (اقلب الإشارات!)\n-٦ ÷ (-٢) ≥ -٢س ÷ (-٢) > ٢ ÷ (-٢)\n٣ ≥ س > -١\nأعد الكتابة: -١ < س ≤ ٣",
                    "practice_question_en": "Now try: 4 ≤ -x + 2 < 7",
                    "practice_question_ar": "الآن جرب: ٤ ≤ -س + ٢ < ٧",
                    "practice_answer": "-5 < x ≤ -2",
                    "practice_answer_ar": "-٥ < س ≤ -٢"
                }
            ],
            "hints_en": [],
            "hints_ar": []
        },
        {
            "id": "practice5_1",
            "section_id": "section5",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "question_en": "-3 < 2x + 1 ≤ 7",
            "question_ar": "-٣ < ٢س + ١ ≤ ٧",
            "answer": "-2 < x ≤ 3",
            "answer_ar": "-٢ < س ≤ ٣",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Subtract 1 from all parts",
                    "step_ar": "اطرح ١ من جميع الأجزاء",
                    "possible_answers": [
                        "-4 < 2x ≤ 6"
                    ],
                    "possible_answers_ar": [
                        "-٤ < ٢س ≤ ٦"
                    ]
                },
                {
                    "step_en": "Divide all parts by 2",
                    "step_ar": "اقسم جميع الأجزاء على ٢",
                    "possible_answers": [
                        "-2 < x ≤ 3"
                    ],
                    "possible_answers_ar": [
                        "-٢ < س ≤ ٣"
                    ]
                }
            ],
            "hints_en": [
                "Perform the same operation on all three parts",
                "First eliminate the constant term",
                "Then eliminate the coefficient of x"
            ],
            "hints_ar": [
                "نفذ نفس العملية على الأجزاء الثلاثة",
                "أولاً احذف الحد الثابت",
                "ثم احذف معامل س"
            ]
        },
        {
            "id": "practice5_2",
            "section_id": "section5",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "question_en": "4 ≤ 3x - 2 < 10",
            "question_ar": "٤ ≤ ٣س - ٢ < ١٠",
            "answer": "2 ≤ x < 4",
            "answer_ar": "٢ ≤ س < ٤",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Add 2 to all parts",
                    "step_ar": "أضف ٢ لجميع الأجزاء",
                    "possible_answers": [
                        "6 ≤ 3x < 12"
                    ],
                    "possible_answers_ar": [
                        "٦ ≤ ٣س < ١٢"
                    ]
                },
                {
                    "step_en": "Divide all parts by 3",
                    "step_ar": "اقسم جميع الأجزاء على ٣",
                    "possible_answers": [
                        "2 ≤ x < 4"
                    ],
                    "possible_answers_ar": [
                        "٢ ≤ س < ٤"
                    ]
                }
            ],
            "hints_en": [
                "What operation cancels -2?",
                "Apply it to all three parts",
                "Then divide to isolate x"
            ],
            "hints_ar": [
                "ما العملية التي تلغي -٢؟",
                "طبقها على الأجزاء الثلاثة",
                "ثم اقسم لعزل س"
            ]
        },
        {
            "id": "assessment5",
            "section_id": "section5",
            "type": ProblemType.ASSESSMENT,
            "weight": 30,
            "question_en": "1 < 2x - 3 ≤ 9",
            "question_ar": "١ < ٢س - ٣ ≤ ٩",
            "answer": "2 < x ≤ 6",
            "answer_ar": "٢ < س ≤ ٦",
            "show_full_solution": False,
            "hide_answer": True,
            "hints_en": [
                "Work with all three parts of the compound inequality",
                "Add 3 to all parts first",
                "Then divide all parts by 2"
            ],
            "hints_ar": [
                "اعمل مع الأجزاء الثلاثة للمتباينة المركبة",
                "أضف ٣ لجميع الأجزاء أولاً",
                "ثم اقسم جميع الأجزاء على ٢"
            ]
        },
        {
            "id": "examprep5",
            "section_id": "section5",
            "type": ProblemType.EXAMPREP,
            "weight": 30,
            "question_en": "-5 ≤ -2x + 1 < 7",
            "question_ar": "-٥ ≤ -٢س + ١ < ٧",
            "answer": "-3 < x ≤ 3",
            "answer_ar": "-٣ < س ≤ ٣",
            "show_full_solution": False,
            "hide_answer": True,
            "hints_en": [
                "This involves dividing by a negative number",
                "Remember to flip all inequality signs when dividing by negative",
                "Work systematically with all parts"
            ],
            "hints_ar": [
                "هذا يتضمن القسمة على عدد سالب",
                "تذكر قلب جميع إشارات المتباينة عند القسمة على سالب",
                "اعمل بشكل منهجي مع جميع الأجزاء"
            ]
        }
    ]
    
    await problems_collection.insert_many(section5_problems)
    
    section5 = {
        "id": "section5",
        "title_en": "Section 5: Solving Inequalities Involving Absolute Value", 
        "title_ar": "القسم الخامس: حل المتباينات التي تتضمن القيمة المطلقة"
    }
    await sections_collection.insert_one(section5)
    
    print("Database initialized with all 5 sections")

# Student operations
async def create_student(username: str, class_name: str = "GR9-A") -> Student:
    student_data = {
        "username": username,
        "class_name": class_name,
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
async def get_all_students_stats(class_filter: str = None) -> List[Dict]:
    """Get comprehensive statistics for all students with optional class filtering"""
    query = {}
    if class_filter:
        query["class_name"] = class_filter
    students = await students_collection.find(query).to_list(None)
    stats = []
    
    for student in students:
        username = student["username"]
        progress_list = await progress_collection.find({"student_username": username}).to_list(None)
        
        # Calculate stats across all sections
        all_problems = await problems_collection.find({}).to_list(None)
        total_problems = len(all_problems)
        completed_problems = len([p for p in progress_list if p.get("completed", False)])
        progress_percentage = (completed_problems / total_problems) * 100 if total_problems > 0 else 0
        
        # Calculate weighted score across all sections
        total_score = 0
        total_weight = 0
        
        for problem in all_problems:
            progress_item = next((p for p in progress_list if p["problem_id"] == problem["id"]), None)
            if progress_item and progress_item.get("completed", False):
                total_score += (progress_item.get("score", 0) * problem["weight"]) / 100
                total_weight += problem["weight"]
        
        weighted_score = (total_score / total_weight) * 100 if total_weight > 0 else 0
        total_attempts = sum(p.get("attempts", 0) for p in progress_list)
        
        # Create problems status for all sections
        problems_status = {}
        for problem in all_problems:
            progress_item = next((p for p in progress_list if p["problem_id"] == problem["id"]), None)
            problems_status[problem["id"]] = {
                "completed": progress_item.get("completed", False) if progress_item else False,
                "score": progress_item.get("score", 0) if progress_item else 0,
                "attempts": progress_item.get("attempts", 0) if progress_item else 0
            }
        
        stats.append({
            "username": username,
            "class_name": student.get("class_name", "GR9-A"),  # Include class_name in response
            "progress_percentage": progress_percentage,
            "completed_problems": completed_problems,
            "total_problems": total_problems,
            "weighted_score": weighted_score,
            "total_attempts": total_attempts,
            "last_activity": student.get("last_login"),
            "problems_status": problems_status
        })
    
    return stats