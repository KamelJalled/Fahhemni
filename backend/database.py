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
            "type": ProblemType.EXPLANATION,
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
                    "step_en": "Write an inequality showing the additional amount 'm', added to the available amount '210' must be greater than or equal to '500'", 
                    "step_ar": "اكتب متباينة توضح أن المبلغ الإضافي 'م'، مضافًا إلى المبلغ المتاح '٢١٠' يجب أن يكون أكبر من أو يساوي '٥٠٠'",
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
    
    # Section 2: Solving Inequalities by Multiplication or Division
    section2_problems = [
        {
            "id": "prep2",
            "section_id": "section2",
            "type": ProblemType.PREPARATION,
            "weight": 10,
            "question_en": "4x < 20",
            "question_ar": "٤س < ٢٠",
            "answer": "x < 5",
            "answer_ar": "س < ٥",
            "explanation_en": "This is a review problem for solving inequalities by multiplication or division.",
            "explanation_ar": "هذه مسألة مراجعة لحل المتباينات بالضرب أو بالقسمة.",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Divide both sides by 4",
                    "step_ar": "الخطوة ١: اقسم كلا الطرفين على ٤",
                    "possible_answers": [
                        "4x / 4 < 20 / 4",
                        "x < 20 / 4"
                    ],
                    "possible_answers_ar": [
                        "٤س / ٤ < ٢٠ / ٤",
                        "س < ٢٠ / ٤"
                    ]
                },
                {
                    "step_en": "Step 2: Simplify the result",
                    "step_ar": "الخطوة ٢: بسّط النتيجة",
                    "possible_answers": [
                        "x < 5"
                    ],
                    "possible_answers_ar": [
                        "س < ٥"
                    ]
                }
            ],
            "final_answer_required": True,
            "hints_en": [
                "What operation cancels out multiplication by 4?",
                "Divide both sides by 4 to isolate x."
            ],
            "hints_ar": [
                "ما العملية التي تلغي الضرب في ٤؟",
                "اقسم كلا الطرفين على ٤ لعزل س."
            ]
        },
        {
            "id": "explanation2",
            "section_id": "section2",
            "type": ProblemType.EXPLANATION,
            "weight": 0,
            "question_en": "Learn Multiplication/Division Inequalities",
            "question_ar": "تعلم متباينات الضرب والقسمة",
            "answer": "",
            "answer_ar": "",
            "show_full_solution": False,
            "hide_answer": False,
            "explanation_en": "Learn to solve inequalities involving multiplication and division",
            "explanation_ar": "تعلم حل المتباينات التي تتضمن الضرب والقسمة",
            "interactive_examples": [
                {
                    "title_en": "Level 1: Simple (Positive Coefficient) - Example 1A (System Solved)",
                    "title_ar": "المستوى ١: بسيط (معامل موجب) - المثال ١أ (حل النظام)", 
                    "problem_en": "5x ≥ 30",
                    "problem_ar": "٥س ≥ ٣٠",
                    "solution_en": "Original inequality: 5x ≥ 30\n\nStep 1: Divide both sides by 5\n5x / 5 ≥ 30 / 5\nStep 2: Simplify\nx ≥ 6",
                    "solution_ar": "المتباينة الأصلية: ٥س ≥ ٣٠\n\nالخطوة ١: اقسم كلا الطرفين على ٥\n٥س / ٥ ≥ ٣٠ / ٥\nالخطوة ٢: بسّط\nس ≥ ٦",
                    "practice_question_en": "Now solve: 4x ≥ 20",
                    "practice_question_ar": "الآن حل: ٤س ≥ ٢٠",
                    "practice_answer": "x ≥ 5",
                    "practice_answer_ar": "س ≥ ٥"
                },
                {
                    "title_en": "Level 2: Medium (Negative Coefficient) - Example 2A (System Solved)",
                    "title_ar": "المستوى ٢: متوسط (معامل سالب) - المثال ٢أ (حل النظام)",
                    "problem_en": "-2p > 8",
                    "problem_ar": "-٢ف > ٨",
                    "solution_en": "Original inequality: -2p > 8\n\nStep 1: Divide both sides by -2 (flip sign)\n-2p / (-2) < 8 / (-2)\nStep 2: Simplify\np < -4",
                    "solution_ar": "المتباينة الأصلية: -٢ف > ٨\n\nالخطوة ١: اقسم كلا الطرفين على -٢ (اقلب الإشارة)\n-٢ف / (-٢) < ٨ / (-٢)\nالخطوة ٢: بسّط\nف < -٤",
                    "practice_question_en": "Now solve: -3m < 15", 
                    "practice_question_ar": "الآن حل: -٣م < ١٥",
                    "practice_answer": "m > -5",
                    "practice_answer_ar": "م > -٥"
                },
                {
                    "title_en": "Level 3: Advanced (Negative Division) - Example 3A (System Solved)",
                    "title_ar": "المستوى ٣: متقدم (القسمة السالبة) - المثال ٣أ (حل النظام)",
                    "problem_en": "-5w ≤ 25",
                    "problem_ar": "-٥و ≤ ٢٥",
                    "solution_en": "Original inequality: -5w ≤ 25\n\nStep 1: Divide both sides by -5 (flip sign)\n-5w / (-5) ≥ 25 / (-5)\nStep 2: Simplify\nw ≥ -5",
                    "solution_ar": "المتباينة الأصلية: -٥و ≤ ٢٥\n\nالخطوة ١: اقسم كلا الطرفين على -٥ (اقلب الإشارة)\n-٥و / (-٥) ≥ ٢٥ / (-٥)\nالخطوة ٢: بسّط\nو ≥ -٥",
                    "practice_question_en": "Now solve: -6k ≥ 30",
                    "practice_question_ar": "الآن حل: -٦ك ≥ ٣٠", 
                    "practice_answer": "k ≤ -5",
                    "practice_answer_ar": "ك ≤ -٥"
                }
            ],
            "step_solutions": [
                {
                    "step_en": "Level 1B Step 1: Divide both sides by 4",
                    "step_ar": "المستوى ١ب الخطوة ١: اقسم كلا الطرفين على ٤",
                    "possible_answers": [
                        "4x / 4 ≥ 20 / 4",
                        "x ≥ 20 / 4",
                        "4x/4 ≥ 20/4"
                    ],
                    "possible_answers_ar": [
                        "٤س / ٤ ≥ ٢٠ / ٤",
                        "س ≥ ٢٠ / ٤",
                        "٤س/٤ ≥ ٢٠/٤"
                    ]
                },
                {
                    "step_en": "Level 1B Step 2: Simplify",
                    "step_ar": "المستوى ١ب الخطوة ٢: بسّط",
                    "possible_answers": [
                        "x ≥ 5",
                        "س ≥ ٥"
                    ],
                    "possible_answers_ar": [
                        "س ≥ ٥",
                        "x ≥ 5"
                    ]
                },
                {
                    "step_en": "Level 2B Step 1: Divide both sides by -3 (flip the inequality sign)",
                    "step_ar": "المستوى ٢ب الخطوة ١: اقسم كلا الطرفين على -٣ (اقلب إشارة المتباينة)",
                    "possible_answers": [
                        "-3m / (-3) > 15 / (-3)",
                        "m > 15 / (-3)",
                        "-3m/(-3) > 15/(-3)",
                        "m > -5"
                    ],
                    "possible_answers_ar": [
                        "-٣م / (-٣) > ١٥ / (-٣)",
                        "م > ١٥ / (-٣)",
                        "-٣م/(-٣) > ١٥/(-٣)",
                        "م > -٥"
                    ]
                },
                {
                    "step_en": "Level 2B Step 2: Simplify",
                    "step_ar": "المستوى ٢ب الخطوة ٢: بسّط",
                    "possible_answers": [
                        "m > -5",
                        "م > -٥"
                    ],
                    "possible_answers_ar": [
                        "م > -٥",
                        "m > -5"
                    ]
                },
                {
                    "step_en": "Level 3B Step 1: Divide both sides by -6 (flip the inequality sign)",
                    "step_ar": "المستوى ٣ب الخطوة ١: اقسم كلا الطرفين على -٦ (اقلب إشارة المتباينة)",
                    "possible_answers": [
                        "-6k / (-6) ≤ 30 / (-6)",
                        "k ≤ 30 / (-6)",
                        "-6k/(-6) ≤ 30/(-6)",
                        "k ≤ -5"
                    ],
                    "possible_answers_ar": [
                        "-٦ك / (-٦) ≤ ٣٠ / (-٦)",
                        "ك ≤ ٣٠ / (-٦)",
                        "-٦ك/(-٦) ≤ ٣٠/(-٦)",
                        "ك ≤ -٥"
                    ]
                },
                {
                    "step_en": "Level 3B Step 2: Simplify",
                    "step_ar": "المستوى ٣ب الخطوة ٢: بسّط",
                    "possible_answers": [
                        "k ≤ -5",
                        "ك ≤ -٥"
                    ],
                    "possible_answers_ar": [
                        "ك ≤ -٥",
                        "k ≤ -5"
                    ]
                }
            ],
            "hints_en": [
                "To isolate x, what number should you divide both sides by?",
                "Now simplify both sides to get the final answer.",
                "What operation is needed to isolate m? Remember the sign flip rule!",
                "Simplify the arithmetic to get the final inequality.",
                "To isolate k, divide by -6. What happens to the inequality sign?",
                "Complete the simplification to get the final answer."
            ],
            "hints_ar": [
                "لعزل س، على أي رقم يجب أن تقسم الطرفين؟",
                "الآن بسّط الطرفين للحصول على الإجابة النهائية.",
                "ما العملية اللازمة لعزل م؟ تذكر قاعدة قلب الإشارة!",
                "بسّط العملية الحسابية للحصول على المتباينة النهائية.",
                "لعزل ك، اقسم على -٦. ماذا يحدث لإشارة المتباينة؟",
                "أكمل التبسيط للحصول على الإجابة النهائية."
            ]
        },
        {
            "id": "practice2_1",
            "section_id": "section2",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "question_en": "-2/3 k > 8",
            "question_ar": "-٢/٣ ك > ٨",
            "answer": "k < -12",
            "answer_ar": "ك < -١٢",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Multiply both sides by -3/2 and flip the inequality sign",
                    "step_ar": "اضرب كلا الطرفين في -٣/٢ واقلب إشارة المتباينة",
                    "possible_answers": [
                        "(-2/3) k * (-3/2) < 8 * (-3/2)",
                        "k < 8 * (-3/2)",
                        "k < -12"
                    ],
                    "possible_answers_ar": [
                        "(-٢/٣) ك * (-٣/٢) < ٨ * (-٣/٢)",
                        "ك < ٨ * (-٣/٢)",
                        "ك < -١٢"
                    ]
                },
                {
                    "step_en": "Flip the inequality sign",
                    "step_ar": "اقلب إشارة المتباينة",
                    "possible_answers": [
                        "k < -12"
                    ],
                    "possible_answers_ar": [
                        "ك < -١٢"
                    ]
                },
                {
                    "step_en": "Simplify 8 * (-3/2)",
                    "step_ar": "بسّط ٨ * (-٣/٢)",
                    "possible_answers": [
                        "k < -12"
                    ],
                    "possible_answers_ar": [
                        "ك < -١٢"
                    ]
                }
            ],
            "hints_en": [
                "To isolate k, multiply both sides by -3/2 (the reciprocal). Remember: when multiplying by a negative number, flip the inequality sign!",
                "When multiplying both sides by a negative number, what happens to the inequality sign?",
                "The rule: multiply by the reciprocal and flip the inequality sign when the multiplier is negative."
            ],
            "hints_ar": [
                "لعزل ك، اضرب كلا الطرفين في -٣/٢ (المقلوب). تذكر: عند الضرب في عدد سالب، اقلب إشارة المتباينة!",
                "عند ضرب كلا الطرفين في عدد سالب، ماذا يحدث لإشارة المتباينة؟",
                "القاعدة: اضرب في المقلوب واقلب إشارة المتباينة عندما يكون المضروب سالباً."
            ]
        },
        {
            "id": "practice2_2",
            "section_id": "section2",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "question_en": "Tickets must be sold at SAR 10 each to collect at least SAR 500. What is the minimum number of tickets (t) that must be sold?",
            "question_ar": "يجب بيع تذاكر بسعر ١٠ ريالات للتذكرة الواحدة لجمع ٥٠٠ ريال على الأقل. ما هو أقل عدد من التذاكر (ت) يجب بيعه؟",
            "answer": "t ≥ 50",
            "answer_ar": "ت ≥ ٥٠",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "Step 1: Write the inequality from the word problem",
                    "step_ar": "الخطوة ١: اكتب المتباينة من المسألة الكلامية",
                    "possible_answers": [
                        "10t ≥ 500",
                        "10 * t ≥ 500"
                    ],
                    "possible_answers_ar": [
                        "١٠ت ≥ ٥٠٠",
                        "١٠ * ت ≥ ٥٠٠"
                    ]
                },
                {
                    "step_en": "Step 2: Divide both sides by 10 (show the operation)",
                    "step_ar": "الخطوة ٢: اقسم كلا الطرفين على ١٠ (اظهر العملية)",
                    "possible_answers": [
                        "10t / 10 ≥ 500 / 10",
                        "t ≥ 500 / 10"
                    ],
                    "possible_answers_ar": [
                        "١٠ت / ١٠ ≥ ٥٠٠ / ١٠",
                        "ت ≥ ٥٠٠ / ١٠"
                    ]
                },
                {
                    "step_en": "Step 3: Simplify to final answer",
                    "step_ar": "الخطوة ٣: بسّط للحصول على الإجابة النهائية",
                    "possible_answers": [
                        "t ≥ 50"
                    ],
                    "possible_answers_ar": [
                        "ت ≥ ٥٠"
                    ]
                }
            ],
            "hints_en": [
                "Think about the variable: t represents number of tickets. What's the price per ticket? What amount needs to be collected?",
                "If you sell t tickets at 10 SAR each, how much will you collect? Does it need to be greater than or equal to 500?",
                "Amount collected = price per ticket × number of tickets. Use ≥ symbol because it says \"at least\""
            ],
            "hints_ar": [
                "فكر في المتغير: ت يمثل عدد التذاكر. ما هو سعر التذكرة الواحدة؟ وما المبلغ المطلوب جمعه؟",
                "إذا بعت ت تذكرة بسعر ١٠ ريال، كم ستجمع؟ هل تحتاج أن يكون المبلغ أكبر من أو يساوي ٥٠٠؟",
                "المبلغ المجموع = سعر التذكرة × عدد التذاكر. استخدم الرمز ≥ لأن المطلوب \"على الأقل\""
            ]
        },
        {
            "id": "assessment2",
            "section_id": "section2",
            "type": ProblemType.ASSESSMENT,
            "weight": 30,
            "question_en": "y / (-2) > 6",
            "question_ar": "ص / (-٢) > ٦",
            "answer": "y < -12",
            "answer_ar": "ص < -١٢",
            "show_full_solution": False,
            "hide_answer": True,
            "hints_en": [
                "When a variable is divided by a negative number, what operation isolates it?",
                "Pay attention to what happens to the inequality sign when you multiply by a negative.",
                "Focus on the process, not the specific numbers."
            ],
            "hints_ar": [
                "عندما يكون المتغير مقسوماً على عدد سالب، ما العملية التي تعزله؟",
                "انتبه لما يحدث لإشارة المتباينة عند الضرب في عدد سالب.",
                "ركز على العملية، وليس على الأرقام المحددة."
            ]
        },
        {
            "id": "examprep2",
            "section_id": "section2",
            "type": ProblemType.EXAMPREP,
            "weight": 30,
            "question_en": "You want to distribute at least 60 pieces of candy equally among 15 children. Write and solve an inequality to find the minimum number of pieces (p) each child can get.",
            "question_ar": "تريد توزيع ٦٠ قطعة حلوى على الأقل بالتساوي على ١٥ طفلاً. اكتب وحل متباينة لإيجاد أقل عدد من قطع الحلوى (ح) يمكن أن يحصل عليه كل طفل.",
            "answer": "p ≥ 4",
            "answer_ar": "ح ≥ ٤",
            "show_full_solution": False,
            "hide_answer": True,
            "step_solutions": [
                {
                    "step_en": "Step 1: Write the inequality from the word problem",
                    "step_ar": "الخطوة ١: اكتب المتباينة من المسألة الكلامية",
                    "possible_answers": [
                        "15p ≥ 60",
                        "15 * p ≥ 60"
                    ],
                    "possible_answers_ar": [
                        "١٥ح ≥ ٦٠",
                        "١٥ * ح ≥ ٦٠"
                    ]
                },
                {
                    "step_en": "Step 2: Divide both sides by 15 (show the operation)",
                    "step_ar": "الخطوة ٢: اقسم كلا الطرفين على ١٥ (اظهر العملية)",
                    "possible_answers": [
                        "15p / 15 ≥ 60 / 15",
                        "p ≥ 60 / 15"
                    ],
                    "possible_answers_ar": [
                        "١٥ح / ١٥ ≥ ٦٠ / ١٥",
                        "ح ≥ ٦٠ / ١٥"
                    ]
                },
                {
                    "step_en": "Step 3: Simplify to final answer",
                    "step_ar": "الخطوة ٣: بسّط للحصول على الإجابة النهائية",
                    "possible_answers": [
                        "p ≥ 4"
                    ],
                    "possible_answers_ar": [
                        "ح ≥ ٤"
                    ]
                }
            ],
            "hints_en": [
                "Variable p represents pieces per child. How many children? How many total pieces needed?",
                "If each child gets p pieces, and you have 15 children, how many pieces total will you distribute?",
                "Total = number of children × pieces per child. Must be \"at least\" 60"
            ],
            "hints_ar": [
                "المتغير ح يمثل عدد القطع لكل طفل. كم طفل لدينا؟ كم قطعة إجمالاً نحتاج؟",
                "إذا أعطيت كل طفل ح قطعة، و لديك ١٥ طفل، كم قطعة ستوزع إجمالاً؟",
                "العدد الإجمالي = عدد الأطفال × القطع لكل طفل. يجب أن يكون \"على الأقل\" ٦٠"
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
    
    # Section 3: Multi-Step Inequalities - COMPREHENSIVE UPDATE
    section3_problems = [
        {
            "id": "prep3",
            "section_id": "section3",
            "type": ProblemType.PREPARATION,
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
                "ما العملية التي تلغي +٥؟ / What operation cancels +5?",
                "اطرح ٥ أولاً، ثم اقسم على ٢ / Subtract 5 first, then divide by 2"
            ],
            "hints_ar": [
                "ما العملية التي تلغي +٥؟",
                "اطرح ٥ أولاً، ثم اقسم على ٢"
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
                    "title_en": "Level 1: Simple (بسيط) - Example 1A (System Demonstrates)",
                    "title_ar": "المستوى ١: بسيط - المثال ١أ (يظهر النظام)",
                    "problem_en": "Solve 3x + 4 > 16",
                    "problem_ar": "احل ٣س + ٤ > ١٦",
                    "solution_en": "Step 1: Subtract 4 from both sides: 3x + 4 - 4 > 16 - 4 → 3x > 12\nStep 2: Divide by 3: 3x/3 > 12/3 → x > 4",
                    "solution_ar": "الخطوة ١: اطرح ٤ من كلا الطرفين: ٣س + ٤ - ٤ > ١٦ - ٤ → ٣س > ١٢\nالخطوة ٢: اقسم على ٣: ٣س/٣ > ١٢/٣ → س > ٤"
                },
                {
                    "title_en": "Level 1: Simple (بسيط) - Example 1B (Student Solves - 2 STEPS REQUIRED)",
                    "title_ar": "المستوى ١: بسيط - المثال ١ب (يحل الطالب - مطلوب خطوتان)",
                    "problem_en": "Solve 2y + 5 ≤ 19",
                    "problem_ar": "احل ٢ص + ٥ ≤ ١٩",
                    "step_solutions": [
                        {
                            "step_en": "اطرح ٥ من كلا الطرفين / Subtract 5 from both sides",
                            "step_ar": "اطرح ٥ من كلا الطرفين",
                            "possible_answers": [
                                "2y ≤ 14",
                                "٢ص ≤ ١٤",
                                "2y + 5 - 5 ≤ 19 - 5"
                            ],
                            "possible_answers_ar": [
                                "٢ص ≤ ١٤",
                                "٢ص + ٥ - ٥ ≤ ١٩ - ٥"
                            ]
                        },
                        {
                            "step_en": "اقسم كلا الطرفين على ٢ / Divide both sides by 2",
                            "step_ar": "اقسم كلا الطرفين على ٢",
                            "possible_answers": [
                                "y ≤ 7",
                                "ص ≤ ٧",
                                "y ≤ 14/2"
                            ],
                            "possible_answers_ar": [
                                "ص ≤ ٧",
                                "ص ≤ ١٤/٢"
                            ]
                        }
                    ]
                },
                {
                    "title_en": "Level 2: Negative Coefficient (معامل سالب) - Example 2A (System Demonstrates)",
                    "title_ar": "المستوى ٢: معامل سالب - المثال ٢أ (يظهر النظام)",
                    "problem_en": "Solve 12 - 4m < 20",
                    "problem_ar": "احل ١٢ - ٤م < ٢٠",
                    "solution_en": "Step 1: Subtract 12: -4m < 8\nStep 2: Divide by -4 and FLIP SIGN: m > -2",
                    "solution_ar": "الخطوة ١: اطرح ١٢: -٤م < ٨\nالخطوة ٢: اقسم على -٤ واقلب الإشارة: م > -٢"
                },
                {
                    "title_en": "Level 2: Negative Coefficient (معامل سالب) - Example 2B (Student Solves - 2 STEPS REQUIRED)",
                    "title_ar": "المستوى ٢: معامل سالب - المثال ٢ب (يحل الطالب - مطلوب خطوتان)",
                    "problem_en": "Solve 15 - 5k ≥ -10",
                    "problem_ar": "احل ١٥ - ٥ك ≥ -١٠",
                    "step_solutions": [
                        {
                            "step_en": "اطرح ١٥ من كلا الطرفين / Subtract 15 from both sides",
                            "step_ar": "اطرح ١٥ من كلا الطرفين",
                            "possible_answers": [
                                "-5k ≥ -25",
                                "-٥ك ≥ -٢٥",
                                "15 - 5k - 15 ≥ -10 - 15"
                            ],
                            "possible_answers_ar": [
                                "-٥ك ≥ -٢٥",
                                "١٥ - ٥ك - ١٥ ≥ -١٠ - ١٥"
                            ]
                        },
                        {
                            "step_en": "اقسم على -٥ واقلب الإشارة / Divide by -5 and flip the sign",
                            "step_ar": "اقسم على -٥ واقلب الإشارة",
                            "possible_answers": [
                                "k ≤ 5",
                                "ك ≤ ٥"
                            ],
                            "possible_answers_ar": [
                                "ك ≤ ٥"
                            ]
                        }
                    ]
                },
                {
                    "title_en": "Level 3: Distributive Property (خاصية التوزيع) - Example 3A (System Demonstrates)",
                    "title_ar": "المستوى ٣: خاصية التوزيع - المثال ٣أ (يظهر النظام)",
                    "problem_en": "Solve 3(n + 2) ≤ 18",
                    "problem_ar": "احل ٣(ن + ٢) ≤ ١٨",
                    "solution_en": "Step 1: Distribute: 3n + 6 ≤ 18\nStep 2: Subtract 6: 3n ≤ 12\nStep 3: Divide by 3: n ≤ 4",
                    "solution_ar": "الخطوة ١: وزع: ٣ن + ٦ ≤ ١٨\nالخطوة ٢: اطرح ٦: ٣ن ≤ ١٢\nالخطوة ٣: اقسم على ٣: ن ≤ ٤"
                },
                {
                    "title_en": "Level 3: Distributive Property (خاصية التوزيع) - Example 3B (Student Solves - 3 STEPS REQUIRED)",
                    "title_ar": "المستوى ٣: خاصية التوزيع - المثال ٣ب (يحل الطالب - مطلوب ٣ خطوات)",
                    "problem_en": "Solve 4(r - 1) > 8",
                    "problem_ar": "احل ٤(ر - ١) > ٨",
                    "step_solutions": [
                        {
                            "step_en": "وزع الـ ٤ / Distribute the 4",
                            "step_ar": "وزع الـ ٤",
                            "possible_answers": [
                                "4r - 4 > 8",
                                "٤ر - ٤ > ٨"
                            ],
                            "possible_answers_ar": [
                                "٤ر - ٤ > ٨"
                            ]
                        },
                        {
                            "step_en": "أضف ٤ لكلا الطرفين / Add 4 to both sides",
                            "step_ar": "أضف ٤ لكلا الطرفين",
                            "possible_answers": [
                                "4r > 12",
                                "٤ر > ١٢"
                            ],
                            "possible_answers_ar": [
                                "٤ر > ١٢"
                            ]
                        },
                        {
                            "step_en": "اقسم على ٤ / Divide by 4",
                            "step_ar": "اقسم على ٤",
                            "possible_answers": [
                                "r > 3",
                                "ر > ٣"
                            ],
                            "possible_answers_ar": [
                                "ر > ٣"
                            ]
                        }
                    ]
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
            "question_en": "Solve the inequality 6 - 3y ≤ 18",
            "question_ar": "احل المتباينة ٦ - ٣ص ≤ ١٨",
            "answer": "y ≥ -4",
            "answer_ar": "ص ≥ -٤",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "اطرح ٦ من كلا الطرفين / Subtract 6 from both sides",
                    "step_ar": "اطرح ٦ من كلا الطرفين",
                    "possible_answers": [
                        "-3y ≤ 12",
                        "-٣ص ≤ ١٢"
                    ],
                    "possible_answers_ar": [
                        "-٣ص ≤ ١٢"
                    ]
                },
                {
                    "step_en": "اقسم على -٣ واقلب الإشارة / Divide by -3 and flip sign",
                    "step_ar": "اقسم على -٣ واقلب الإشارة",
                    "possible_answers": [
                        "y ≥ -4",
                        "ص ≥ -٤"
                    ],
                    "possible_answers_ar": [
                        "ص ≥ -٤"
                    ]
                }
            ],
            "final_answer_required": False,
            "hints_en": [
                "ابدأ بطرح ٦ من كلا الطرفين / Start by subtracting 6",
                "عزل الحد الذي يحتوي على المتغير / Isolate the term with variable",
                "٦ - ٦ - ٣ص ≤ ١٨ - ٦ / 6 - 6 - 3y ≤ 18 - 6"
            ],
            "hints_ar": [
                "ابدأ بطرح ٦ من كلا الطرفين",
                "عزل الحد الذي يحتوي على المتغير",
                "٦ - ٦ - ٣ص ≤ ١٨ - ٦"
            ]
        },
        {
            "id": "practice3_2",
            "section_id": "section3",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "stage_type": "practice_word",
            "question_en": "A car rental costs SAR 100 plus SAR 2 per kilometer (k). Your budget is SAR 250. What is the maximum distance you can drive?",
            "question_ar": "إيجار سيارة يكلف ١٠٠ ريال بالإضافة إلى ٢ ريال لكل كيلومتر. ميزانيتك ٢٥٠ ريال. ما أقصى مسافة يمكنك قيادتها؟",
            "answer": "k ≤ 75",
            "answer_ar": "ك ≤ ٧٥",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "اكتب المتباينة / Write the inequality",
                    "step_ar": "اكتب المتباينة",
                    "possible_answers": [
                        "100 + 2k ≤ 250",
                        "١٠٠ + ٢ك ≤ ٢٥٠",
                        "2k + 100 ≤ 250"
                    ],
                    "possible_answers_ar": [
                        "١٠٠ + ٢ك ≤ ٢٥٠",
                        "٢ك + ١٠٠ ≤ ٢٥٠"
                    ]
                },
                {
                    "step_en": "اطرح التكلفة الثابتة / Subtract the fixed cost",
                    "step_ar": "اطرح التكلفة الثابتة",
                    "possible_answers": [
                        "2k ≤ 150",
                        "٢ك ≤ ١٥٠"
                    ],
                    "possible_answers_ar": [
                        "٢ك ≤ ١٥٠"
                    ]
                },
                {
                    "step_en": "احسب الحد الأقصى للكيلومترات / Calculate maximum kilometers",
                    "step_ar": "احسب الحد الأقصى للكيلومترات",
                    "possible_answers": [
                        "k ≤ 75",
                        "ك ≤ ٧٥"
                    ],
                    "possible_answers_ar": [
                        "ك ≤ ٧٥"
                    ]
                }
            ],
            "final_answer_required": False,
            "hints_en": [
                "التكلفة الإجمالية = التكلفة الثابتة + (تكلفة الكيلومتر × عدد الكيلومترات) / Total = Fixed + (Per km × Number)",
                "استخدم k للكيلومترات / Use k for kilometers",
                "التكلفة يجب أن تكون ≤ الميزانية / Cost must be ≤ budget"
            ],
            "hints_ar": [
                "التكلفة الإجمالية = التكلفة الثابتة + (تكلفة الكيلومتر × عدد الكيلومترات)",
                "استخدم k للكيلومترات",
                "التكلفة يجب أن تكون ≤ الميزانية"
            ]
        },
        {
            "id": "assessment3",
            "section_id": "section3",
            "type": ProblemType.ASSESSMENT,
            "weight": 20,
            "question_en": "What is the solution set for the inequality: (x + 3) / 2 ≤ 5?",
            "question_ar": "ما هي مجموعة حل المتباينة: (س + ٣) / ٢ ≤ ٥؟",
            "answer": "x ≤ 7",
            "answer_ar": "س ≤ ٧",
            "show_full_solution": False,
            "hide_answer": True,
            "explanation_en": "Multiply both sides by 2, then subtract 3",
            "explanation_ar": "اضرب كلا الطرفين في ٢، ثم اطرح ٣",
            "final_answer_required": True,
            "hints_en": [
                "اضرب كلا الطرفين في ٢ أولاً / Multiply both sides by 2 first",
                "بعد الضرب في ٢، اطرح ٣ / After multiplying by 2, subtract 3"
            ],
            "hints_ar": [
                "اضرب كلا الطرفين في ٢ أولاً",
                "بعد الضرب في ٢، اطرح ٣"
            ]
        },
        {
            "id": "examprep3",
            "section_id": "section3",
            "type": ProblemType.EXAM_PREP,
            "weight": 25,
            "question_en": "Solve the inequality: 3(1 - k) < 12",
            "question_ar": "حل المتباينة: ٣(١ - ك) < ١٢",
            "answer": "k > -3",
            "answer_ar": "ك > -٣",
            "show_full_solution": False,
            "hide_answer": True,
            "explanation_en": "Distribute 3, subtract 3, then divide by -3 (flip sign)",
            "explanation_ar": "وزع ٣، اطرح ٣، ثم اقسم على -٣ (اقلب الإشارة)",
            "final_answer_required": True,
            "hints_en": [],
            "hints_ar": []
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