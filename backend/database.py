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
                    "title_en": "Level 1: Simple - Example 1A (System Demonstrates)",
                    "title_ar": "المستوى ١: بسيط - المثال ١أ (يظهر النظام)",
                    "problem_en": "Solve 3x + 4 > 16",
                    "problem_ar": "احل ٣س + ٤ > ١٦",
                    "solution_en": "Step 1: Subtract 4 from both sides: 3x + 4 - 4 > 16 - 4 → 3x > 12\nStep 2: Divide by 3: 3x/3 > 12/3 → x > 4",
                    "solution_ar": "الخطوة ١: اطرح ٤ من كلا الطرفين: ٣س + ٤ - ٤ > ١٦ - ٤ → ٣س > ١٢\nالخطوة ٢: اقسم على ٣: ٣س/٣ > ١٢/٣ → س > ٤",
                    "practice_question_en": "Now solve: 2y + 5 ≤ 19",
                    "practice_question_ar": "الآن احل: ٢ص + ٥ ≤ ١٩",
                    "practice_answer": "y ≤ 7",
                    "practice_answer_ar": "ص ≤ ٧"
                },
                {
                    "title_en": "Level 2: Negative Coefficient - Example 2A (System Demonstrates)",
                    "title_ar": "المستوى ٢: معامل سالب - المثال ٢أ (يظهر النظام)",
                    "problem_en": "Solve 12 - 4m < 20",
                    "problem_ar": "احل ١٢ - ٤م < ٢٠",
                    "solution_en": "Step 1: Subtract 12: -4m < 8\nStep 2: Divide by -4 and FLIP SIGN: m > -2",
                    "solution_ar": "الخطوة ١: اطرح ١٢: -٤م < ٨\nالخطوة ٢: اقسم على -٤ واقلب الإشارة: م > -٢",
                    "practice_question_en": "Now solve: 15 - 5k ≥ -10",
                    "practice_question_ar": "الآن احل: ١٥ - ٥ك ≥ -١٠",
                    "practice_answer": "k ≤ 5",
                    "practice_answer_ar": "ك ≤ ٥"
                },
                {
                    "title_en": "Level 3: Distributive Property - Example 3A (System Demonstrates)",
                    "title_ar": "المستوى ٣: خاصية التوزيع - المثال ٣أ (يظهر النظام)",
                    "problem_en": "Solve 3(n + 2) ≤ 18",
                    "problem_ar": "احل ٣(ن + ٢) ≤ ١٨",
                    "solution_en": "Step 1: Distribute: 3n + 6 ≤ 18\nStep 2: Subtract 6: 3n ≤ 12\nStep 3: Divide by 3: n ≤ 4",
                    "solution_ar": "الخطوة ١: وزع: ٣ن + ٦ ≤ ١٨\nالخطوة ٢: اطرح ٦: ٣ن ≤ ١٢\nالخطوة ٣: اقسم على ٣: ن ≤ ٤",
                    "practice_question_en": "Now solve: 4(r - 1) > 8",
                    "practice_question_ar": "الآن احل: ٤(ر - ١) > ٨",
                    "practice_answer": "r > 3",
                    "practice_answer_ar": "ر > ٣"
                }
            ],
            "step_solutions": [
                {
                    "step_en": "Level 1B Step 1: Subtract 5 from both sides",
                    "step_ar": "المستوى ١ب الخطوة ١: اطرح ٥ من كلا الطرفين",
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
                    "step_en": "Level 1B Step 2: Divide both sides by 2",
                    "step_ar": "المستوى ١ب الخطوة ٢: اقسم كلا الطرفين على ٢",
                    "possible_answers": [
                        "y ≤ 7",
                        "ص ≤ ٧",
                        "y ≤ 14/2"
                    ],
                    "possible_answers_ar": [
                        "ص ≤ ٧",
                        "ص ≤ ١٤/٢"
                    ]
                },
                {
                    "step_en": "Level 2B Step 1: Subtract 15 from both sides",
                    "step_ar": "المستوى ٢ب الخطوة ١: اطرح ١٥ من كلا الطرفين",
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
                    "step_en": "Level 2B Step 2: Divide by -5 and flip the inequality sign",
                    "step_ar": "المستوى ٢ب الخطوة ٢: اقسم على -٥ واقلب إشارة المتباينة",
                    "possible_answers": [
                        "k ≤ 5",
                        "ك ≤ ٥"
                    ],
                    "possible_answers_ar": [
                        "ك ≤ ٥"
                    ]
                },
                {
                    "step_en": "Level 3B Step 1: Distribute the 4",
                    "step_ar": "المستوى ٣ب الخطوة ١: وزع الـ ٤",
                    "possible_answers": [
                        "4r - 4 > 8",
                        "٤ر - ٤ > ٨"
                    ],
                    "possible_answers_ar": [
                        "٤ر - ٤ > ٨"
                    ]
                },
                {
                    "step_en": "Level 3B Step 2: Add 4 to both sides",
                    "step_ar": "المستوى ٣ب الخطوة ٢: أضف ٤ لكلا الطرفين",
                    "possible_answers": [
                        "4r > 12",
                        "٤ر > ١٢"
                    ],
                    "possible_answers_ar": [
                        "٤ر > ١٢"
                    ]
                },
                {
                    "step_en": "Level 3B Step 3: Divide by 4",
                    "step_ar": "المستوى ٣ب الخطوة ٣: اقسم على ٤",
                    "possible_answers": [
                        "r > 3",
                        "ر > ٣"
                    ],
                    "possible_answers_ar": [
                        "ر > ٣"
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
            "type": ProblemType.EXAMPREP,
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
    
    # Section 4: Compound Inequalities - COMPREHENSIVE UPDATE
    section4_problems = [
        {
            "id": "prep4",
            "section_id": "section4",
            "type": ProblemType.PREPARATION,
            "weight": 10,
            "question_en": "Solve: 3 < x + 2 < 8",
            "question_ar": "حل: ٣ < س + ٢ < ٨",
            "answer": "1 < x < 6",
            "answer_ar": "١ < س < ٦",
            "explanation_en": "This is a compound inequality. Apply operations to all parts simultaneously.",
            "explanation_ar": "هذه متباينة مركبة. طبق العمليات على جميع الأجزاء في نفس الوقت.",
            "show_full_solution": False,
            "hide_answer": False,
            "final_answer_required": True,
            "hints_en": [
                "اطرح ٢ من جميع الأجزاء / Subtract 2 from all parts",
                "٣ - ٢ < س + ٢ - ٢ < ٨ - ٢ / 3 - 2 < x + 2 - 2 < 8 - 2"
            ],
            "hints_ar": [
                "اطرح ٢ من جميع الأجزاء",
                "٣ - ٢ < س + ٢ - ٢ < ٨ - ٢"
            ]
        },
        {
            "id": "explanation4",
            "section_id": "section4",
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
                    "title_en": "Level 1: Simple Compound - Example 1A (System Demonstrates)",
                    "title_ar": "المستوى ١: مركب بسيط - المثال ١أ (يظهر النظام)",
                    "problem_en": "Solve 5 < m + 1 < 9",
                    "problem_ar": "احل ٥ < م + ١ < ٩",
                    "solution_en": "Step 1: Subtract 1 from all parts: 5 - 1 < m + 1 - 1 < 9 - 1\nResult: 4 < m < 8",
                    "solution_ar": "الخطوة ١: اطرح ١ من جميع الأجزاء: ٥ - ١ < م + ١ - ١ < ٩ - ١\nالنتيجة: ٤ < م < ٨",
                    "practice_question_en": "Now solve: -2 ≤ y - 3 ≤ 4",
                    "practice_question_ar": "الآن احل: -٢ ≤ ص - ٣ ≤ ٤",
                    "practice_answer": "1 ≤ y ≤ 7",
                    "practice_answer_ar": "١ ≤ ص ≤ ٧"
                },
                {
                    "title_en": "Level 2: With Multiplication/Division - Example 2A (System Demonstrates)",
                    "title_ar": "المستوى ٢: مع الضرب والقسمة - المثال ٢أ (يظهر النظام)",
                    "problem_en": "Solve -6 < 2k < 10",
                    "problem_ar": "احل -٦ < ٢ك < ١٠",
                    "solution_en": "Divide all parts by 2: -6/2 < 2k/2 < 10/2\nResult: -3 < k < 5",
                    "solution_ar": "اقسم جميع الأجزاء على ٢: -٦/٢ < ٢ك/٢ < ١٠/٢\nالنتيجة: -٣ < ك < ٥",
                    "practice_question_en": "Now solve: -12 ≤ -3n ≤ 6",
                    "practice_question_ar": "الآن احل: -١٢ ≤ -٣ن ≤ ٦",
                    "practice_answer": "-2 ≤ n ≤ 4",
                    "practice_answer_ar": "-٢ ≤ ن ≤ ٤"
                },
                {
                    "title_en": "Level 3: OR Inequalities - Example 3A (System Demonstrates)",
                    "title_ar": "المستوى ٣: متباينات أو - المثال ٣أ (يظهر النظام)",
                    "problem_en": "Solve x < -1 or x > 3",
                    "problem_ar": "احل س < -١ أو س > ٣",
                    "solution_en": "This is a disjoint inequality - two separate ranges\nSolution remains: x < -1 or x > 3",
                    "solution_ar": "هذه متباينة منفصلة - مداان منفصلان\nالحل يبقى: س < -١ أو س > ٣",
                    "practice_question_en": "Now solve: 2t ≤ -4 or t + 1 > 5",
                    "practice_question_ar": "الآن احل: ٢ت ≤ -٤ أو ت + ١ > ٥",
                    "practice_answer": "t ≤ -2 or t > 4",
                    "practice_answer_ar": "ت ≤ -٢ أو ت > ٤"
                }
            ],
            "step_solutions": [
                {
                    "step_en": "Level 1B Step 1: Add 3 to all parts",
                    "step_ar": "المستوى ١ب الخطوة ١: أضف ٣ لجميع الأجزاء",
                    "possible_answers": [
                        "1 ≤ y ≤ 7",
                        "١ ≤ ص ≤ ٧",
                        "-2+3 ≤ y-3+3 ≤ 4+3",
                        "-2 + 3 ≤ y ≤ 4 + 3"
                    ],
                    "possible_answers_ar": [
                        "١ ≤ ص ≤ ٧",
                        "-٢+٣ ≤ ص-٣+٣ ≤ ٤+٣"
                    ]
                },
                {
                    "step_en": "Level 1B Step 2: Simplify",
                    "step_ar": "المستوى ١ب الخطوة ٢: بسّط",
                    "possible_answers": [
                        "1 ≤ y ≤ 7",
                        "١ ≤ ص ≤ ٧"
                    ],
                    "possible_answers_ar": [
                        "١ ≤ ص ≤ ٧"
                    ]
                },
                {
                    "step_en": "Level 2B Step 1: Divide by -3 and flip ALL signs",
                    "step_ar": "المستوى ٢ب الخطوة ١: اقسم على -٣ واقلب جميع الإشارات",
                    "possible_answers": [
                        "4 ≥ n ≥ -2",
                        "-2 ≤ n ≤ 4",
                        "-٢ ≤ ن ≤ ٤"
                    ],
                    "possible_answers_ar": [
                        "٤ ≥ ن ≥ -٢",
                        "-٢ ≤ ن ≤ ٤"
                    ]
                },
                {
                    "step_en": "Level 2B Step 2: Rewrite in standard form (smallest to largest)",
                    "step_ar": "المستوى ٢ب الخطوة ٢: اكتب بالترتيب من الأصغر للأكبر",
                    "possible_answers": [
                        "-2 ≤ n ≤ 4",
                        "-٢ ≤ ن ≤ ٤"
                    ],
                    "possible_answers_ar": [
                        "-٢ ≤ ن ≤ ٤"
                    ]
                },
                {
                    "step_en": "Level 3B Step 1: Solve each inequality separately",
                    "step_ar": "المستوى ٣ب الخطوة ١: حل كل متباينة منفصلة",
                    "possible_answers": [
                        "t ≤ -2 or t > 4",
                        "ت ≤ -٢ أو ت > ٤",
                        "t <= -2 or t > 4",
                        "t ≤ -2 || t > 4"
                    ],
                    "possible_answers_ar": [
                        "ت ≤ -٢ أو ت > ٤"
                    ]
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
            "question_en": "Solve -5 < 3x + 1 < 13",
            "question_ar": "احل -٥ < ٣س + ١ < ١٣",
            "answer": "-2 < x < 4",
            "answer_ar": "-٢ < س < ٤",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "اطرح ١ من جميع الأجزاء / Subtract 1 from all parts",
                    "step_ar": "اطرح ١ من جميع الأجزاء",
                    "possible_answers": [
                        "-6 < 3x < 12",
                        "-٦ < ٣س < ١٢"
                    ],
                    "possible_answers_ar": [
                        "-٦ < ٣س < ١٢"
                    ]
                },
                {
                    "step_en": "اقسم جميع الأجزاء على ٣ / Divide all parts by 3",
                    "step_ar": "اقسم جميع الأجزاء على ٣",
                    "possible_answers": [
                        "-2 < x < 4",
                        "-٢ < س < ٤"
                    ],
                    "possible_answers_ar": [
                        "-٢ < س < ٤"
                    ]
                }
            ],
            "final_answer_required": False,
            "hints_en": [
                "ابدأ بطرح ١ من جميع الأجزاء الثلاثة / Start by subtracting 1 from all three parts",
                "تخلص من الثابت أولاً / Remove the constant first",
                "-٥ - ١ < ٣س < ١٣ - ١ / -5 - 1 < 3x < 13 - 1"
            ],
            "hints_ar": [
                "ابدأ بطرح ١ من جميع الأجزاء الثلاثة",
                "تخلص من الثابت أولاً",
                "-٥ - ١ < ٣س < ١٣ - ١"
            ]
        },
        {
            "id": "practice4_2",
            "section_id": "section4",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "stage_type": "practice_word",
            "question_en": "Room temperature must be between 18°C and 25°C. If F = (9/5)C + 32 converts Celsius to Fahrenheit, what's the range in Fahrenheit?",
            "question_ar": "درجة حرارة الغرفة يجب أن تكون بين ١٨ و٢٥ درجة مئوية. إذا كانت الصيغة ف = (٩/٥)م + ٣٢ تحول من مئوية إلى فهرنهايت، ما المدى بالفهرنهايت؟",
            "answer": "64.4 ≤ F ≤ 77",
            "answer_ar": "٦٤.٤ ≤ ف ≤ ٧٧",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "اكتب المدى بالدرجة المئوية / Write the Celsius range",
                    "step_ar": "اكتب المدى بالدرجة المئوية",
                    "possible_answers": [
                        "18 ≤ C ≤ 25",
                        "١٨ ≤ م ≤ ٢٥"
                    ],
                    "possible_answers_ar": [
                        "١٨ ≤ م ≤ ٢٥"
                    ]
                },
                {
                    "step_en": "طبق الصيغة على جميع الأجزاء / Apply formula to all parts",
                    "step_ar": "طبق الصيغة على جميع الأجزاء",
                    "possible_answers": [
                        "(9/5)(18) + 32 ≤ F ≤ (9/5)(25) + 32",
                        "32.4 + 32 ≤ F ≤ 45 + 32"
                    ],
                    "possible_answers_ar": [
                        "(٩/٥)(١٨) + ٣٢ ≤ ف ≤ (٩/٥)(٢٥) + ٣٢"
                    ]
                },
                {
                    "step_en": "احسب القيم النهائية / Calculate final values",
                    "step_ar": "احسب القيم النهائية",
                    "possible_answers": [
                        "64.4 ≤ F ≤ 77",
                        "64 ≤ F ≤ 77",
                        "٦٤.٤ ≤ ف ≤ ٧٧"
                    ],
                    "possible_answers_ar": [
                        "٦٤.٤ ≤ ف ≤ ٧٧",
                        "٦٤ ≤ ف ≤ ٧٧"
                    ]
                }
            ],
            "final_answer_required": False,
            "hints_en": [
                "درجة الحرارة يجب أن تكون بين ١٨ و٢٥ / Temperature must be between 18 and 25",
                "استخدم C أو م للدرجة المئوية / Use C for Celsius",
                "المدى: ١٨ ≤ م ≤ ٢٥ / Range: 18 ≤ C ≤ 25"
            ],
            "hints_ar": [
                "درجة الحرارة يجب أن تكون بين ١٨ و٢٥",
                "استخدم C أو م للدرجة المئوية",
                "المدى: ١٨ ≤ م ≤ ٢٥"
            ]
        },
        {
            "id": "assessment4",
            "section_id": "section4",
            "type": ProblemType.ASSESSMENT,
            "weight": 20,
            "question_en": "What is the solution to -8 ≤ 4 - 2x < 6?",
            "question_ar": "ما هو حل -٨ ≤ ٤ - ٢س < ٦؟",
            "answer": "-1 < x ≤ 6",
            "answer_ar": "-١ < س ≤ ٦",
            "show_full_solution": False,
            "hide_answer": True,
            "explanation_en": "Subtract 4 from all parts, then divide by -2 and flip signs",
            "explanation_ar": "اطرح ٤ من جميع الأجزاء، ثم اقسم على -٢ واقلب الإشارات",
            "final_answer_required": True,
            "hints_en": [
                "اطرح ٤ من جميع الأجزاء أولاً / Subtract 4 from all parts first",
                "تذكر قلب الإشارات عند القسمة على -٢ / Remember to flip signs when dividing by -2"
            ],
            "hints_ar": [
                "اطرح ٤ من جميع الأجزاء أولاً",
                "تذكر قلب الإشارات عند القسمة على -٢"
            ]
        },
        {
            "id": "examprep4",
            "section_id": "section4",
            "type": ProblemType.EXAMPREP,
            "weight": 25,
            "question_en": "Solve: 2(x - 1) ≤ 6 AND x + 3 > 2",
            "question_ar": "حل: ٢(س - ١) ≤ ٦ و س + ٣ > ٢",
            "answer": "-1 < x ≤ 4",
            "answer_ar": "-١ < س ≤ ٤",
            "show_full_solution": False,
            "hide_answer": True,
            "explanation_en": "Solve both inequalities separately, then find the intersection",
            "explanation_ar": "احل كل متباينة منفصلة، ثم جد التقاطع",
            "final_answer_required": True,
            "hints_en": [],
            "hints_ar": []
        }
    ]
    
    await problems_collection.insert_many(section4_problems)
    
    section4 = {
        "id": "section4", 
        "title_en": "Section 4: Solving Compound Inequalities", 
        "title_ar": "القسم الرابع: حل المتباينات المركبة"
    }
    await sections_collection.insert_one(section4)
    
    # Section 5: Absolute Value Inequalities - COMPREHENSIVE UPDATE
    section5_problems = [
        {
            "id": "prep5",
            "section_id": "section5",
            "type": ProblemType.PREPARATION,
            "weight": 10,
            "question_en": "Solve: |x| < 4",
            "question_ar": "حل: |س| < ٤",
            "answer": "-4 < x < 4",
            "answer_ar": "-٤ < س < ٤",
            "explanation_en": "Absolute value less than a positive number creates a compound inequality.",
            "explanation_ar": "القيمة المطلقة أقل من عدد موجب تنتج متباينة مركبة.",
            "show_full_solution": False,
            "hide_answer": False,
            "final_answer_required": True,
            "hints_en": [
                "القيمة المطلقة أقل من ٤ تعني المسافة من الصفر أقل من ٤ / Absolute value less than 4 means distance from zero less than 4",
                "الحل بين -٤ و ٤ / Solution is between -4 and 4"
            ],
            "hints_ar": [
                "القيمة المطلقة أقل من ٤ تعني المسافة من الصفر أقل من ٤",
                "الحل بين -٤ و ٤"
            ]
        },
        {
            "id": "explanation5",
            "section_id": "section5",
            "type": ProblemType.EXPLANATION,
            "weight": 0,
            "question_en": "Learn Absolute Value Inequalities",
            "question_ar": "تعلم متباينات القيمة المطلقة",
            "answer": "",
            "answer_ar": "",
            "show_full_solution": False,
            "hide_answer": False,
            "interactive_examples": [
                {
                    "title_en": "Level 1: Simple Absolute Value - Example 1A (System Demonstrates)",
                    "title_ar": "المستوى ١: قيمة مطلقة بسيطة - المثال ١أ (يظهر النظام)",
                    "problem_en": "Solve |m| ≤ 6",
                    "problem_ar": "احل |م| ≤ ٦",
                    "solution_en": "Absolute value ≤ positive means compound inequality\nConvert to: -6 ≤ m ≤ 6\nSolution: -6 ≤ m ≤ 6",
                    "solution_ar": "القيمة المطلقة ≤ موجب تعني متباينة مركبة\nحول إلى: -٦ ≤ م ≤ ٦\nالحل: -٦ ≤ م ≤ ٦",
                    "practice_question_en": "Now solve: |y| < 3",
                    "practice_question_ar": "الآن احل: |ص| < ٣",
                    "practice_answer": "-3 < y < 3",
                    "practice_answer_ar": "-٣ < ص < ٣"
                },
                {
                    "title_en": "Level 2: Absolute Value Greater Than - Example 2A (System Demonstrates)",
                    "title_ar": "المستوى ٢: القيمة المطلقة أكبر من - المثال ٢أ (يظهر النظام)",
                    "problem_en": "Solve |k| > 5",
                    "problem_ar": "احل |ك| > ٥",
                    "solution_en": "Absolute value > positive means OR inequality\nConvert to: k < -5 or k > 5\nTwo separate ranges, not connected",
                    "solution_ar": "القيمة المطلقة > موجب تعني متباينة أو\nحول إلى: ك < -٥ أو ك > ٥\nمداان منفصلان، غير متصلان",
                    "practice_question_en": "Now solve: |n| ≥ 2",
                    "practice_question_ar": "الآن احل: |ن| ≥ ٢",
                    "practice_answer": "n ≤ -2 or n ≥ 2",
                    "practice_answer_ar": "ن ≤ -٢ أو ن ≥ ٢"
                },
                {
                    "title_en": "Level 3: Complex Absolute Value - Example 3A (System Demonstrates)",
                    "title_ar": "المستوى ٣: قيمة مطلقة معقدة - المثال ٣أ (يظهر النظام)",
                    "problem_en": "Solve |2x - 3| < 7",
                    "problem_ar": "احل |٢س - ٣| < ٧",
                    "solution_en": "Step 1: Convert to compound: -7 < 2x - 3 < 7\nStep 2: Add 3 to all parts: -4 < 2x < 10\nStep 3: Divide by 2: -2 < x < 5",
                    "solution_ar": "الخطوة ١: حول إلى مركبة: -٧ < ٢س - ٣ < ٧\nالخطوة ٢: أضف ٣ لجميع الأجزاء: -٤ < ٢س < ١٠\nالخطوة ٣: اقسم على ٢: -٢ < س < ٥",
                    "practice_question_en": "Now solve: |x + 4| ≤ 6",
                    "practice_question_ar": "الآن احل: |س + ٤| ≤ ٦",
                    "practice_answer": "-10 ≤ x ≤ 2",
                    "practice_answer_ar": "-١٠ ≤ س ≤ ٢"
                }
            ],
            "step_solutions": [
                {
                    "step_en": "Level 1B Step 1: Convert to compound inequality",
                    "step_ar": "المستوى ١ب الخطوة ١: حول إلى متباينة مركبة",
                    "possible_answers": [
                        "-3 < y < 3",
                        "-٣ < ص < ٣",
                        "y > -3 and y < 3"
                    ],
                    "possible_answers_ar": [
                        "-٣ < ص < ٣",
                        "ص > -٣ و ص < ٣"
                    ]
                },
                {
                    "step_en": "Level 2B Step 1: Convert to OR inequality",
                    "step_ar": "المستوى ٢ب الخطوة ١: حول إلى متباينة منفصلة",
                    "possible_answers": [
                        "n ≤ -2 or n ≥ 2",
                        "ن ≤ -٢ أو ن ≥ ٢",
                        "n <= -2 or n >= 2",
                        "n ≤ -2 || n ≥ 2"
                    ],
                    "possible_answers_ar": [
                        "ن ≤ -٢ أو ن ≥ ٢"
                    ]
                },
                {
                    "step_en": "Level 3B Step 1: Convert to compound inequality",
                    "step_ar": "المستوى ٣ب الخطوة ١: حول إلى متباينة مركبة",
                    "possible_answers": [
                        "-6 ≤ x + 4 ≤ 6",
                        "-٦ ≤ س + ٤ ≤ ٦"
                    ],
                    "possible_answers_ar": [
                        "-٦ ≤ س + ٤ ≤ ٦"
                    ]
                },
                {
                    "step_en": "Level 3B Step 2: Subtract 4 from all parts",
                    "step_ar": "المستوى ٣ب الخطوة ٢: اطرح ٤ من جميع الأجزاء",
                    "possible_answers": [
                        "-10 ≤ x ≤ 2",
                        "-١٠ ≤ س ≤ ٢"
                    ],
                    "possible_answers_ar": [
                        "-١٠ ≤ س ≤ ٢"
                    ]
                },
                {
                    "step_en": "Level 3B Step 3: Write final answer",
                    "step_ar": "المستوى ٣ب الخطوة ٣: اكتب الإجابة النهائية",
                    "possible_answers": [
                        "-10 ≤ x ≤ 2",
                        "-١٠ ≤ س ≤ ٢"
                    ],
                    "possible_answers_ar": [
                        "-١٠ ≤ س ≤ ٢"
                    ]
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
            "question_en": "Solve |3y - 2| > 8",
            "question_ar": "احل |٣ص - ٢| > ٨",
            "answer": "y < -2 or y > 10/3",
            "answer_ar": "ص < -٢ أو ص > ١٠/٣",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "حول إلى متباينة منفصلة / Convert to OR inequality",
                    "step_ar": "حول إلى متباينة منفصلة",
                    "possible_answers": [
                        "3y - 2 < -8 or 3y - 2 > 8",
                        "3y - 2 < -8 || 3y - 2 > 8",
                        "٣ص - ٢ < -٨ أو ٣ص - ٢ > ٨"
                    ],
                    "possible_answers_ar": [
                        "٣ص - ٢ < -٨ أو ٣ص - ٢ > ٨"
                    ]
                },
                {
                    "step_en": "حل كل متباينة منفصلة / Solve each inequality separately",
                    "step_ar": "حل كل متباينة منفصلة",
                    "possible_answers": [
                        "y < -2 or y > 10/3",
                        "y < -2 or y > 3.33",
                        "ص < -٢ أو ص > ١٠/٣"
                    ],
                    "possible_answers_ar": [
                        "ص < -٢ أو ص > ١٠/٣"
                    ]
                }
            ],
            "final_answer_required": False,
            "hints_en": [
                "القيمة المطلقة > ٨ تعني حالتين منفصلتين / Absolute value > 8 means two separate cases",
                "إما أقل من -٨ أو أكبر من ٨ / Either < -8 or > 8",
                "|تعبير| > ٨ يعطي: تعبير < -٨ أو تعبير > ٨"
            ],
            "hints_ar": [
                "القيمة المطلقة > ٨ تعني حالتين منفصلتين",
                "إما أقل من -٨ أو أكبر من ٨",
                "|تعبير| > ٨ يعطي: تعبير < -٨ أو تعبير > ٨"
            ]
        },
        {
            "id": "practice5_2",
            "section_id": "section5",
            "type": ProblemType.PRACTICE,
            "weight": 15,
            "stage_type": "practice_word",
            "question_en": "A machine produces parts with target length 50mm. Tolerance is ±0.5mm. Write and solve inequality for acceptable lengths.",
            "question_ar": "آلة تنتج قطع بطول مستهدف ٥٠ مم. التفاوت المسموح ±٠.٥ مم. اكتب واحل متباينة الأطوال المقبولة.",
            "answer": "49.5 ≤ L ≤ 50.5",
            "answer_ar": "٤٩.٥ ≤ ط ≤ ٥٠.٥",
            "show_full_solution": False,
            "hide_answer": False,
            "step_solutions": [
                {
                    "step_en": "اكتب متباينة القيمة المطلقة / Write absolute value inequality",
                    "step_ar": "اكتب متباينة القيمة المطلقة",
                    "possible_answers": [
                        "|L - 50| ≤ 0.5",
                        "|ط - ٥٠| ≤ ٠.٥"
                    ],
                    "possible_answers_ar": [
                        "|ط - ٥٠| ≤ ٠.٥"
                    ]
                },
                {
                    "step_en": "حول إلى متباينة مركبة / Convert to compound",
                    "step_ar": "حول إلى متباينة مركبة",
                    "possible_answers": [
                        "-0.5 ≤ L - 50 ≤ 0.5",
                        "-٠.٥ ≤ ط - ٥٠ ≤ ٠.٥"
                    ],
                    "possible_answers_ar": [
                        "-٠.٥ ≤ ط - ٥٠ ≤ ٠.٥"
                    ]
                },
                {
                    "step_en": "احسب المدى المقبول للأطوال / Calculate acceptable length range",
                    "step_ar": "احسب المدى المقبول للأطوال",
                    "possible_answers": [
                        "49.5 ≤ L ≤ 50.5",
                        "٤٩.٥ ≤ ط ≤ ٥٠.٥"
                    ],
                    "possible_answers_ar": [
                        "٤٩.٥ ≤ ط ≤ ٥٠.٥"
                    ]
                }
            ],
            "final_answer_required": False,
            "hints_en": [
                "الفرق عن الطول المستهدف يجب أن يكون ضمن التفاوت / Difference from target must be within tolerance",
                "استخدم |الطول - المستهدف| ≤ التفاوت",
                "الفرق عن ٥٠ يجب أن يكون ≤ ٠.٥"
            ],
            "hints_ar": [
                "الفرق عن الطول المستهدف يجب أن يكون ضمن التفاوت",
                "استخدم |الطول - المستهدف| ≤ التفاوت",
                "الفرق عن ٥٠ يجب أن يكون ≤ ٠.٥"
            ]
        },
        {
            "id": "assessment5",
            "section_id": "section5",
            "type": ProblemType.ASSESSMENT,
            "weight": 20,
            "question_en": "What is the solution to |4 - x| ≥ 3?",
            "question_ar": "ما هو حل |٤ - س| ≥ ٣؟",
            "answer": "x ≤ 1 or x ≥ 7",
            "answer_ar": "س ≤ ١ أو س ≥ ٧",
            "show_full_solution": False,
            "hide_answer": True,
            "explanation_en": "Convert to two cases: 4 - x ≥ 3 or 4 - x ≤ -3, then solve each",
            "explanation_ar": "حول إلى حالتين: ٤ - س ≥ ٣ أو ٤ - س ≤ -٣، ثم احل كل حالة",
            "final_answer_required": True,
            "hints_en": [
                "فكر في حالتين: ٤ - س ≥ ٣ أو ٤ - س ≤ -٣ / Think two cases: 4 - x ≥ 3 or 4 - x ≤ -3",
                "حل كل حالة منفصلة وانتبه للإشارات / Solve each case separately, watch the signs"
            ],
            "hints_ar": [
                "فكر في حالتين: ٤ - س ≥ ٣ أو ٤ - س ≤ -٣",
                "حل كل حالة منفصلة وانتبه للإشارات"
            ]
        },
        {
            "id": "examprep5",
            "section_id": "section5",
            "type": ProblemType.EXAMPREP,
            "weight": 25,
            "question_en": "Solve: |2x + 1| - 3 < 4",
            "question_ar": "حل: |٢س + ١| - ٣ < ٤",
            "answer": "-4 < x < 3",
            "answer_ar": "-٤ < س < ٣",
            "show_full_solution": False,
            "hide_answer": True,
            "explanation_en": "First add 3 to both sides, then convert absolute value to compound inequality",
            "explanation_ar": "أولاً أضف ٣ للطرفين، ثم حول القيمة المطلقة إلى متباينة مركبة",
            "final_answer_required": True,
            "hints_en": [],
            "hints_ar": []
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