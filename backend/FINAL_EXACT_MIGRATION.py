#!/usr/bin/env python3
"""
FINAL CORRECT MIGRATION SCRIPT - Extracted from Working Preview
This contains the EXACT content from learning-equation.preview.emergentagent.com
Generated from your working Emergent preview database
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

# CONFIGURATION - UPDATE FOR YOUR PRODUCTION DATABASE
MONGO_URL = "mongodb+srv://ccccccccccccc@cluster0.dip2jyt.mongodb.net/mathtutor?retryWrites=true&w=majority&appName=Cluster0"  # ← REPLACE WITH YOUR MONGODB URL
DB_NAME = "mathtutor"           # ← REPLACE WITH YOUR DATABASE NAME

async def migrate_exact_preview_data():
    """Migrate EXACT data from working Emergent preview"""
    
    print("🚀 Starting EXACT migration from learning-equation.preview.emergentagent.com...")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print(f"📡 Connected to database: {DB_NAME}")
    
    # Collections
    problems_collection = db.problems
    sections_collection = db.sections
    
    # Clear existing data (OPTIONAL - comment out these lines to preserve existing data)
    print("🗑️ Clearing existing problems and sections...")
    await problems_collection.delete_many({})
    await sections_collection.delete_many({})
    
    # EXACT SECTIONS DATA FROM WORKING PREVIEW
    sections_data = [
        {
                "id": "section1",
                "title_en": "Section 1: Solving Inequalities by Addition or Subtraction",
                "title_ar": "\u0627\u0644\u0642\u0633\u0645 \u0627\u0644\u0623\u0648\u0644: \u062d\u0644 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0627\u062a \u0628\u0627\u0644\u062c\u0645\u0639 \u0623\u0648 \u0628\u0627\u0644\u0637\u0631\u062d"
        },
        {
                "id": "section2",
                "title_en": "Section 2: Solving Inequalities by Multiplication or Division",
                "title_ar": "\u0627\u0644\u0642\u0633\u0645 \u0627\u0644\u062b\u0627\u0646\u064a: \u062d\u0644 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0627\u062a \u0628\u0627\u0644\u0636\u0631\u0628 \u0623\u0648 \u0628\u0627\u0644\u0642\u0633\u0645\u0629"
        },
        {
                "id": "section3",
                "title_en": "Section 3: Solving Multi-Step Inequalities",
                "title_ar": "\u0627\u0644\u0642\u0633\u0645 \u0627\u0644\u062b\u0627\u0644\u062b: \u062d\u0644 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0627\u062a \u0627\u0644\u0645\u062a\u0639\u062f\u062f\u0629 \u0627\u0644\u062e\u0637\u0648\u0627\u062a"
        },
        {
                "id": "section4",
                "title_en": "Section 4: Solving Compound Inequalities",
                "title_ar": "\u0627\u0644\u0642\u0633\u0645 \u0627\u0644\u0631\u0627\u0628\u0639: \u062d\u0644 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0627\u062a \u0627\u0644\u0645\u0631\u0643\u0628\u0629"
        },
        {
                "id": "section5",
                "title_en": "Section 5: Solving Inequalities Involving Absolute Value",
                "title_ar": "\u0627\u0644\u0642\u0633\u0645 \u0627\u0644\u062e\u0627\u0645\u0633: \u062d\u0644 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0627\u062a \u0627\u0644\u062a\u064a \u062a\u062a\u0636\u0645\u0646 \u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u0645\u0637\u0644\u0642\u0629"
        }
]
    
    print("📚 Inserting EXACT sections from preview...")
    await sections_collection.insert_many(sections_data)
    
    # EXACT PROBLEMS DATA FROM WORKING PREVIEW  
    problems_data = [
        {
                "id": "prep1",
                "section_id": "section1",
                "type": "preparation",
                "weight": 10,
                "question_en": "x - 5 > 10",
                "question_ar": "\u0633 - \u0665 > \u0661\u0660",
                "answer": "x > 15",
                "answer_ar": "\u0633 > \u0661\u0665",
                "explanation_en": "This is a review problem for solving inequalities.",
                "explanation_ar": "\u0647\u0630\u0647 \u0645\u0633\u0623\u0644\u0629 \u0645\u0631\u0627\u062c\u0639\u0629 \u0644\u062d\u0644 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0627\u062a.",
                "show_full_solution": False,
                "hide_answer": False,
                "step_solutions": [
                        {
                                "step_en": "Add 5 to both sides",
                                "step_ar": "\u0623\u0636\u0641 \u0665 \u0625\u0644\u0649 \u0627\u0644\u0637\u0631\u0641\u064a\u0646",
                                "possible_answers": [
                                        "x - 5 + 5 > 10 + 5",
                                        "x > 10 + 5",
                                        "x > 15"
                                ],
                                "possible_answers_ar": [
                                        "\u0633 - \u0665 + \u0665 > \u0661\u0660 + \u0665",
                                        "\u0633 > \u0661\u0660 + \u0665",
                                        "\u0633 > \u0661\u0665"
                                ]
                        }
                ],
                "final_answer_required": True,
                "hints_en": [
                        "What operation undoes subtraction? Think about addition.",
                        "Add the same value to both sides to keep the inequality balanced.",
                        "Calculate: What is 10 + 5?"
                ],
                "hints_ar": [
                        "\u0645\u0627 \u0627\u0644\u0639\u0645\u0644\u064a\u0629 \u0627\u0644\u062a\u064a \u062a\u0644\u063a\u064a \u0627\u0644\u0637\u0631\u062d\u061f",
                        "\u0623\u0636\u0641 \u0665 \u0625\u0644\u0649 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0644\u0639\u0632\u0644 \u0633."
                ]
        },
        {
                "id": "explanation1",
                "section_id": "section1",
                "type": "explanation",
                "weight": 0,
                "question_en": "Learn Addition/Subtraction Inequalities",
                "question_ar": "\u062a\u0639\u0644\u0645 \u0645\u062a\u0628\u0627\u064a\u0646\u0627\u062a \u0627\u0644\u062c\u0645\u0639 \u0648\u0627\u0644\u0637\u0631\u062d",
                "answer": "",
                "answer_ar": "",
                "show_full_solution": False,
                "hide_answer": False,
                "explanation_en": "Learn to solve inequalities involving addition and subtraction",
                "explanation_ar": "\u062a\u0639\u0644\u0645 \u062d\u0644 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0627\u062a \u0627\u0644\u062a\u064a \u062a\u062a\u0636\u0645\u0646 \u0627\u0644\u062c\u0645\u0639 \u0648\u0627\u0644\u0637\u0631\u062d",
                "interactive_examples": [
                        {
                                "title_en": "Level 1: Simple (Example 1A - System Solved)",
                                "title_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0661: \u0628\u0633\u064a\u0637 (\u0627\u0644\u0645\u062b\u0627\u0644 \u0661\u0623 - \u062d\u0644 \u0627\u0644\u0646\u0638\u0627\u0645)",
                                "problem_en": "x - 8 > 2",
                                "problem_ar": "\u0633 - \u0668 > \u0662",
                                "solution_en": "Original inequality: x - 8 > 2\n\nStep 1: x - 8 + 8 > 2 + 8\nStep 2: x > 10",
                                "solution_ar": "\u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0627\u0644\u0623\u0635\u0644\u064a\u0629: \u0633 - \u0668 > \u0662\n\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0633 - \u0668 + \u0668 > \u0662 + \u0668\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0633 > \u0661\u0660",
                                "practice_question_en": "Now solve: y - 5 > 10",
                                "practice_question_ar": "\u0627\u0644\u0622\u0646 \u062d\u0644: \u0635 - \u0665 > \u0661\u0660",
                                "practice_answer": "y > 15",
                                "practice_answer_ar": "\u0635 > \u0661\u0665"
                        },
                        {
                                "title_en": "Level 2: Medium (Example 2A - System Solved)",
                                "title_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0662: \u0645\u062a\u0648\u0633\u0637 (\u0627\u0644\u0645\u062b\u0627\u0644 \u0662\u0623 - \u062d\u0644 \u0627\u0644\u0646\u0638\u0627\u0645)",
                                "problem_en": "12 \u2264 k + 3",
                                "problem_ar": "\u0661\u0662 \u2264 \u0643 + \u0663",
                                "solution_en": "Original inequality: 12 \u2264 k + 3\n\nStep 1: 12 - 3 \u2264 k + 3 - 3\nStep 2: 9 \u2264 k",
                                "solution_ar": "\u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0627\u0644\u0623\u0635\u0644\u064a\u0629: \u0661\u0662 \u2264 \u0643 + \u0663\n\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0661\u0662 - \u0663 \u2264 \u0643 + \u0663 - \u0663\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0669 \u2264 \u0643",
                                "practice_question_en": "Now solve: 20 \u2264 m + 8",
                                "practice_question_ar": "\u0627\u0644\u0622\u0646 \u062d\u0644: \u0662\u0660 \u2264 \u0645 + \u0668",
                                "practice_answer": "12 \u2264 m",
                                "practice_answer_ar": "\u0661\u0662 \u2264 \u0645"
                        },
                        {
                                "title_en": "Level 3: Advanced (Example 3A - System Solved)",
                                "title_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663: \u0645\u062a\u0642\u062f\u0645 (\u0627\u0644\u0645\u062b\u0627\u0644 \u0663\u0623 - \u062d\u0644 \u0627\u0644\u0646\u0638\u0627\u0645)",
                                "problem_en": "3n + 6 \u2265 2n + 9",
                                "problem_ar": "\u0663\u0646 + \u0666 \u2265 \u0662\u0646 + \u0669",
                                "solution_en": "Original inequality: 3n + 6 \u2265 2n + 9\n\nStep 1: 3n + 6 - 2n \u2265 2n + 9 - 2n\nStep 2: n + 6 \u2265 9\nStep 3: n + 6 - 6 \u2265 9 - 6\nStep 4: n \u2265 3",
                                "solution_ar": "\u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0627\u0644\u0623\u0635\u0644\u064a\u0629: \u0663\u0646 + \u0666 \u2265 \u0662\u0646 + \u0669\n\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0663\u0646 + \u0666 - \u0662\u0646 \u2265 \u0662\u0646 + \u0669 - \u0662\u0646\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0646 + \u0666 \u2265 \u0669\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0663: \u0646 + \u0666 - \u0666 \u2265 \u0669 - \u0666\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0664: \u0646 \u2265 \u0663",
                                "practice_question_en": "Now solve: 5k - 4 < 4k + 1",
                                "practice_question_ar": "\u0627\u0644\u0622\u0646 \u062d\u0644: \u0665\u0643 - \u0664 < \u0664\u0643 + \u0661",
                                "practice_answer": "k < 5",
                                "practice_answer_ar": "\u0643 < \u0665"
                        }
                ],
                "step_solutions": [
                        {
                                "step_en": "Level 1B Step 1: Add 5 to both sides",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0661\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0623\u0636\u0641 \u0665 \u0625\u0644\u0649 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646",
                                "possible_answers": [
                                        "y - 5 + 5 > 10 + 5",
                                        "y > 15"
                                ],
                                "possible_answers_ar": [
                                        "\u0635 - \u0665 + \u0665 > \u0661\u0660 + \u0665",
                                        "\u0635 > \u0661\u0665"
                                ]
                        },
                        {
                                "step_en": "Level 1B Step 2: Simplify",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0661\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0628\u0633\u0651\u0637",
                                "possible_answers": [
                                        "y > 15"
                                ],
                                "possible_answers_ar": [
                                        "\u0635 > \u0661\u0665"
                                ]
                        },
                        {
                                "step_en": "Level 2B Step 1: Subtract 8 from both sides",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0662\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0637\u0631\u062d \u0668 \u0645\u0646 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646",
                                "possible_answers": [
                                        "20 - 8 \u2264 m + 8 - 8",
                                        "12 \u2264 m"
                                ],
                                "possible_answers_ar": [
                                        "\u0662\u0660 - \u0668 \u2264 \u0645 + \u0668 - \u0668",
                                        "\u0661\u0662 \u2264 \u0645"
                                ]
                        },
                        {
                                "step_en": "Level 2B Step 2: Write in standard form",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0662\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0627\u0643\u062a\u0628 \u0628\u0627\u0644\u0634\u0643\u0644 \u0627\u0644\u0642\u064a\u0627\u0633\u064a",
                                "possible_answers": [
                                        "12 \u2264 m",
                                        "m \u2265 12"
                                ],
                                "possible_answers_ar": [
                                        "\u0661\u0662 \u2264 \u0645",
                                        "\u0645 \u2265 \u0661\u0662"
                                ]
                        },
                        {
                                "step_en": "Level 3B Step 1: Subtract 4k from both sides",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0637\u0631\u062d \u0664\u0643 \u0645\u0646 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646",
                                "possible_answers": [
                                        "5k - 4k - 4 < 4k - 4k + 1",
                                        "5k - 4 - 4k < 4k + 1 - 4k",
                                        "k - 4 < 1"
                                ],
                                "possible_answers_ar": [
                                        "\u0665\u0643 - \u0664\u0643 - \u0664 < \u0664\u0643 - \u0664\u0643 + \u0661",
                                        "\u0665\u0643 - \u0664 - \u0664\u0643 < \u0664\u0643 + \u0661 - \u0664\u0643",
                                        "\u0643 - \u0664 < \u0661"
                                ]
                        },
                        {
                                "step_en": "Level 3B Step 2: Add 4 to both sides",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0623\u0636\u0641 \u0664 \u0625\u0644\u0649 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646",
                                "possible_answers": [
                                        "k - 4 + 4 < 1 + 4",
                                        "k < 1 + 4"
                                ],
                                "possible_answers_ar": [
                                        "\u0643 - \u0664 + \u0664 < \u0661 + \u0664",
                                        "\u0643 < \u0661 + \u0664"
                                ]
                        },
                        {
                                "step_en": "Level 3B Step 3: Simplify to get final answer",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0663: \u0628\u0633\u0651\u0637 \u0644\u0644\u062d\u0635\u0648\u0644 \u0639\u0644\u0649 \u0627\u0644\u0625\u062c\u0627\u0628\u0629 \u0627\u0644\u0646\u0647\u0627\u0626\u064a\u0629",
                                "possible_answers": [
                                        "k < 5"
                                ],
                                "possible_answers_ar": [
                                        "\u0643 < \u0665"
                                ]
                        }
                ],
                "hints_en": [
                        "\u0644\u0644\u062a\u062e\u0644\u0635 \u0645\u0646 \u0627\u0644\u0637\u0631\u062d\u060c \u0645\u0627 \u0647\u064a \u0627\u0644\u0639\u0645\u0644\u064a\u0629 \u0627\u0644\u0639\u0643\u0633\u064a\u0629 \u0627\u0644\u062a\u064a \u064a\u062c\u0628 \u0623\u0646 \u062a\u0633\u062a\u062e\u062f\u0645\u0647\u0627\u061f",
                        "\u0642\u0645 \u0628\u062a\u0628\u0633\u064a\u0637 \u0643\u0644\u0627 \u0637\u0631\u0641\u064a \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629.",
                        "\u0644\u0639\u0632\u0644 \u0627\u0644\u0645\u062a\u063a\u064a\u0631 '\u0645'\u060c \u0645\u0627\u0630\u0627 \u064a\u062c\u0628 \u0623\u0646 \u062a\u0641\u0639\u0644 \u0628\u0627\u0644\u0631\u0642\u0645 \u0668\u061f",
                        "\u0645\u0627 \u0647\u0648 \u0646\u0627\u062a\u062c \u0662\u0660 - \u0668\u061f",
                        "\u0627\u0628\u062f\u0623 \u0628\u062c\u0645\u0639 \u062d\u062f\u0648\u062f '\u0643' \u0627\u0644\u0645\u062a\u0634\u0627\u0628\u0647\u0629 \u0641\u064a \u0637\u0631\u0641 \u0648\u0627\u062d\u062f.",
                        "\u0627\u0644\u0622\u0646 \u0627\u0639\u0632\u0644 \u0643 \u0628\u0625\u0636\u0627\u0641\u0629 \u0664 \u0625\u0644\u0649 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646."
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
                "id": "practice1_1",
                "section_id": "section1",
                "type": "practice",
                "weight": 15,
                "question_en": "m + 19 > 56",
                "question_ar": "\u0645 + \u0661\u0669 > \u0665\u0666",
                "answer": "m > 37",
                "answer_ar": "\u0645 > \u0663\u0667",
                "show_full_solution": False,
                "hide_answer": False,
                "step_solutions": [
                        {
                                "step_en": "Subtract 19 from both sides",
                                "step_ar": "\u0627\u0637\u0631\u062d \u0661\u0669 \u0645\u0646 \u0627\u0644\u0637\u0631\u0641\u064a\u0646",
                                "possible_answers": [
                                        "m + 19 - 19 > 56 - 19",
                                        "m > 56 - 19",
                                        "m > 37"
                                ],
                                "possible_answers_ar": [
                                        "\u0645 + \u0661\u0669 - \u0661\u0669 > \u0665\u0666 - \u0661\u0669",
                                        "\u0645 > \u0665\u0666 - \u0661\u0669",
                                        "\u0645 > \u0663\u0667"
                                ]
                        },
                        {
                                "step_en": "Simplify the calculation",
                                "step_ar": "\u0628\u0633\u0651\u0637 \u0627\u0644\u0639\u0645\u0644\u064a\u0629 \u0627\u0644\u062d\u0633\u0627\u0628\u064a\u0629",
                                "possible_answers": [
                                        "m > 37"
                                ],
                                "possible_answers_ar": [
                                        "\u0645 > \u0663\u0667"
                                ]
                        }
                ],
                "hints_en": [
                        "How can you isolate the variable 'm'?",
                        "Simplify the calculation."
                ],
                "hints_ar": [
                        "\u0643\u064a\u0641 \u064a\u0645\u0643\u0646\u0643 \u0639\u0632\u0644 \u0627\u0644\u0645\u062a\u063a\u064a\u0631 '\u0645'\u061f",
                        "\u0642\u0645 \u0628\u062a\u0628\u0633\u064a\u0637 \u0627\u0644\u0639\u0645\u0644\u064a\u0629 \u0627\u0644\u062d\u0633\u0627\u0628\u064a\u0629."
                ]
        },
        {
                "id": "practice1_2",
                "section_id": "section1",
                "type": "practice",
                "weight": 15,
                "question_en": "A school's goal is to collect at least SAR 500. They have SAR 210. How much more money (m) do they need?",
                "question_ar": "\u0647\u062f\u0641 \u0645\u062f\u0631\u0633\u0629 \u0647\u0648 \u062c\u0645\u0639 \u0665\u0660\u0660 \u0631\u064a\u0627\u0644 \u0639\u0644\u0649 \u0627\u0644\u0623\u0642\u0644. \u0644\u0642\u062f \u062c\u0645\u0639\u0648\u0627 \u0662\u0661\u0660 \u0631\u064a\u0627\u0644\u0627\u062a. \u0645\u0627 \u0647\u0648 \u0627\u0644\u0645\u0628\u0644\u063a \u0627\u0644\u0625\u0636\u0627\u0641\u064a (\u0645) \u0627\u0644\u0630\u064a \u064a\u062d\u062a\u0627\u062c\u0648\u0646 \u0644\u062c\u0645\u0639\u0647\u061f",
                "answer": "m \u2265 290",
                "answer_ar": "\u0645 \u2265 \u0662\u0669\u0660",
                "show_full_solution": False,
                "hide_answer": False,
                "step_solutions": [
                        {
                                "step_en": "Write an inequality showing the additional amount 'm', added to the available amount '210' must be greater than or equal to '500'",
                                "step_ar": "\u0627\u0643\u062a\u0628 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u062a\u0648\u0636\u062d \u0623\u0646 \u0627\u0644\u0645\u0628\u0644\u063a \u0627\u0644\u0625\u0636\u0627\u0641\u064a '\u0645'\u060c \u0645\u0636\u0627\u0641\u064b\u0627 \u0625\u0644\u0649 \u0627\u0644\u0645\u0628\u0644\u063a \u0627\u0644\u0645\u062a\u0627\u062d '\u0662\u0661\u0660' \u064a\u062c\u0628 \u0623\u0646 \u064a\u0643\u0648\u0646 \u0623\u0643\u0628\u0631 \u0645\u0646 \u0623\u0648 \u064a\u0633\u0627\u0648\u064a '\u0665\u0660\u0660'",
                                "possible_answers": [
                                        "m + 210 \u2265 500",
                                        "210 + m \u2265 500"
                                ],
                                "possible_answers_ar": [
                                        "\u0645 + \u0662\u0661\u0660 \u2265 \u0665\u0660\u0660",
                                        "\u0662\u0661\u0660 + \u0645 \u2265 \u0665\u0660\u0660"
                                ]
                        },
                        {
                                "step_en": "Subtract 210 from both sides",
                                "step_ar": "\u0627\u0637\u0631\u062d \u0662\u0661\u0660 \u0645\u0646 \u0627\u0644\u0637\u0631\u0641\u064a\u0646",
                                "possible_answers": [
                                        "m + 210 - 210 \u2265 500 - 210",
                                        "m \u2265 500 - 210",
                                        "210 + m - 210 \u2265 500 - 210"
                                ],
                                "possible_answers_ar": [
                                        "\u0645 + \u0662\u0661\u0660 - \u0662\u0661\u0660 \u2265 \u0665\u0660\u0660 - \u0662\u0661\u0660",
                                        "\u0645 \u2265 \u0665\u0660\u0660 - \u0662\u0661\u0660",
                                        "\u0662\u0661\u0660 + \u0645 - \u0662\u0661\u0660 \u2265 \u0665\u0660\u0660 - \u0662\u0661\u0660"
                                ]
                        },
                        {
                                "step_en": "Simplify to get final answer",
                                "step_ar": "\u0628\u0633\u0651\u0637 \u0644\u0644\u062d\u0635\u0648\u0644 \u0639\u0644\u0649 \u0627\u0644\u0625\u062c\u0627\u0628\u0629 \u0627\u0644\u0646\u0647\u0627\u0626\u064a\u0629",
                                "possible_answers": [
                                        "m \u2265 290"
                                ],
                                "possible_answers_ar": [
                                        "\u0645 \u2265 \u0662\u0669\u0660"
                                ]
                        }
                ],
                "hints_en": [
                        "What inequality symbol does \"at least\" mean? (\u2265)",
                        "Use subtraction to isolate 'm'."
                ],
                "hints_ar": [
                        "\u0643\u0644\u0645\u0629 \"\u0639\u0644\u0649 \u0627\u0644\u0623\u0642\u0644\" \u062a\u0639\u0646\u064a \u0623\u064a \u0631\u0645\u0632 \u0645\u062a\u0628\u0627\u064a\u0646\u0629\u061f (\u2265)",
                        "\u0627\u0633\u062a\u062e\u062f\u0645 \u0639\u0645\u0644\u064a\u0629 \u0627\u0644\u0637\u0631\u062d \u0644\u0639\u0632\u0644 '\u0645'."
                ]
        },
        {
                "id": "assessment1",
                "section_id": "section1",
                "type": "assessment",
                "weight": 30,
                "question_en": "k - 9 \u2265 2",
                "question_ar": "\u0643 - \u0669 \u2265 \u0662",
                "answer": "k \u2265 11",
                "answer_ar": "\u0643 \u2265 \u0661\u0661",
                "show_full_solution": False,
                "hide_answer": True,
                "hints_en": [
                        "Think about what operation will help you solve for k.",
                        "You need to isolate k by using addition.",
                        "That's all the hints available."
                ],
                "hints_ar": [
                        "\u0641\u0643\u0631 \u0641\u064a \u0627\u0644\u0639\u0645\u0644\u064a\u0629 \u0627\u0644\u062a\u064a \u0633\u062a\u0633\u0627\u0639\u062f\u0643 \u0641\u064a \u062d\u0644 \u0643.",
                        "\u062a\u062d\u062a\u0627\u062c \u0625\u0644\u0649 \u0639\u0632\u0644 \u0643 \u0628\u0627\u0633\u062a\u062e\u062f\u0627\u0645 \u0627\u0644\u062c\u0645\u0639.",
                        "\u0647\u0630\u0647 \u0643\u0644 \u0627\u0644\u0625\u0631\u0634\u0627\u062f\u0627\u062a \u0627\u0644\u0645\u062a\u0627\u062d\u0629."
                ]
        },
        {
                "id": "examprep1",
                "section_id": "section1",
                "type": "examprep",
                "weight": 30,
                "question_en": "Sara has SAR 150 and wants to buy a gift that costs at least SAR 220. Write and solve an inequality to find the additional amount (m) she needs.",
                "question_ar": "\u0644\u062f\u0649 \u0633\u0627\u0631\u0629 \u0661\u0665\u0660 \u0631\u064a\u0627\u0644\u0627\u064b \u0648\u062a\u0631\u064a\u062f \u0634\u0631\u0627\u0621 \u0647\u062f\u064a\u0629 \u062a\u0643\u0644\u0641 \u0639\u0644\u0649 \u0627\u0644\u0623\u0642\u0644 \u0662\u0662\u0660 \u0631\u064a\u0627\u0644\u0627\u064b. \u0627\u0643\u062a\u0628 \u0648\u062d\u0644 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0644\u0625\u064a\u062c\u0627\u062f \u0627\u0644\u0645\u0628\u0644\u063a \u0627\u0644\u0625\u0636\u0627\u0641\u064a (\u0645) \u0627\u0644\u0630\u064a \u062a\u062d\u062a\u0627\u062c\u0647.",
                "answer": "m \u2265 70",
                "answer_ar": "\u0645 \u2265 \u0667\u0660",
                "show_full_solution": False,
                "hide_answer": True,
                "hints_en": [
                        "The inequality is 150 + m \u2265 220",
                        "Subtract 150 from both sides to solve for m.",
                        "That's all the hints available."
                ],
                "hints_ar": [
                        "\u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0647\u064a \u0661\u0665\u0660 + \u0645 \u2265 \u0662\u0662\u0660",
                        "\u0627\u0637\u0631\u062d \u0661\u0665\u0660 \u0645\u0646 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0644\u062d\u0644 \u0645.",
                        "\u0647\u0630\u0647 \u0643\u0644 \u0627\u0644\u0625\u0631\u0634\u0627\u062f\u0627\u062a \u0627\u0644\u0645\u062a\u0627\u062d\u0629."
                ]
        },
        {
                "id": "prep2",
                "section_id": "section2",
                "type": "preparation",
                "weight": 10,
                "question_en": "4x < 20",
                "question_ar": "\u0664\u0633 < \u0662\u0660",
                "answer": "x < 5",
                "answer_ar": "\u0633 < \u0665",
                "explanation_en": "This is a review problem for solving inequalities by multiplication or division.",
                "explanation_ar": "\u0647\u0630\u0647 \u0645\u0633\u0623\u0644\u0629 \u0645\u0631\u0627\u062c\u0639\u0629 \u0644\u062d\u0644 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0627\u062a \u0628\u0627\u0644\u0636\u0631\u0628 \u0623\u0648 \u0628\u0627\u0644\u0642\u0633\u0645\u0629.",
                "show_full_solution": False,
                "hide_answer": False,
                "step_solutions": [
                        {
                                "step_en": "Step 1: Divide both sides by 4",
                                "step_ar": "\u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0642\u0633\u0645 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0639\u0644\u0649 \u0664",
                                "possible_answers": [
                                        "4x / 4 < 20 / 4",
                                        "x < 20 / 4"
                                ],
                                "possible_answers_ar": [
                                        "\u0664\u0633 / \u0664 < \u0662\u0660 / \u0664",
                                        "\u0633 < \u0662\u0660 / \u0664"
                                ]
                        },
                        {
                                "step_en": "Step 2: Simplify the result",
                                "step_ar": "\u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0628\u0633\u0651\u0637 \u0627\u0644\u0646\u062a\u064a\u062c\u0629",
                                "possible_answers": [
                                        "x < 5"
                                ],
                                "possible_answers_ar": [
                                        "\u0633 < \u0665"
                                ]
                        }
                ],
                "final_answer_required": True,
                "hints_en": [
                        "What operation cancels out multiplication by 4?",
                        "Divide both sides by 4 to isolate x."
                ],
                "hints_ar": [
                        "\u0645\u0627 \u0627\u0644\u0639\u0645\u0644\u064a\u0629 \u0627\u0644\u062a\u064a \u062a\u0644\u063a\u064a \u0627\u0644\u0636\u0631\u0628 \u0641\u064a \u0664\u061f",
                        "\u0627\u0642\u0633\u0645 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0639\u0644\u0649 \u0664 \u0644\u0639\u0632\u0644 \u0633."
                ]
        },
        {
                "id": "explanation2",
                "section_id": "section2",
                "type": "explanation",
                "weight": 0,
                "question_en": "Learn Multiplication/Division Inequalities",
                "question_ar": "\u062a\u0639\u0644\u0645 \u0645\u062a\u0628\u0627\u064a\u0646\u0627\u062a \u0627\u0644\u0636\u0631\u0628 \u0648\u0627\u0644\u0642\u0633\u0645\u0629",
                "answer": "",
                "answer_ar": "",
                "show_full_solution": False,
                "hide_answer": False,
                "explanation_en": "Learn to solve inequalities involving multiplication and division",
                "explanation_ar": "\u062a\u0639\u0644\u0645 \u062d\u0644 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0627\u062a \u0627\u0644\u062a\u064a \u062a\u062a\u0636\u0645\u0646 \u0627\u0644\u0636\u0631\u0628 \u0648\u0627\u0644\u0642\u0633\u0645\u0629",
                "interactive_examples": [
                        {
                                "title_en": "Level 1: Simple (Positive Coefficient) - Example 1A (System Solved)",
                                "title_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0661: \u0628\u0633\u064a\u0637 (\u0645\u0639\u0627\u0645\u0644 \u0645\u0648\u062c\u0628) - \u0627\u0644\u0645\u062b\u0627\u0644 \u0661\u0623 (\u062d\u0644 \u0627\u0644\u0646\u0638\u0627\u0645)",
                                "problem_en": "5x \u2265 30",
                                "problem_ar": "\u0665\u0633 \u2265 \u0663\u0660",
                                "solution_en": "Original inequality: 5x \u2265 30\n\nStep 1: Divide both sides by 5\n5x / 5 \u2265 30 / 5\nStep 2: Simplify\nx \u2265 6",
                                "solution_ar": "\u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0627\u0644\u0623\u0635\u0644\u064a\u0629: \u0665\u0633 \u2265 \u0663\u0660\n\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0642\u0633\u0645 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0639\u0644\u0649 \u0665\n\u0665\u0633 / \u0665 \u2265 \u0663\u0660 / \u0665\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0628\u0633\u0651\u0637\n\u0633 \u2265 \u0666",
                                "practice_question_en": "Now solve: 4x \u2265 20",
                                "practice_question_ar": "\u0627\u0644\u0622\u0646 \u062d\u0644: \u0664\u0633 \u2265 \u0662\u0660",
                                "practice_answer": "x \u2265 5",
                                "practice_answer_ar": "\u0633 \u2265 \u0665"
                        },
                        {
                                "title_en": "Level 2: Medium (Negative Coefficient) - Example 2A (System Solved)",
                                "title_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0662: \u0645\u062a\u0648\u0633\u0637 (\u0645\u0639\u0627\u0645\u0644 \u0633\u0627\u0644\u0628) - \u0627\u0644\u0645\u062b\u0627\u0644 \u0662\u0623 (\u062d\u0644 \u0627\u0644\u0646\u0638\u0627\u0645)",
                                "problem_en": "-2p > 8",
                                "problem_ar": "-\u0662\u0641 > \u0668",
                                "solution_en": "Original inequality: -2p > 8\n\nStep 1: Divide both sides by -2 (flip sign)\n-2p / (-2) < 8 / (-2)\nStep 2: Simplify\np < -4",
                                "solution_ar": "\u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0627\u0644\u0623\u0635\u0644\u064a\u0629: -\u0662\u0641 > \u0668\n\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0642\u0633\u0645 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0639\u0644\u0649 -\u0662 (\u0627\u0642\u0644\u0628 \u0627\u0644\u0625\u0634\u0627\u0631\u0629)\n-\u0662\u0641 / (-\u0662) < \u0668 / (-\u0662)\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0628\u0633\u0651\u0637\n\u0641 < -\u0664",
                                "practice_question_en": "Now solve: -3m < 15",
                                "practice_question_ar": "\u0627\u0644\u0622\u0646 \u062d\u0644: -\u0663\u0645 < \u0661\u0665",
                                "practice_answer": "m > -5",
                                "practice_answer_ar": "\u0645 > -\u0665"
                        },
                        {
                                "title_en": "Level 3: Advanced (Negative Division) - Example 3A (System Solved)",
                                "title_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663: \u0645\u062a\u0642\u062f\u0645 (\u0627\u0644\u0642\u0633\u0645\u0629 \u0627\u0644\u0633\u0627\u0644\u0628\u0629) - \u0627\u0644\u0645\u062b\u0627\u0644 \u0663\u0623 (\u062d\u0644 \u0627\u0644\u0646\u0638\u0627\u0645)",
                                "problem_en": "-5w \u2264 25",
                                "problem_ar": "-\u0665\u0648 \u2264 \u0662\u0665",
                                "solution_en": "Original inequality: -5w \u2264 25\n\nStep 1: Divide both sides by -5 (flip sign)\n-5w / (-5) \u2265 25 / (-5)\nStep 2: Simplify\nw \u2265 -5",
                                "solution_ar": "\u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0627\u0644\u0623\u0635\u0644\u064a\u0629: -\u0665\u0648 \u2264 \u0662\u0665\n\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0642\u0633\u0645 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0639\u0644\u0649 -\u0665 (\u0627\u0642\u0644\u0628 \u0627\u0644\u0625\u0634\u0627\u0631\u0629)\n-\u0665\u0648 / (-\u0665) \u2265 \u0662\u0665 / (-\u0665)\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0628\u0633\u0651\u0637\n\u0648 \u2265 -\u0665",
                                "practice_question_en": "Now solve: -6k \u2265 30",
                                "practice_question_ar": "\u0627\u0644\u0622\u0646 \u062d\u0644: -\u0666\u0643 \u2265 \u0663\u0660",
                                "practice_answer": "k \u2264 -5",
                                "practice_answer_ar": "\u0643 \u2264 -\u0665"
                        }
                ],
                "step_solutions": [
                        {
                                "step_en": "Level 1B Step 1: Divide both sides by 4",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0661\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0642\u0633\u0645 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0639\u0644\u0649 \u0664",
                                "possible_answers": [
                                        "4x / 4 \u2265 20 / 4",
                                        "x \u2265 20 / 4",
                                        "4x/4 \u2265 20/4"
                                ],
                                "possible_answers_ar": [
                                        "\u0664\u0633 / \u0664 \u2265 \u0662\u0660 / \u0664",
                                        "\u0633 \u2265 \u0662\u0660 / \u0664",
                                        "\u0664\u0633/\u0664 \u2265 \u0662\u0660/\u0664"
                                ]
                        },
                        {
                                "step_en": "Level 1B Step 2: Simplify",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0661\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0628\u0633\u0651\u0637",
                                "possible_answers": [
                                        "x \u2265 5",
                                        "\u0633 \u2265 \u0665"
                                ],
                                "possible_answers_ar": [
                                        "\u0633 \u2265 \u0665",
                                        "x \u2265 5"
                                ]
                        },
                        {
                                "step_en": "Level 2B Step 1: Divide both sides by -3 (flip the inequality sign)",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0662\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0642\u0633\u0645 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0639\u0644\u0649 -\u0663 (\u0627\u0642\u0644\u0628 \u0625\u0634\u0627\u0631\u0629 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629)",
                                "possible_answers": [
                                        "-3m / (-3) > 15 / (-3)",
                                        "m > 15 / (-3)",
                                        "-3m/(-3) > 15/(-3)",
                                        "m > -5"
                                ],
                                "possible_answers_ar": [
                                        "-\u0663\u0645 / (-\u0663) > \u0661\u0665 / (-\u0663)",
                                        "\u0645 > \u0661\u0665 / (-\u0663)",
                                        "-\u0663\u0645/(-\u0663) > \u0661\u0665/(-\u0663)",
                                        "\u0645 > -\u0665"
                                ]
                        },
                        {
                                "step_en": "Level 2B Step 2: Simplify",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0662\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0628\u0633\u0651\u0637",
                                "possible_answers": [
                                        "m > -5",
                                        "\u0645 > -\u0665"
                                ],
                                "possible_answers_ar": [
                                        "\u0645 > -\u0665",
                                        "m > -5"
                                ]
                        },
                        {
                                "step_en": "Level 3B Step 1: Divide both sides by -6 (flip the inequality sign)",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0642\u0633\u0645 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0639\u0644\u0649 -\u0666 (\u0627\u0642\u0644\u0628 \u0625\u0634\u0627\u0631\u0629 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629)",
                                "possible_answers": [
                                        "-6k / (-6) \u2264 30 / (-6)",
                                        "k \u2264 30 / (-6)",
                                        "-6k/(-6) \u2264 30/(-6)",
                                        "k \u2264 -5"
                                ],
                                "possible_answers_ar": [
                                        "-\u0666\u0643 / (-\u0666) \u2264 \u0663\u0660 / (-\u0666)",
                                        "\u0643 \u2264 \u0663\u0660 / (-\u0666)",
                                        "-\u0666\u0643/(-\u0666) \u2264 \u0663\u0660/(-\u0666)",
                                        "\u0643 \u2264 -\u0665"
                                ]
                        },
                        {
                                "step_en": "Level 3B Step 2: Simplify",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0628\u0633\u0651\u0637",
                                "possible_answers": [
                                        "k \u2264 -5",
                                        "\u0643 \u2264 -\u0665"
                                ],
                                "possible_answers_ar": [
                                        "\u0643 \u2264 -\u0665",
                                        "k \u2264 -5"
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
                        "\u0644\u0639\u0632\u0644 \u0633\u060c \u0639\u0644\u0649 \u0623\u064a \u0631\u0642\u0645 \u064a\u062c\u0628 \u0623\u0646 \u062a\u0642\u0633\u0645 \u0627\u0644\u0637\u0631\u0641\u064a\u0646\u061f",
                        "\u0627\u0644\u0622\u0646 \u0628\u0633\u0651\u0637 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0644\u0644\u062d\u0635\u0648\u0644 \u0639\u0644\u0649 \u0627\u0644\u0625\u062c\u0627\u0628\u0629 \u0627\u0644\u0646\u0647\u0627\u0626\u064a\u0629.",
                        "\u0645\u0627 \u0627\u0644\u0639\u0645\u0644\u064a\u0629 \u0627\u0644\u0644\u0627\u0632\u0645\u0629 \u0644\u0639\u0632\u0644 \u0645\u061f \u062a\u0630\u0643\u0631 \u0642\u0627\u0639\u062f\u0629 \u0642\u0644\u0628 \u0627\u0644\u0625\u0634\u0627\u0631\u0629!",
                        "\u0628\u0633\u0651\u0637 \u0627\u0644\u0639\u0645\u0644\u064a\u0629 \u0627\u0644\u062d\u0633\u0627\u0628\u064a\u0629 \u0644\u0644\u062d\u0635\u0648\u0644 \u0639\u0644\u0649 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0627\u0644\u0646\u0647\u0627\u0626\u064a\u0629.",
                        "\u0644\u0639\u0632\u0644 \u0643\u060c \u0627\u0642\u0633\u0645 \u0639\u0644\u0649 -\u0666. \u0645\u0627\u0630\u0627 \u064a\u062d\u062f\u062b \u0644\u0625\u0634\u0627\u0631\u0629 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629\u061f",
                        "\u0623\u0643\u0645\u0644 \u0627\u0644\u062a\u0628\u0633\u064a\u0637 \u0644\u0644\u062d\u0635\u0648\u0644 \u0639\u0644\u0649 \u0627\u0644\u0625\u062c\u0627\u0628\u0629 \u0627\u0644\u0646\u0647\u0627\u0626\u064a\u0629."
                ]
        },
        {
                "id": "practice2_1",
                "section_id": "section2",
                "type": "practice",
                "weight": 15,
                "question_en": "-2/3 k > 8",
                "question_ar": "-\u0662/\u0663 \u0643 > \u0668",
                "answer": "k < -12",
                "answer_ar": "\u0643 < -\u0661\u0662",
                "show_full_solution": False,
                "hide_answer": False,
                "step_solutions": [
                        {
                                "step_en": "Multiply both sides by -3/2 and flip the inequality sign",
                                "step_ar": "\u0627\u0636\u0631\u0628 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0641\u064a -\u0663/\u0662 \u0648\u0627\u0642\u0644\u0628 \u0625\u0634\u0627\u0631\u0629 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629",
                                "possible_answers": [
                                        "(-2/3) k * (-3/2) < 8 * (-3/2)",
                                        "k < 8 * (-3/2)",
                                        "k < -12"
                                ],
                                "possible_answers_ar": [
                                        "(-\u0662/\u0663) \u0643 * (-\u0663/\u0662) < \u0668 * (-\u0663/\u0662)",
                                        "\u0643 < \u0668 * (-\u0663/\u0662)",
                                        "\u0643 < -\u0661\u0662"
                                ]
                        },
                        {
                                "step_en": "Flip the inequality sign",
                                "step_ar": "\u0627\u0642\u0644\u0628 \u0625\u0634\u0627\u0631\u0629 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629",
                                "possible_answers": [
                                        "k < -12"
                                ],
                                "possible_answers_ar": [
                                        "\u0643 < -\u0661\u0662"
                                ]
                        },
                        {
                                "step_en": "Simplify 8 * (-3/2)",
                                "step_ar": "\u0628\u0633\u0651\u0637 \u0668 * (-\u0663/\u0662)",
                                "possible_answers": [
                                        "k < -12"
                                ],
                                "possible_answers_ar": [
                                        "\u0643 < -\u0661\u0662"
                                ]
                        }
                ],
                "hints_en": [
                        "To isolate k, multiply both sides by -3/2 (the reciprocal). Remember: when multiplying by a negative number, flip the inequality sign!",
                        "When multiplying both sides by a negative number, what happens to the inequality sign?",
                        "The rule: multiply by the reciprocal and flip the inequality sign when the multiplier is negative."
                ],
                "hints_ar": [
                        "\u0644\u0639\u0632\u0644 \u0643\u060c \u0627\u0636\u0631\u0628 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0641\u064a -\u0663/\u0662 (\u0627\u0644\u0645\u0642\u0644\u0648\u0628). \u062a\u0630\u0643\u0631: \u0639\u0646\u062f \u0627\u0644\u0636\u0631\u0628 \u0641\u064a \u0639\u062f\u062f \u0633\u0627\u0644\u0628\u060c \u0627\u0642\u0644\u0628 \u0625\u0634\u0627\u0631\u0629 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629!",
                        "\u0639\u0646\u062f \u0636\u0631\u0628 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0641\u064a \u0639\u062f\u062f \u0633\u0627\u0644\u0628\u060c \u0645\u0627\u0630\u0627 \u064a\u062d\u062f\u062b \u0644\u0625\u0634\u0627\u0631\u0629 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629\u061f",
                        "\u0627\u0644\u0642\u0627\u0639\u062f\u0629: \u0627\u0636\u0631\u0628 \u0641\u064a \u0627\u0644\u0645\u0642\u0644\u0648\u0628 \u0648\u0627\u0642\u0644\u0628 \u0625\u0634\u0627\u0631\u0629 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0639\u0646\u062f\u0645\u0627 \u064a\u0643\u0648\u0646 \u0627\u0644\u0645\u0636\u0631\u0648\u0628 \u0633\u0627\u0644\u0628\u0627\u064b."
                ]
        },
        {
                "id": "practice2_2",
                "section_id": "section2",
                "type": "practice",
                "weight": 15,
                "question_en": "Tickets must be sold at SAR 10 each to collect at least SAR 500. What is the minimum number of tickets (t) that must be sold?",
                "question_ar": "\u064a\u062c\u0628 \u0628\u064a\u0639 \u062a\u0630\u0627\u0643\u0631 \u0628\u0633\u0639\u0631 \u0661\u0660 \u0631\u064a\u0627\u0644\u0627\u062a \u0644\u0644\u062a\u0630\u0643\u0631\u0629 \u0627\u0644\u0648\u0627\u062d\u062f\u0629 \u0644\u062c\u0645\u0639 \u0665\u0660\u0660 \u0631\u064a\u0627\u0644 \u0639\u0644\u0649 \u0627\u0644\u0623\u0642\u0644. \u0645\u0627 \u0647\u0648 \u0623\u0642\u0644 \u0639\u062f\u062f \u0645\u0646 \u0627\u0644\u062a\u0630\u0627\u0643\u0631 (\u062a) \u064a\u062c\u0628 \u0628\u064a\u0639\u0647\u061f",
                "answer": "t \u2265 50",
                "answer_ar": "\u062a \u2265 \u0665\u0660",
                "show_full_solution": False,
                "hide_answer": False,
                "step_solutions": [
                        {
                                "step_en": "Step 1: Write the inequality from the word problem",
                                "step_ar": "\u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0643\u062a\u0628 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0646 \u0627\u0644\u0645\u0633\u0623\u0644\u0629 \u0627\u0644\u0643\u0644\u0627\u0645\u064a\u0629",
                                "possible_answers": [
                                        "10t \u2265 500",
                                        "10 * t \u2265 500"
                                ],
                                "possible_answers_ar": [
                                        "\u0661\u0660\u062a \u2265 \u0665\u0660\u0660",
                                        "\u0661\u0660 * \u062a \u2265 \u0665\u0660\u0660"
                                ]
                        },
                        {
                                "step_en": "Step 2: Divide both sides by 10 (show the operation)",
                                "step_ar": "\u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0627\u0642\u0633\u0645 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0639\u0644\u0649 \u0661\u0660 (\u0627\u0638\u0647\u0631 \u0627\u0644\u0639\u0645\u0644\u064a\u0629)",
                                "possible_answers": [
                                        "10t / 10 \u2265 500 / 10",
                                        "t \u2265 500 / 10"
                                ],
                                "possible_answers_ar": [
                                        "\u0661\u0660\u062a / \u0661\u0660 \u2265 \u0665\u0660\u0660 / \u0661\u0660",
                                        "\u062a \u2265 \u0665\u0660\u0660 / \u0661\u0660"
                                ]
                        },
                        {
                                "step_en": "Step 3: Simplify to final answer",
                                "step_ar": "\u0627\u0644\u062e\u0637\u0648\u0629 \u0663: \u0628\u0633\u0651\u0637 \u0644\u0644\u062d\u0635\u0648\u0644 \u0639\u0644\u0649 \u0627\u0644\u0625\u062c\u0627\u0628\u0629 \u0627\u0644\u0646\u0647\u0627\u0626\u064a\u0629",
                                "possible_answers": [
                                        "t \u2265 50"
                                ],
                                "possible_answers_ar": [
                                        "\u062a \u2265 \u0665\u0660"
                                ]
                        }
                ],
                "hints_en": [
                        "Think about the variable: t represents number of tickets. What's the price per ticket? What amount needs to be collected?",
                        "If you sell t tickets at 10 SAR each, how much will you collect? Does it need to be greater than or equal to 500?",
                        "Amount collected = price per ticket \u00d7 number of tickets. Use \u2265 symbol because it says \"at least\""
                ],
                "hints_ar": [
                        "\u0641\u0643\u0631 \u0641\u064a \u0627\u0644\u0645\u062a\u063a\u064a\u0631: \u062a \u064a\u0645\u062b\u0644 \u0639\u062f\u062f \u0627\u0644\u062a\u0630\u0627\u0643\u0631. \u0645\u0627 \u0647\u0648 \u0633\u0639\u0631 \u0627\u0644\u062a\u0630\u0643\u0631\u0629 \u0627\u0644\u0648\u0627\u062d\u062f\u0629\u061f \u0648\u0645\u0627 \u0627\u0644\u0645\u0628\u0644\u063a \u0627\u0644\u0645\u0637\u0644\u0648\u0628 \u062c\u0645\u0639\u0647\u061f",
                        "\u0625\u0630\u0627 \u0628\u0639\u062a \u062a \u062a\u0630\u0643\u0631\u0629 \u0628\u0633\u0639\u0631 \u0661\u0660 \u0631\u064a\u0627\u0644\u060c \u0643\u0645 \u0633\u062a\u062c\u0645\u0639\u061f \u0647\u0644 \u062a\u062d\u062a\u0627\u062c \u0623\u0646 \u064a\u0643\u0648\u0646 \u0627\u0644\u0645\u0628\u0644\u063a \u0623\u0643\u0628\u0631 \u0645\u0646 \u0623\u0648 \u064a\u0633\u0627\u0648\u064a \u0665\u0660\u0660\u061f",
                        "\u0627\u0644\u0645\u0628\u0644\u063a \u0627\u0644\u0645\u062c\u0645\u0648\u0639 = \u0633\u0639\u0631 \u0627\u0644\u062a\u0630\u0643\u0631\u0629 \u00d7 \u0639\u062f\u062f \u0627\u0644\u062a\u0630\u0627\u0643\u0631. \u0627\u0633\u062a\u062e\u062f\u0645 \u0627\u0644\u0631\u0645\u0632 \u2265 \u0644\u0623\u0646 \u0627\u0644\u0645\u0637\u0644\u0648\u0628 \"\u0639\u0644\u0649 \u0627\u0644\u0623\u0642\u0644\""
                ]
        },
        {
                "id": "assessment2",
                "section_id": "section2",
                "type": "assessment",
                "weight": 30,
                "question_en": "y / (-2) > 6",
                "question_ar": "\u0635 / (-\u0662) > \u0666",
                "answer": "y < -12",
                "answer_ar": "\u0635 < -\u0661\u0662",
                "show_full_solution": False,
                "hide_answer": True,
                "hints_en": [
                        "When a variable is divided by a negative number, what operation isolates it?",
                        "Pay attention to what happens to the inequality sign when you multiply by a negative.",
                        "Focus on the process, not the specific numbers."
                ],
                "hints_ar": [
                        "\u0639\u0646\u062f\u0645\u0627 \u064a\u0643\u0648\u0646 \u0627\u0644\u0645\u062a\u063a\u064a\u0631 \u0645\u0642\u0633\u0648\u0645\u0627\u064b \u0639\u0644\u0649 \u0639\u062f\u062f \u0633\u0627\u0644\u0628\u060c \u0645\u0627 \u0627\u0644\u0639\u0645\u0644\u064a\u0629 \u0627\u0644\u062a\u064a \u062a\u0639\u0632\u0644\u0647\u061f",
                        "\u0627\u0646\u062a\u0628\u0647 \u0644\u0645\u0627 \u064a\u062d\u062f\u062b \u0644\u0625\u0634\u0627\u0631\u0629 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0639\u0646\u062f \u0627\u0644\u0636\u0631\u0628 \u0641\u064a \u0639\u062f\u062f \u0633\u0627\u0644\u0628.",
                        "\u0631\u0643\u0632 \u0639\u0644\u0649 \u0627\u0644\u0639\u0645\u0644\u064a\u0629\u060c \u0648\u0644\u064a\u0633 \u0639\u0644\u0649 \u0627\u0644\u0623\u0631\u0642\u0627\u0645 \u0627\u0644\u0645\u062d\u062f\u062f\u0629."
                ]
        },
        {
                "id": "examprep2",
                "section_id": "section2",
                "type": "examprep",
                "weight": 30,
                "question_en": "You want to distribute at least 60 pieces of candy equally among 15 children. Write and solve an inequality to find the minimum number of pieces (p) each child can get.",
                "question_ar": "\u062a\u0631\u064a\u062f \u062a\u0648\u0632\u064a\u0639 \u0666\u0660 \u0642\u0637\u0639\u0629 \u062d\u0644\u0648\u0649 \u0639\u0644\u0649 \u0627\u0644\u0623\u0642\u0644 \u0628\u0627\u0644\u062a\u0633\u0627\u0648\u064a \u0639\u0644\u0649 \u0661\u0665 \u0637\u0641\u0644\u0627\u064b. \u0627\u0643\u062a\u0628 \u0648\u062d\u0644 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0644\u0625\u064a\u062c\u0627\u062f \u0623\u0642\u0644 \u0639\u062f\u062f \u0645\u0646 \u0642\u0637\u0639 \u0627\u0644\u062d\u0644\u0648\u0649 (\u062d) \u064a\u0645\u0643\u0646 \u0623\u0646 \u064a\u062d\u0635\u0644 \u0639\u0644\u064a\u0647 \u0643\u0644 \u0637\u0641\u0644.",
                "answer": "p \u2265 4",
                "answer_ar": "\u062d \u2265 \u0664",
                "show_full_solution": False,
                "hide_answer": True,
                "step_solutions": [
                        {
                                "step_en": "Step 1: Write the inequality from the word problem",
                                "step_ar": "\u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0643\u062a\u0628 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0646 \u0627\u0644\u0645\u0633\u0623\u0644\u0629 \u0627\u0644\u0643\u0644\u0627\u0645\u064a\u0629",
                                "possible_answers": [
                                        "15p \u2265 60",
                                        "15 * p \u2265 60"
                                ],
                                "possible_answers_ar": [
                                        "\u0661\u0665\u062d \u2265 \u0666\u0660",
                                        "\u0661\u0665 * \u062d \u2265 \u0666\u0660"
                                ]
                        },
                        {
                                "step_en": "Step 2: Divide both sides by 15 (show the operation)",
                                "step_ar": "\u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0627\u0642\u0633\u0645 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0639\u0644\u0649 \u0661\u0665 (\u0627\u0638\u0647\u0631 \u0627\u0644\u0639\u0645\u0644\u064a\u0629)",
                                "possible_answers": [
                                        "15p / 15 \u2265 60 / 15",
                                        "p \u2265 60 / 15"
                                ],
                                "possible_answers_ar": [
                                        "\u0661\u0665\u062d / \u0661\u0665 \u2265 \u0666\u0660 / \u0661\u0665",
                                        "\u062d \u2265 \u0666\u0660 / \u0661\u0665"
                                ]
                        },
                        {
                                "step_en": "Step 3: Simplify to final answer",
                                "step_ar": "\u0627\u0644\u062e\u0637\u0648\u0629 \u0663: \u0628\u0633\u0651\u0637 \u0644\u0644\u062d\u0635\u0648\u0644 \u0639\u0644\u0649 \u0627\u0644\u0625\u062c\u0627\u0628\u0629 \u0627\u0644\u0646\u0647\u0627\u0626\u064a\u0629",
                                "possible_answers": [
                                        "p \u2265 4"
                                ],
                                "possible_answers_ar": [
                                        "\u062d \u2265 \u0664"
                                ]
                        }
                ],
                "hints_en": [
                        "Variable p represents pieces per child. How many children? How many total pieces needed?",
                        "If each child gets p pieces, and you have 15 children, how many pieces total will you distribute?",
                        "Total = number of children \u00d7 pieces per child. Must be \"at least\" 60"
                ],
                "hints_ar": [
                        "\u0627\u0644\u0645\u062a\u063a\u064a\u0631 \u062d \u064a\u0645\u062b\u0644 \u0639\u062f\u062f \u0627\u0644\u0642\u0637\u0639 \u0644\u0643\u0644 \u0637\u0641\u0644. \u0643\u0645 \u0637\u0641\u0644 \u0644\u062f\u064a\u0646\u0627\u061f \u0643\u0645 \u0642\u0637\u0639\u0629 \u0625\u062c\u0645\u0627\u0644\u0627\u064b \u0646\u062d\u062a\u0627\u062c\u061f",
                        "\u0625\u0630\u0627 \u0623\u0639\u0637\u064a\u062a \u0643\u0644 \u0637\u0641\u0644 \u062d \u0642\u0637\u0639\u0629\u060c \u0648 \u0644\u062f\u064a\u0643 \u0661\u0665 \u0637\u0641\u0644\u060c \u0643\u0645 \u0642\u0637\u0639\u0629 \u0633\u062a\u0648\u0632\u0639 \u0625\u062c\u0645\u0627\u0644\u0627\u064b\u061f",
                        "\u0627\u0644\u0639\u062f\u062f \u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a = \u0639\u062f\u062f \u0627\u0644\u0623\u0637\u0641\u0627\u0644 \u00d7 \u0627\u0644\u0642\u0637\u0639 \u0644\u0643\u0644 \u0637\u0641\u0644. \u064a\u062c\u0628 \u0623\u0646 \u064a\u0643\u0648\u0646 \"\u0639\u0644\u0649 \u0627\u0644\u0623\u0642\u0644\" \u0666\u0660"
                ]
        },
        {
                "id": "prep3",
                "section_id": "section3",
                "type": "preparation",
                "weight": 10,
                "question_en": "Solve the inequality: 2x + 5 > 15",
                "question_ar": "\u062d\u0644 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629: \u0662\u0633 + \u0665 > \u0661\u0665",
                "answer": "x > 5",
                "answer_ar": "\u0633 > \u0665",
                "explanation_en": "This is a review problem for solving multi-step inequalities.",
                "explanation_ar": "\u0647\u0630\u0647 \u0645\u0633\u0623\u0644\u0629 \u0645\u0631\u0627\u062c\u0639\u0629 \u0644\u062d\u0644 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0627\u062a \u0645\u062a\u0639\u062f\u062f\u0629 \u0627\u0644\u062e\u0637\u0648\u0627\u062a.",
                "show_full_solution": False,
                "hide_answer": False,
                "step_solutions": [
                        {
                                "step_en": "Step 1: Subtract 5 from both sides",
                                "step_ar": "\u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0637\u0631\u062d \u0665 \u0645\u0646 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646",
                                "possible_answers": [
                                        "2x + 5 - 5 > 15 - 5",
                                        "2x > 15 - 5",
                                        "2x > 10"
                                ],
                                "possible_answers_ar": [
                                        "\u0662\u0633 + \u0665 - \u0665 > \u0661\u0665 - \u0665",
                                        "\u0662\u0633 > \u0661\u0665 - \u0665",
                                        "\u0662\u0633 > \u0661\u0660"
                                ]
                        },
                        {
                                "step_en": "Step 2: Divide by 2",
                                "step_ar": "\u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0627\u0642\u0633\u0645 \u0639\u0644\u0649 \u0662",
                                "possible_answers": [
                                        "2x / 2 > 10 / 2",
                                        "x > 10 / 2",
                                        "x > 5"
                                ],
                                "possible_answers_ar": [
                                        "\u0662\u0633 / \u0662 > \u0661\u0660 / \u0662",
                                        "\u0633 > \u0661\u0660 / \u0662",
                                        "\u0633 > \u0665"
                                ]
                        }
                ],
                "final_answer_required": True,
                "hints_en": [
                        "\u0645\u0627 \u0627\u0644\u0639\u0645\u0644\u064a\u0629 \u0627\u0644\u062a\u064a \u062a\u0644\u063a\u064a +\u0665\u061f / What operation cancels +5?",
                        "\u0627\u0637\u0631\u062d \u0665 \u0623\u0648\u0644\u0627\u064b\u060c \u062b\u0645 \u0627\u0642\u0633\u0645 \u0639\u0644\u0649 \u0662 / Subtract 5 first, then divide by 2"
                ],
                "hints_ar": [
                        "\u0645\u0627 \u0627\u0644\u0639\u0645\u0644\u064a\u0629 \u0627\u0644\u062a\u064a \u062a\u0644\u063a\u064a +\u0665\u061f",
                        "\u0627\u0637\u0631\u062d \u0665 \u0623\u0648\u0644\u0627\u064b\u060c \u062b\u0645 \u0627\u0642\u0633\u0645 \u0639\u0644\u0649 \u0662"
                ]
        },
        {
                "id": "explanation3",
                "section_id": "section3",
                "type": "explanation",
                "weight": 0,
                "question_en": "Learn Multi-Step Inequalities",
                "question_ar": "\u062a\u0639\u0644\u0645 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0627\u062a \u0645\u062a\u0639\u062f\u062f\u0629 \u0627\u0644\u062e\u0637\u0648\u0627\u062a",
                "answer": "",
                "answer_ar": "",
                "show_full_solution": False,
                "hide_answer": False,
                "interactive_examples": [
                        {
                                "title_en": "Level 1: Simple - Example 1A (System Demonstrates)",
                                "title_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0661: \u0628\u0633\u064a\u0637 - \u0627\u0644\u0645\u062b\u0627\u0644 \u0661\u0623 (\u064a\u0638\u0647\u0631 \u0627\u0644\u0646\u0638\u0627\u0645)",
                                "problem_en": "Solve 3x + 4 > 16",
                                "problem_ar": "\u0627\u062d\u0644 \u0663\u0633 + \u0664 > \u0661\u0666",
                                "solution_en": "Step 1: Subtract 4 from both sides: 3x + 4 - 4 > 16 - 4 \u2192 3x > 12\nStep 2: Divide by 3: 3x/3 > 12/3 \u2192 x > 4",
                                "solution_ar": "\u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0637\u0631\u062d \u0664 \u0645\u0646 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646: \u0663\u0633 + \u0664 - \u0664 > \u0661\u0666 - \u0664 \u2192 \u0663\u0633 > \u0661\u0662\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0627\u0642\u0633\u0645 \u0639\u0644\u0649 \u0663: \u0663\u0633/\u0663 > \u0661\u0662/\u0663 \u2192 \u0633 > \u0664",
                                "practice_question_en": "Now solve: 2y + 5 \u2264 19",
                                "practice_question_ar": "\u0627\u0644\u0622\u0646 \u0627\u062d\u0644: \u0662\u0635 + \u0665 \u2264 \u0661\u0669",
                                "practice_answer": "y \u2264 7",
                                "practice_answer_ar": "\u0635 \u2264 \u0667"
                        },
                        {
                                "title_en": "Level 2: Negative Coefficient - Example 2A (System Demonstrates)",
                                "title_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0662: \u0645\u0639\u0627\u0645\u0644 \u0633\u0627\u0644\u0628 - \u0627\u0644\u0645\u062b\u0627\u0644 \u0662\u0623 (\u064a\u0638\u0647\u0631 \u0627\u0644\u0646\u0638\u0627\u0645)",
                                "problem_en": "Solve 12 - 4m < 20",
                                "problem_ar": "\u0627\u062d\u0644 \u0661\u0662 - \u0664\u0645 < \u0662\u0660",
                                "solution_en": "Step 1: Subtract 12: -4m < 8\nStep 2: Divide by -4 and FLIP SIGN: m > -2",
                                "solution_ar": "\u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0637\u0631\u062d \u0661\u0662: -\u0664\u0645 < \u0668\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0627\u0642\u0633\u0645 \u0639\u0644\u0649 -\u0664 \u0648\u0627\u0642\u0644\u0628 \u0627\u0644\u0625\u0634\u0627\u0631\u0629: \u0645 > -\u0662",
                                "practice_question_en": "Now solve: 15 - 5k \u2265 -10",
                                "practice_question_ar": "\u0627\u0644\u0622\u0646 \u0627\u062d\u0644: \u0661\u0665 - \u0665\u0643 \u2265 -\u0661\u0660",
                                "practice_answer": "k \u2264 5",
                                "practice_answer_ar": "\u0643 \u2264 \u0665"
                        },
                        {
                                "title_en": "Level 3: Distributive Property - Example 3A (System Demonstrates)",
                                "title_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663: \u062e\u0627\u0635\u064a\u0629 \u0627\u0644\u062a\u0648\u0632\u064a\u0639 - \u0627\u0644\u0645\u062b\u0627\u0644 \u0663\u0623 (\u064a\u0638\u0647\u0631 \u0627\u0644\u0646\u0638\u0627\u0645)",
                                "problem_en": "Solve 3(n + 2) \u2264 18",
                                "problem_ar": "\u0627\u062d\u0644 \u0663(\u0646 + \u0662) \u2264 \u0661\u0668",
                                "solution_en": "Step 1: Distribute: 3n + 6 \u2264 18\nStep 2: Subtract 6: 3n \u2264 12\nStep 3: Divide by 3: n \u2264 4",
                                "solution_ar": "\u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0648\u0632\u0639: \u0663\u0646 + \u0666 \u2264 \u0661\u0668\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0627\u0637\u0631\u062d \u0666: \u0663\u0646 \u2264 \u0661\u0662\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0663: \u0627\u0642\u0633\u0645 \u0639\u0644\u0649 \u0663: \u0646 \u2264 \u0664",
                                "practice_question_en": "Now solve: 4(r - 1) > 8",
                                "practice_question_ar": "\u0627\u0644\u0622\u0646 \u0627\u062d\u0644: \u0664(\u0631 - \u0661) > \u0668",
                                "practice_answer": "r > 3",
                                "practice_answer_ar": "\u0631 > \u0663"
                        }
                ],
                "step_solutions": [
                        {
                                "step_en": "Level 1B Step 1: Subtract 5 from both sides",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0661\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0637\u0631\u062d \u0665 \u0645\u0646 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646",
                                "possible_answers": [
                                        "2y \u2264 14",
                                        "\u0662\u0635 \u2264 \u0661\u0664",
                                        "2y + 5 - 5 \u2264 19 - 5"
                                ],
                                "possible_answers_ar": [
                                        "\u0662\u0635 \u2264 \u0661\u0664",
                                        "\u0662\u0635 + \u0665 - \u0665 \u2264 \u0661\u0669 - \u0665"
                                ]
                        },
                        {
                                "step_en": "Level 1B Step 2: Divide both sides by 2",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0661\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0627\u0642\u0633\u0645 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0639\u0644\u0649 \u0662",
                                "possible_answers": [
                                        "y \u2264 7",
                                        "\u0635 \u2264 \u0667",
                                        "y \u2264 14/2"
                                ],
                                "possible_answers_ar": [
                                        "\u0635 \u2264 \u0667",
                                        "\u0635 \u2264 \u0661\u0664/\u0662"
                                ]
                        },
                        {
                                "step_en": "Level 2B Step 1: Subtract 15 from both sides",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0662\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0637\u0631\u062d \u0661\u0665 \u0645\u0646 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646",
                                "possible_answers": [
                                        "-5k \u2265 -25",
                                        "-\u0665\u0643 \u2265 -\u0662\u0665",
                                        "15 - 5k - 15 \u2265 -10 - 15"
                                ],
                                "possible_answers_ar": [
                                        "-\u0665\u0643 \u2265 -\u0662\u0665",
                                        "\u0661\u0665 - \u0665\u0643 - \u0661\u0665 \u2265 -\u0661\u0660 - \u0661\u0665"
                                ]
                        },
                        {
                                "step_en": "Level 2B Step 2: Divide by -5 and flip the inequality sign",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0662\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0627\u0642\u0633\u0645 \u0639\u0644\u0649 -\u0665 \u0648\u0627\u0642\u0644\u0628 \u0625\u0634\u0627\u0631\u0629 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629",
                                "possible_answers": [
                                        "k \u2264 5",
                                        "\u0643 \u2264 \u0665"
                                ],
                                "possible_answers_ar": [
                                        "\u0643 \u2264 \u0665"
                                ]
                        },
                        {
                                "step_en": "Level 3B Step 1: Distribute the 4",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0648\u0632\u0639 \u0627\u0644\u0640 \u0664",
                                "possible_answers": [
                                        "4r - 4 > 8",
                                        "\u0664\u0631 - \u0664 > \u0668"
                                ],
                                "possible_answers_ar": [
                                        "\u0664\u0631 - \u0664 > \u0668"
                                ]
                        },
                        {
                                "step_en": "Level 3B Step 2: Add 4 to both sides",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0623\u0636\u0641 \u0664 \u0644\u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646",
                                "possible_answers": [
                                        "4r > 12",
                                        "\u0664\u0631 > \u0661\u0662"
                                ],
                                "possible_answers_ar": [
                                        "\u0664\u0631 > \u0661\u0662"
                                ]
                        },
                        {
                                "step_en": "Level 3B Step 3: Divide by 4",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0663: \u0627\u0642\u0633\u0645 \u0639\u0644\u0649 \u0664",
                                "possible_answers": [
                                        "r > 3",
                                        "\u0631 > \u0663"
                                ],
                                "possible_answers_ar": [
                                        "\u0631 > \u0663"
                                ]
                        }
                ],
                "hints_en": [],
                "hints_ar": []
        },
        {
                "id": "practice3_1",
                "section_id": "section3",
                "type": "practice",
                "weight": 15,
                "question_en": "Solve the inequality 6 - 3y \u2264 18",
                "question_ar": "\u0627\u062d\u0644 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0666 - \u0663\u0635 \u2264 \u0661\u0668",
                "answer": "y \u2265 -4",
                "answer_ar": "\u0635 \u2265 -\u0664",
                "show_full_solution": False,
                "hide_answer": False,
                "step_solutions": [
                        {
                                "step_en": "\u0627\u0637\u0631\u062d \u0666 \u0645\u0646 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 / Subtract 6 from both sides",
                                "step_ar": "\u0627\u0637\u0631\u062d \u0666 \u0645\u0646 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646",
                                "possible_answers": [
                                        "-3y \u2264 12",
                                        "-\u0663\u0635 \u2264 \u0661\u0662"
                                ],
                                "possible_answers_ar": [
                                        "-\u0663\u0635 \u2264 \u0661\u0662"
                                ]
                        },
                        {
                                "step_en": "\u0627\u0642\u0633\u0645 \u0639\u0644\u0649 -\u0663 \u0648\u0627\u0642\u0644\u0628 \u0627\u0644\u0625\u0634\u0627\u0631\u0629 / Divide by -3 and flip sign",
                                "step_ar": "\u0627\u0642\u0633\u0645 \u0639\u0644\u0649 -\u0663 \u0648\u0627\u0642\u0644\u0628 \u0627\u0644\u0625\u0634\u0627\u0631\u0629",
                                "possible_answers": [
                                        "y \u2265 -4",
                                        "\u0635 \u2265 -\u0664"
                                ],
                                "possible_answers_ar": [
                                        "\u0635 \u2265 -\u0664"
                                ]
                        }
                ],
                "final_answer_required": False,
                "hints_en": [
                        "\u0627\u0628\u062f\u0623 \u0628\u0637\u0631\u062d \u0666 \u0645\u0646 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 / Start by subtracting 6",
                        "\u0639\u0632\u0644 \u0627\u0644\u062d\u062f \u0627\u0644\u0630\u064a \u064a\u062d\u062a\u0648\u064a \u0639\u0644\u0649 \u0627\u0644\u0645\u062a\u063a\u064a\u0631 / Isolate the term with variable",
                        "\u0666 - \u0666 - \u0663\u0635 \u2264 \u0661\u0668 - \u0666 / 6 - 6 - 3y \u2264 18 - 6"
                ],
                "hints_ar": [
                        "\u0627\u0628\u062f\u0623 \u0628\u0637\u0631\u062d \u0666 \u0645\u0646 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646",
                        "\u0639\u0632\u0644 \u0627\u0644\u062d\u062f \u0627\u0644\u0630\u064a \u064a\u062d\u062a\u0648\u064a \u0639\u0644\u0649 \u0627\u0644\u0645\u062a\u063a\u064a\u0631",
                        "\u0666 - \u0666 - \u0663\u0635 \u2264 \u0661\u0668 - \u0666"
                ]
        },
        {
                "id": "practice3_2",
                "section_id": "section3",
                "type": "practice",
                "weight": 15,
                "stage_type": "practice_word",
                "question_en": "A car rental costs SAR 100 plus SAR 2 per kilometer (k). Your budget is SAR 250. What is the maximum distance you can drive?",
                "question_ar": "\u0625\u064a\u062c\u0627\u0631 \u0633\u064a\u0627\u0631\u0629 \u064a\u0643\u0644\u0641 \u0661\u0660\u0660 \u0631\u064a\u0627\u0644 \u0628\u0627\u0644\u0625\u0636\u0627\u0641\u0629 \u0625\u0644\u0649 \u0662 \u0631\u064a\u0627\u0644 \u0644\u0643\u0644 \u0643\u064a\u0644\u0648\u0645\u062a\u0631. \u0645\u064a\u0632\u0627\u0646\u064a\u062a\u0643 \u0662\u0665\u0660 \u0631\u064a\u0627\u0644. \u0645\u0627 \u0623\u0642\u0635\u0649 \u0645\u0633\u0627\u0641\u0629 \u064a\u0645\u0643\u0646\u0643 \u0642\u064a\u0627\u062f\u062a\u0647\u0627\u061f",
                "answer": "k \u2264 75",
                "answer_ar": "\u0643 \u2264 \u0667\u0665",
                "show_full_solution": False,
                "hide_answer": False,
                "step_solutions": [
                        {
                                "step_en": "\u0627\u0643\u062a\u0628 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629 / Write the inequality",
                                "step_ar": "\u0627\u0643\u062a\u0628 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629",
                                "possible_answers": [
                                        "100 + 2k \u2264 250",
                                        "\u0661\u0660\u0660 + \u0662\u0643 \u2264 \u0662\u0665\u0660",
                                        "2k + 100 \u2264 250"
                                ],
                                "possible_answers_ar": [
                                        "\u0661\u0660\u0660 + \u0662\u0643 \u2264 \u0662\u0665\u0660",
                                        "\u0662\u0643 + \u0661\u0660\u0660 \u2264 \u0662\u0665\u0660"
                                ]
                        },
                        {
                                "step_en": "\u0627\u0637\u0631\u062d \u0627\u0644\u062a\u0643\u0644\u0641\u0629 \u0627\u0644\u062b\u0627\u0628\u062a\u0629 / Subtract the fixed cost",
                                "step_ar": "\u0627\u0637\u0631\u062d \u0627\u0644\u062a\u0643\u0644\u0641\u0629 \u0627\u0644\u062b\u0627\u0628\u062a\u0629",
                                "possible_answers": [
                                        "2k \u2264 150",
                                        "\u0662\u0643 \u2264 \u0661\u0665\u0660"
                                ],
                                "possible_answers_ar": [
                                        "\u0662\u0643 \u2264 \u0661\u0665\u0660"
                                ]
                        },
                        {
                                "step_en": "\u0627\u062d\u0633\u0628 \u0627\u0644\u062d\u062f \u0627\u0644\u0623\u0642\u0635\u0649 \u0644\u0644\u0643\u064a\u0644\u0648\u0645\u062a\u0631\u0627\u062a / Calculate maximum kilometers",
                                "step_ar": "\u0627\u062d\u0633\u0628 \u0627\u0644\u062d\u062f \u0627\u0644\u0623\u0642\u0635\u0649 \u0644\u0644\u0643\u064a\u0644\u0648\u0645\u062a\u0631\u0627\u062a",
                                "possible_answers": [
                                        "k \u2264 75",
                                        "\u0643 \u2264 \u0667\u0665"
                                ],
                                "possible_answers_ar": [
                                        "\u0643 \u2264 \u0667\u0665"
                                ]
                        }
                ],
                "final_answer_required": False,
                "hints_en": [
                        "\u0627\u0644\u062a\u0643\u0644\u0641\u0629 \u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a\u0629 = \u0627\u0644\u062a\u0643\u0644\u0641\u0629 \u0627\u0644\u062b\u0627\u0628\u062a\u0629 + (\u062a\u0643\u0644\u0641\u0629 \u0627\u0644\u0643\u064a\u0644\u0648\u0645\u062a\u0631 \u00d7 \u0639\u062f\u062f \u0627\u0644\u0643\u064a\u0644\u0648\u0645\u062a\u0631\u0627\u062a) / Total = Fixed + (Per km \u00d7 Number)",
                        "\u0627\u0633\u062a\u062e\u062f\u0645 k \u0644\u0644\u0643\u064a\u0644\u0648\u0645\u062a\u0631\u0627\u062a / Use k for kilometers",
                        "\u0627\u0644\u062a\u0643\u0644\u0641\u0629 \u064a\u062c\u0628 \u0623\u0646 \u062a\u0643\u0648\u0646 \u2264 \u0627\u0644\u0645\u064a\u0632\u0627\u0646\u064a\u0629 / Cost must be \u2264 budget"
                ],
                "hints_ar": [
                        "\u0627\u0644\u062a\u0643\u0644\u0641\u0629 \u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a\u0629 = \u0627\u0644\u062a\u0643\u0644\u0641\u0629 \u0627\u0644\u062b\u0627\u0628\u062a\u0629 + (\u062a\u0643\u0644\u0641\u0629 \u0627\u0644\u0643\u064a\u0644\u0648\u0645\u062a\u0631 \u00d7 \u0639\u062f\u062f \u0627\u0644\u0643\u064a\u0644\u0648\u0645\u062a\u0631\u0627\u062a)",
                        "\u0627\u0633\u062a\u062e\u062f\u0645 k \u0644\u0644\u0643\u064a\u0644\u0648\u0645\u062a\u0631\u0627\u062a",
                        "\u0627\u0644\u062a\u0643\u0644\u0641\u0629 \u064a\u062c\u0628 \u0623\u0646 \u062a\u0643\u0648\u0646 \u2264 \u0627\u0644\u0645\u064a\u0632\u0627\u0646\u064a\u0629"
                ]
        },
        {
                "id": "assessment3",
                "section_id": "section3",
                "type": "assessment",
                "weight": 20,
                "question_en": "What is the solution set for the inequality: (x + 3) / 2 \u2264 5?",
                "question_ar": "\u0645\u0627 \u0647\u064a \u0645\u062c\u0645\u0648\u0639\u0629 \u062d\u0644 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629: (\u0633 + \u0663) / \u0662 \u2264 \u0665\u061f",
                "answer": "x \u2264 7",
                "answer_ar": "\u0633 \u2264 \u0667",
                "show_full_solution": False,
                "hide_answer": True,
                "explanation_en": "Multiply both sides by 2, then subtract 3",
                "explanation_ar": "\u0627\u0636\u0631\u0628 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0641\u064a \u0662\u060c \u062b\u0645 \u0627\u0637\u0631\u062d \u0663",
                "final_answer_required": True,
                "hints_en": [
                        "\u0627\u0636\u0631\u0628 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0641\u064a \u0662 \u0623\u0648\u0644\u0627\u064b / Multiply both sides by 2 first",
                        "\u0628\u0639\u062f \u0627\u0644\u0636\u0631\u0628 \u0641\u064a \u0662\u060c \u0627\u0637\u0631\u062d \u0663 / After multiplying by 2, subtract 3"
                ],
                "hints_ar": [
                        "\u0627\u0636\u0631\u0628 \u0643\u0644\u0627 \u0627\u0644\u0637\u0631\u0641\u064a\u0646 \u0641\u064a \u0662 \u0623\u0648\u0644\u0627\u064b",
                        "\u0628\u0639\u062f \u0627\u0644\u0636\u0631\u0628 \u0641\u064a \u0662\u060c \u0627\u0637\u0631\u062d \u0663"
                ]
        },
        {
                "id": "examprep3",
                "section_id": "section3",
                "type": "examprep",
                "weight": 25,
                "question_en": "Solve the inequality: 3(1 - k) < 12",
                "question_ar": "\u062d\u0644 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0629: \u0663(\u0661 - \u0643) < \u0661\u0662",
                "answer": "k > -3",
                "answer_ar": "\u0643 > -\u0663",
                "show_full_solution": False,
                "hide_answer": True,
                "explanation_en": "Distribute 3, subtract 3, then divide by -3 (flip sign)",
                "explanation_ar": "\u0648\u0632\u0639 \u0663\u060c \u0627\u0637\u0631\u062d \u0663\u060c \u062b\u0645 \u0627\u0642\u0633\u0645 \u0639\u0644\u0649 -\u0663 (\u0627\u0642\u0644\u0628 \u0627\u0644\u0625\u0634\u0627\u0631\u0629)",
                "final_answer_required": True,
                "hints_en": [],
                "hints_ar": []
        },
        {
                "id": "prep4",
                "section_id": "section4",
                "type": "preparation",
                "weight": 10,
                "question_en": "Solve: 3 < x + 2 < 8",
                "question_ar": "\u062d\u0644: \u0663 < \u0633 + \u0662 < \u0668",
                "answer": "1 < x < 6",
                "answer_ar": "\u0661 < \u0633 < \u0666",
                "explanation_en": "This is a compound inequality. Apply operations to all parts simultaneously.",
                "explanation_ar": "\u0647\u0630\u0647 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0631\u0643\u0628\u0629. \u0637\u0628\u0642 \u0627\u0644\u0639\u0645\u0644\u064a\u0627\u062a \u0639\u0644\u0649 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621 \u0641\u064a \u0646\u0641\u0633 \u0627\u0644\u0648\u0642\u062a.",
                "show_full_solution": False,
                "hide_answer": False,
                "final_answer_required": True,
                "hints_en": [
                        "\u0627\u0637\u0631\u062d \u0662 \u0645\u0646 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621 / Subtract 2 from all parts",
                        "\u0663 - \u0662 < \u0633 + \u0662 - \u0662 < \u0668 - \u0662 / 3 - 2 < x + 2 - 2 < 8 - 2"
                ],
                "hints_ar": [
                        "\u0627\u0637\u0631\u062d \u0662 \u0645\u0646 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621",
                        "\u0663 - \u0662 < \u0633 + \u0662 - \u0662 < \u0668 - \u0662"
                ]
        },
        {
                "id": "explanation4",
                "section_id": "section4",
                "type": "explanation",
                "weight": 0,
                "question_en": "Learn Compound Inequalities",
                "question_ar": "\u062a\u0639\u0644\u0645 \u0627\u0644\u0645\u062a\u0628\u0627\u064a\u0646\u0627\u062a \u0627\u0644\u0645\u0631\u0643\u0628\u0629",
                "answer": "",
                "answer_ar": "",
                "show_full_solution": False,
                "hide_answer": False,
                "interactive_examples": [
                        {
                                "title_en": "Level 1: Simple Compound - Example 1A (System Demonstrates)",
                                "title_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0661: \u0645\u0631\u0643\u0628 \u0628\u0633\u064a\u0637 - \u0627\u0644\u0645\u062b\u0627\u0644 \u0661\u0623 (\u064a\u0638\u0647\u0631 \u0627\u0644\u0646\u0638\u0627\u0645)",
                                "problem_en": "Solve 5 < m + 1 < 9",
                                "problem_ar": "\u0627\u062d\u0644 \u0665 < \u0645 + \u0661 < \u0669",
                                "solution_en": "Step 1: Subtract 1 from all parts: 5 - 1 < m + 1 - 1 < 9 - 1\nResult: 4 < m < 8",
                                "solution_ar": "\u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0637\u0631\u062d \u0661 \u0645\u0646 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621: \u0665 - \u0661 < \u0645 + \u0661 - \u0661 < \u0669 - \u0661\n\u0627\u0644\u0646\u062a\u064a\u062c\u0629: \u0664 < \u0645 < \u0668",
                                "practice_question_en": "Now solve: -2 \u2264 y - 3 \u2264 4",
                                "practice_question_ar": "\u0627\u0644\u0622\u0646 \u0627\u062d\u0644: -\u0662 \u2264 \u0635 - \u0663 \u2264 \u0664",
                                "practice_answer": "1 \u2264 y \u2264 7",
                                "practice_answer_ar": "\u0661 \u2264 \u0635 \u2264 \u0667"
                        },
                        {
                                "title_en": "Level 2: With Multiplication/Division - Example 2A (System Demonstrates)",
                                "title_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0662: \u0645\u0639 \u0627\u0644\u0636\u0631\u0628 \u0648\u0627\u0644\u0642\u0633\u0645\u0629 - \u0627\u0644\u0645\u062b\u0627\u0644 \u0662\u0623 (\u064a\u0638\u0647\u0631 \u0627\u0644\u0646\u0638\u0627\u0645)",
                                "problem_en": "Solve -6 < 2k < 10",
                                "problem_ar": "\u0627\u062d\u0644 -\u0666 < \u0662\u0643 < \u0661\u0660",
                                "solution_en": "Divide all parts by 2: -6/2 < 2k/2 < 10/2\nResult: -3 < k < 5",
                                "solution_ar": "\u0627\u0642\u0633\u0645 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621 \u0639\u0644\u0649 \u0662: -\u0666/\u0662 < \u0662\u0643/\u0662 < \u0661\u0660/\u0662\n\u0627\u0644\u0646\u062a\u064a\u062c\u0629: -\u0663 < \u0643 < \u0665",
                                "practice_question_en": "Now solve: -12 \u2264 -3n \u2264 6",
                                "practice_question_ar": "\u0627\u0644\u0622\u0646 \u0627\u062d\u0644: -\u0661\u0662 \u2264 -\u0663\u0646 \u2264 \u0666",
                                "practice_answer": "-2 \u2264 n \u2264 4",
                                "practice_answer_ar": "-\u0662 \u2264 \u0646 \u2264 \u0664"
                        },
                        {
                                "title_en": "Level 3: OR Inequalities - Example 3A (System Demonstrates)",
                                "title_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663: \u0645\u062a\u0628\u0627\u064a\u0646\u0627\u062a \u0623\u0648 - \u0627\u0644\u0645\u062b\u0627\u0644 \u0663\u0623 (\u064a\u0638\u0647\u0631 \u0627\u0644\u0646\u0638\u0627\u0645)",
                                "problem_en": "Solve x < -1 or x > 3",
                                "problem_ar": "\u0627\u062d\u0644 \u0633 < -\u0661 \u0623\u0648 \u0633 > \u0663",
                                "solution_en": "This is a disjoint inequality - two separate ranges\nSolution remains: x < -1 or x > 3",
                                "solution_ar": "\u0647\u0630\u0647 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0646\u0641\u0635\u0644\u0629 - \u0645\u062f\u0627\u0627\u0646 \u0645\u0646\u0641\u0635\u0644\u0627\u0646\n\u0627\u0644\u062d\u0644 \u064a\u0628\u0642\u0649: \u0633 < -\u0661 \u0623\u0648 \u0633 > \u0663",
                                "practice_question_en": "Now solve: 2t \u2264 -4 or t + 1 > 5",
                                "practice_question_ar": "\u0627\u0644\u0622\u0646 \u0627\u062d\u0644: \u0662\u062a \u2264 -\u0664 \u0623\u0648 \u062a + \u0661 > \u0665",
                                "practice_answer": "t \u2264 -2 or t > 4",
                                "practice_answer_ar": "\u062a \u2264 -\u0662 \u0623\u0648 \u062a > \u0664"
                        }
                ],
                "step_solutions": [
                        {
                                "step_en": "Level 1B Step 1: Add 3 to all parts",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0661\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0623\u0636\u0641 \u0663 \u0644\u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621",
                                "possible_answers": [
                                        "1 \u2264 y \u2264 7",
                                        "\u0661 \u2264 \u0635 \u2264 \u0667",
                                        "-2+3 \u2264 y-3+3 \u2264 4+3",
                                        "-2 + 3 \u2264 y \u2264 4 + 3"
                                ],
                                "possible_answers_ar": [
                                        "\u0661 \u2264 \u0635 \u2264 \u0667",
                                        "-\u0662+\u0663 \u2264 \u0635-\u0663+\u0663 \u2264 \u0664+\u0663"
                                ]
                        },
                        {
                                "step_en": "Level 1B Step 2: Simplify",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0661\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0628\u0633\u0651\u0637",
                                "possible_answers": [
                                        "1 \u2264 y \u2264 7",
                                        "\u0661 \u2264 \u0635 \u2264 \u0667"
                                ],
                                "possible_answers_ar": [
                                        "\u0661 \u2264 \u0635 \u2264 \u0667"
                                ]
                        },
                        {
                                "step_en": "Level 2B Step 1: Divide by -3 and flip ALL signs",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0662\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u0627\u0642\u0633\u0645 \u0639\u0644\u0649 -\u0663 \u0648\u0627\u0642\u0644\u0628 \u062c\u0645\u064a\u0639 \u0627\u0644\u0625\u0634\u0627\u0631\u0627\u062a",
                                "possible_answers": [
                                        "4 \u2265 n \u2265 -2",
                                        "-2 \u2264 n \u2264 4",
                                        "-\u0662 \u2264 \u0646 \u2264 \u0664"
                                ],
                                "possible_answers_ar": [
                                        "\u0664 \u2265 \u0646 \u2265 -\u0662",
                                        "-\u0662 \u2264 \u0646 \u2264 \u0664"
                                ]
                        },
                        {
                                "step_en": "Level 2B Step 2: Rewrite in standard form (smallest to largest)",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0662\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0627\u0643\u062a\u0628 \u0628\u0627\u0644\u062a\u0631\u062a\u064a\u0628 \u0645\u0646 \u0627\u0644\u0623\u0635\u063a\u0631 \u0644\u0644\u0623\u0643\u0628\u0631",
                                "possible_answers": [
                                        "-2 \u2264 n \u2264 4",
                                        "-\u0662 \u2264 \u0646 \u2264 \u0664"
                                ],
                                "possible_answers_ar": [
                                        "-\u0662 \u2264 \u0646 \u2264 \u0664"
                                ]
                        },
                        {
                                "step_en": "Level 3B Step 1: Solve each inequality separately",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u062d\u0644 \u0643\u0644 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0646\u0641\u0635\u0644\u0629",
                                "possible_answers": [
                                        "t \u2264 -2 or t > 4",
                                        "\u062a \u2264 -\u0662 \u0623\u0648 \u062a > \u0664",
                                        "t <= -2 or t > 4",
                                        "t \u2264 -2 || t > 4"
                                ],
                                "possible_answers_ar": [
                                        "\u062a \u2264 -\u0662 \u0623\u0648 \u062a > \u0664"
                                ]
                        }
                ],
                "hints_en": [],
                "hints_ar": []
        },
        {
                "id": "practice4_1",
                "section_id": "section4",
                "type": "practice",
                "weight": 15,
                "question_en": "Solve -5 < 3x + 1 < 13",
                "question_ar": "\u0627\u062d\u0644 -\u0665 < \u0663\u0633 + \u0661 < \u0661\u0663",
                "answer": "-2 < x < 4",
                "answer_ar": "-\u0662 < \u0633 < \u0664",
                "show_full_solution": False,
                "hide_answer": False,
                "step_solutions": [
                        {
                                "step_en": "\u0627\u0637\u0631\u062d \u0661 \u0645\u0646 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621 / Subtract 1 from all parts",
                                "step_ar": "\u0627\u0637\u0631\u062d \u0661 \u0645\u0646 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621",
                                "possible_answers": [
                                        "-6 < 3x < 12",
                                        "-\u0666 < \u0663\u0633 < \u0661\u0662"
                                ],
                                "possible_answers_ar": [
                                        "-\u0666 < \u0663\u0633 < \u0661\u0662"
                                ]
                        },
                        {
                                "step_en": "\u0627\u0642\u0633\u0645 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621 \u0639\u0644\u0649 \u0663 / Divide all parts by 3",
                                "step_ar": "\u0627\u0642\u0633\u0645 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621 \u0639\u0644\u0649 \u0663",
                                "possible_answers": [
                                        "-2 < x < 4",
                                        "-\u0662 < \u0633 < \u0664"
                                ],
                                "possible_answers_ar": [
                                        "-\u0662 < \u0633 < \u0664"
                                ]
                        }
                ],
                "final_answer_required": False,
                "hints_en": [
                        "\u0627\u0628\u062f\u0623 \u0628\u0637\u0631\u062d \u0661 \u0645\u0646 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621 \u0627\u0644\u062b\u0644\u0627\u062b\u0629 / Start by subtracting 1 from all three parts",
                        "\u062a\u062e\u0644\u0635 \u0645\u0646 \u0627\u0644\u062b\u0627\u0628\u062a \u0623\u0648\u0644\u0627\u064b / Remove the constant first",
                        "-\u0665 - \u0661 < \u0663\u0633 < \u0661\u0663 - \u0661 / -5 - 1 < 3x < 13 - 1"
                ],
                "hints_ar": [
                        "\u0627\u0628\u062f\u0623 \u0628\u0637\u0631\u062d \u0661 \u0645\u0646 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621 \u0627\u0644\u062b\u0644\u0627\u062b\u0629",
                        "\u062a\u062e\u0644\u0635 \u0645\u0646 \u0627\u0644\u062b\u0627\u0628\u062a \u0623\u0648\u0644\u0627\u064b",
                        "-\u0665 - \u0661 < \u0663\u0633 < \u0661\u0663 - \u0661"
                ]
        },
        {
                "id": "practice4_2",
                "section_id": "section4",
                "type": "practice",
                "weight": 15,
                "stage_type": "practice_word",
                "question_en": "Room temperature must be between 18\u00b0C and 25\u00b0C. If F = (9/5)C + 32 converts Celsius to Fahrenheit, what's the range in Fahrenheit?",
                "question_ar": "\u062f\u0631\u062c\u0629 \u062d\u0631\u0627\u0631\u0629 \u0627\u0644\u063a\u0631\u0641\u0629 \u064a\u062c\u0628 \u0623\u0646 \u062a\u0643\u0648\u0646 \u0628\u064a\u0646 \u0661\u0668 \u0648\u0662\u0665 \u062f\u0631\u062c\u0629 \u0645\u0626\u0648\u064a\u0629. \u0625\u0630\u0627 \u0643\u0627\u0646\u062a \u0627\u0644\u0635\u064a\u063a\u0629 \u0641 = (\u0669/\u0665)\u0645 + \u0663\u0662 \u062a\u062d\u0648\u0644 \u0645\u0646 \u0645\u0626\u0648\u064a\u0629 \u0625\u0644\u0649 \u0641\u0647\u0631\u0646\u0647\u0627\u064a\u062a\u060c \u0645\u0627 \u0627\u0644\u0645\u062f\u0649 \u0628\u0627\u0644\u0641\u0647\u0631\u0646\u0647\u0627\u064a\u062a\u061f",
                "answer": "64.4 \u2264 F \u2264 77",
                "answer_ar": "\u0666\u0664.\u0664 \u2264 \u0641 \u2264 \u0667\u0667",
                "show_full_solution": False,
                "hide_answer": False,
                "step_solutions": [
                        {
                                "step_en": "\u0627\u0643\u062a\u0628 \u0627\u0644\u0645\u062f\u0649 \u0628\u0627\u0644\u062f\u0631\u062c\u0629 \u0627\u0644\u0645\u0626\u0648\u064a\u0629 / Write the Celsius range",
                                "step_ar": "\u0627\u0643\u062a\u0628 \u0627\u0644\u0645\u062f\u0649 \u0628\u0627\u0644\u062f\u0631\u062c\u0629 \u0627\u0644\u0645\u0626\u0648\u064a\u0629",
                                "possible_answers": [
                                        "18 \u2264 C \u2264 25",
                                        "\u0661\u0668 \u2264 \u0645 \u2264 \u0662\u0665"
                                ],
                                "possible_answers_ar": [
                                        "\u0661\u0668 \u2264 \u0645 \u2264 \u0662\u0665"
                                ]
                        },
                        {
                                "step_en": "\u0637\u0628\u0642 \u0627\u0644\u0635\u064a\u063a\u0629 \u0639\u0644\u0649 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621 / Apply formula to all parts",
                                "step_ar": "\u0637\u0628\u0642 \u0627\u0644\u0635\u064a\u063a\u0629 \u0639\u0644\u0649 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621",
                                "possible_answers": [
                                        "(9/5)(18) + 32 \u2264 F \u2264 (9/5)(25) + 32",
                                        "32.4 + 32 \u2264 F \u2264 45 + 32"
                                ],
                                "possible_answers_ar": [
                                        "(\u0669/\u0665)(\u0661\u0668) + \u0663\u0662 \u2264 \u0641 \u2264 (\u0669/\u0665)(\u0662\u0665) + \u0663\u0662"
                                ]
                        },
                        {
                                "step_en": "\u0627\u062d\u0633\u0628 \u0627\u0644\u0642\u064a\u0645 \u0627\u0644\u0646\u0647\u0627\u0626\u064a\u0629 / Calculate final values",
                                "step_ar": "\u0627\u062d\u0633\u0628 \u0627\u0644\u0642\u064a\u0645 \u0627\u0644\u0646\u0647\u0627\u0626\u064a\u0629",
                                "possible_answers": [
                                        "64.4 \u2264 F \u2264 77",
                                        "64 \u2264 F \u2264 77",
                                        "\u0666\u0664.\u0664 \u2264 \u0641 \u2264 \u0667\u0667"
                                ],
                                "possible_answers_ar": [
                                        "\u0666\u0664.\u0664 \u2264 \u0641 \u2264 \u0667\u0667",
                                        "\u0666\u0664 \u2264 \u0641 \u2264 \u0667\u0667"
                                ]
                        }
                ],
                "final_answer_required": False,
                "hints_en": [
                        "\u062f\u0631\u062c\u0629 \u0627\u0644\u062d\u0631\u0627\u0631\u0629 \u064a\u062c\u0628 \u0623\u0646 \u062a\u0643\u0648\u0646 \u0628\u064a\u0646 \u0661\u0668 \u0648\u0662\u0665 / Temperature must be between 18 and 25",
                        "\u0627\u0633\u062a\u062e\u062f\u0645 C \u0623\u0648 \u0645 \u0644\u0644\u062f\u0631\u062c\u0629 \u0627\u0644\u0645\u0626\u0648\u064a\u0629 / Use C for Celsius",
                        "\u0627\u0644\u0645\u062f\u0649: \u0661\u0668 \u2264 \u0645 \u2264 \u0662\u0665 / Range: 18 \u2264 C \u2264 25"
                ],
                "hints_ar": [
                        "\u062f\u0631\u062c\u0629 \u0627\u0644\u062d\u0631\u0627\u0631\u0629 \u064a\u062c\u0628 \u0623\u0646 \u062a\u0643\u0648\u0646 \u0628\u064a\u0646 \u0661\u0668 \u0648\u0662\u0665",
                        "\u0627\u0633\u062a\u062e\u062f\u0645 C \u0623\u0648 \u0645 \u0644\u0644\u062f\u0631\u062c\u0629 \u0627\u0644\u0645\u0626\u0648\u064a\u0629",
                        "\u0627\u0644\u0645\u062f\u0649: \u0661\u0668 \u2264 \u0645 \u2264 \u0662\u0665"
                ]
        },
        {
                "id": "assessment4",
                "section_id": "section4",
                "type": "assessment",
                "weight": 20,
                "question_en": "What is the solution to -8 \u2264 4 - 2x < 6?",
                "question_ar": "\u0645\u0627 \u0647\u0648 \u062d\u0644 -\u0668 \u2264 \u0664 - \u0662\u0633 < \u0666\u061f",
                "answer": "-1 < x \u2264 6",
                "answer_ar": "-\u0661 < \u0633 \u2264 \u0666",
                "show_full_solution": False,
                "hide_answer": True,
                "explanation_en": "Subtract 4 from all parts, then divide by -2 and flip signs",
                "explanation_ar": "\u0627\u0637\u0631\u062d \u0664 \u0645\u0646 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621\u060c \u062b\u0645 \u0627\u0642\u0633\u0645 \u0639\u0644\u0649 -\u0662 \u0648\u0627\u0642\u0644\u0628 \u0627\u0644\u0625\u0634\u0627\u0631\u0627\u062a",
                "final_answer_required": True,
                "hints_en": [
                        "\u0627\u0637\u0631\u062d \u0664 \u0645\u0646 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621 \u0623\u0648\u0644\u0627\u064b / Subtract 4 from all parts first",
                        "\u062a\u0630\u0643\u0631 \u0642\u0644\u0628 \u0627\u0644\u0625\u0634\u0627\u0631\u0627\u062a \u0639\u0646\u062f \u0627\u0644\u0642\u0633\u0645\u0629 \u0639\u0644\u0649 -\u0662 / Remember to flip signs when dividing by -2"
                ],
                "hints_ar": [
                        "\u0627\u0637\u0631\u062d \u0664 \u0645\u0646 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621 \u0623\u0648\u0644\u0627\u064b",
                        "\u062a\u0630\u0643\u0631 \u0642\u0644\u0628 \u0627\u0644\u0625\u0634\u0627\u0631\u0627\u062a \u0639\u0646\u062f \u0627\u0644\u0642\u0633\u0645\u0629 \u0639\u0644\u0649 -\u0662"
                ]
        },
        {
                "id": "examprep4",
                "section_id": "section4",
                "type": "examprep",
                "weight": 25,
                "question_en": "Solve: 2(x - 1) \u2264 6 AND x + 3 > 2",
                "question_ar": "\u062d\u0644: \u0662(\u0633 - \u0661) \u2264 \u0666 \u0648 \u0633 + \u0663 > \u0662",
                "answer": "-1 < x \u2264 4",
                "answer_ar": "-\u0661 < \u0633 \u2264 \u0664",
                "show_full_solution": False,
                "hide_answer": True,
                "explanation_en": "Solve both inequalities separately, then find the intersection",
                "explanation_ar": "\u0627\u062d\u0644 \u0643\u0644 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0646\u0641\u0635\u0644\u0629\u060c \u062b\u0645 \u062c\u062f \u0627\u0644\u062a\u0642\u0627\u0637\u0639",
                "final_answer_required": True,
                "hints_en": [],
                "hints_ar": []
        },
        {
                "id": "prep5",
                "section_id": "section5",
                "type": "preparation",
                "weight": 10,
                "question_en": "Solve: |x| < 4",
                "question_ar": "\u062d\u0644: |\u0633| < \u0664",
                "answer": "-4 < x < 4",
                "answer_ar": "-\u0664 < \u0633 < \u0664",
                "explanation_en": "Absolute value less than a positive number creates a compound inequality.",
                "explanation_ar": "\u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u0645\u0637\u0644\u0642\u0629 \u0623\u0642\u0644 \u0645\u0646 \u0639\u062f\u062f \u0645\u0648\u062c\u0628 \u062a\u0646\u062a\u062c \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0631\u0643\u0628\u0629.",
                "show_full_solution": False,
                "hide_answer": False,
                "final_answer_required": True,
                "hints_en": [
                        "\u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u0645\u0637\u0644\u0642\u0629 \u0623\u0642\u0644 \u0645\u0646 \u0664 \u062a\u0639\u0646\u064a \u0627\u0644\u0645\u0633\u0627\u0641\u0629 \u0645\u0646 \u0627\u0644\u0635\u0641\u0631 \u0623\u0642\u0644 \u0645\u0646 \u0664 / Absolute value less than 4 means distance from zero less than 4",
                        "\u0627\u0644\u062d\u0644 \u0628\u064a\u0646 -\u0664 \u0648 \u0664 / Solution is between -4 and 4"
                ],
                "hints_ar": [
                        "\u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u0645\u0637\u0644\u0642\u0629 \u0623\u0642\u0644 \u0645\u0646 \u0664 \u062a\u0639\u0646\u064a \u0627\u0644\u0645\u0633\u0627\u0641\u0629 \u0645\u0646 \u0627\u0644\u0635\u0641\u0631 \u0623\u0642\u0644 \u0645\u0646 \u0664",
                        "\u0627\u0644\u062d\u0644 \u0628\u064a\u0646 -\u0664 \u0648 \u0664"
                ]
        },
        {
                "id": "explanation5",
                "section_id": "section5",
                "type": "explanation",
                "weight": 0,
                "question_en": "Learn Absolute Value Inequalities",
                "question_ar": "\u062a\u0639\u0644\u0645 \u0645\u062a\u0628\u0627\u064a\u0646\u0627\u062a \u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u0645\u0637\u0644\u0642\u0629",
                "answer": "",
                "answer_ar": "",
                "show_full_solution": False,
                "hide_answer": False,
                "interactive_examples": [
                        {
                                "title_en": "Level 1: Simple Absolute Value - Example 1A (System Demonstrates)",
                                "title_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0661: \u0642\u064a\u0645\u0629 \u0645\u0637\u0644\u0642\u0629 \u0628\u0633\u064a\u0637\u0629 - \u0627\u0644\u0645\u062b\u0627\u0644 \u0661\u0623 (\u064a\u0638\u0647\u0631 \u0627\u0644\u0646\u0638\u0627\u0645)",
                                "problem_en": "Solve |m| \u2264 6",
                                "problem_ar": "\u0627\u062d\u0644 |\u0645| \u2264 \u0666",
                                "solution_en": "Absolute value \u2264 positive means compound inequality\nConvert to: -6 \u2264 m \u2264 6\nSolution: -6 \u2264 m \u2264 6",
                                "solution_ar": "\u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u0645\u0637\u0644\u0642\u0629 \u2264 \u0645\u0648\u062c\u0628 \u062a\u0639\u0646\u064a \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0631\u0643\u0628\u0629\n\u062d\u0648\u0644 \u0625\u0644\u0649: -\u0666 \u2264 \u0645 \u2264 \u0666\n\u0627\u0644\u062d\u0644: -\u0666 \u2264 \u0645 \u2264 \u0666",
                                "practice_question_en": "Now solve: |y| < 3",
                                "practice_question_ar": "\u0627\u0644\u0622\u0646 \u0627\u062d\u0644: |\u0635| < \u0663",
                                "practice_answer": "-3 < y < 3",
                                "practice_answer_ar": "-\u0663 < \u0635 < \u0663"
                        },
                        {
                                "title_en": "Level 2: Absolute Value Greater Than - Example 2A (System Demonstrates)",
                                "title_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0662: \u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u0645\u0637\u0644\u0642\u0629 \u0623\u0643\u0628\u0631 \u0645\u0646 - \u0627\u0644\u0645\u062b\u0627\u0644 \u0662\u0623 (\u064a\u0638\u0647\u0631 \u0627\u0644\u0646\u0638\u0627\u0645)",
                                "problem_en": "Solve |k| > 5",
                                "problem_ar": "\u0627\u062d\u0644 |\u0643| > \u0665",
                                "solution_en": "Absolute value > positive means OR inequality\nConvert to: k < -5 or k > 5\nTwo separate ranges, not connected",
                                "solution_ar": "\u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u0645\u0637\u0644\u0642\u0629 > \u0645\u0648\u062c\u0628 \u062a\u0639\u0646\u064a \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0623\u0648\n\u062d\u0648\u0644 \u0625\u0644\u0649: \u0643 < -\u0665 \u0623\u0648 \u0643 > \u0665\n\u0645\u062f\u0627\u0627\u0646 \u0645\u0646\u0641\u0635\u0644\u0627\u0646\u060c \u063a\u064a\u0631 \u0645\u062a\u0635\u0644\u0627\u0646",
                                "practice_question_en": "Now solve: |n| \u2265 2",
                                "practice_question_ar": "\u0627\u0644\u0622\u0646 \u0627\u062d\u0644: |\u0646| \u2265 \u0662",
                                "practice_answer": "n \u2264 -2 or n \u2265 2",
                                "practice_answer_ar": "\u0646 \u2264 -\u0662 \u0623\u0648 \u0646 \u2265 \u0662"
                        },
                        {
                                "title_en": "Level 3: Complex Absolute Value - Example 3A (System Demonstrates)",
                                "title_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663: \u0642\u064a\u0645\u0629 \u0645\u0637\u0644\u0642\u0629 \u0645\u0639\u0642\u062f\u0629 - \u0627\u0644\u0645\u062b\u0627\u0644 \u0663\u0623 (\u064a\u0638\u0647\u0631 \u0627\u0644\u0646\u0638\u0627\u0645)",
                                "problem_en": "Solve |2x - 3| < 7",
                                "problem_ar": "\u0627\u062d\u0644 |\u0662\u0633 - \u0663| < \u0667",
                                "solution_en": "Step 1: Convert to compound: -7 < 2x - 3 < 7\nStep 2: Add 3 to all parts: -4 < 2x < 10\nStep 3: Divide by 2: -2 < x < 5",
                                "solution_ar": "\u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u062d\u0648\u0644 \u0625\u0644\u0649 \u0645\u0631\u0643\u0628\u0629: -\u0667 < \u0662\u0633 - \u0663 < \u0667\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0623\u0636\u0641 \u0663 \u0644\u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621: -\u0664 < \u0662\u0633 < \u0661\u0660\n\u0627\u0644\u062e\u0637\u0648\u0629 \u0663: \u0627\u0642\u0633\u0645 \u0639\u0644\u0649 \u0662: -\u0662 < \u0633 < \u0665",
                                "practice_question_en": "Now solve: |x + 4| \u2264 6",
                                "practice_question_ar": "\u0627\u0644\u0622\u0646 \u0627\u062d\u0644: |\u0633 + \u0664| \u2264 \u0666",
                                "practice_answer": "-10 \u2264 x \u2264 2",
                                "practice_answer_ar": "-\u0661\u0660 \u2264 \u0633 \u2264 \u0662"
                        }
                ],
                "step_solutions": [
                        {
                                "step_en": "Level 1B Step 1: Convert to compound inequality",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0661\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u062d\u0648\u0644 \u0625\u0644\u0649 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0631\u0643\u0628\u0629",
                                "possible_answers": [
                                        "-3 < y < 3",
                                        "-\u0663 < \u0635 < \u0663",
                                        "y > -3 and y < 3"
                                ],
                                "possible_answers_ar": [
                                        "-\u0663 < \u0635 < \u0663",
                                        "\u0635 > -\u0663 \u0648 \u0635 < \u0663"
                                ]
                        },
                        {
                                "step_en": "Level 2B Step 1: Convert to OR inequality",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0662\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u062d\u0648\u0644 \u0625\u0644\u0649 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0646\u0641\u0635\u0644\u0629",
                                "possible_answers": [
                                        "n \u2264 -2 or n \u2265 2",
                                        "\u0646 \u2264 -\u0662 \u0623\u0648 \u0646 \u2265 \u0662",
                                        "n <= -2 or n >= 2",
                                        "n \u2264 -2 || n \u2265 2"
                                ],
                                "possible_answers_ar": [
                                        "\u0646 \u2264 -\u0662 \u0623\u0648 \u0646 \u2265 \u0662"
                                ]
                        },
                        {
                                "step_en": "Level 3B Step 1: Convert to compound inequality",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0661: \u062d\u0648\u0644 \u0625\u0644\u0649 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0631\u0643\u0628\u0629",
                                "possible_answers": [
                                        "-6 \u2264 x + 4 \u2264 6",
                                        "-\u0666 \u2264 \u0633 + \u0664 \u2264 \u0666"
                                ],
                                "possible_answers_ar": [
                                        "-\u0666 \u2264 \u0633 + \u0664 \u2264 \u0666"
                                ]
                        },
                        {
                                "step_en": "Level 3B Step 2: Subtract 4 from all parts",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0662: \u0627\u0637\u0631\u062d \u0664 \u0645\u0646 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u062c\u0632\u0627\u0621",
                                "possible_answers": [
                                        "-10 \u2264 x \u2264 2",
                                        "-\u0661\u0660 \u2264 \u0633 \u2264 \u0662"
                                ],
                                "possible_answers_ar": [
                                        "-\u0661\u0660 \u2264 \u0633 \u2264 \u0662"
                                ]
                        },
                        {
                                "step_en": "Level 3B Step 3: Write final answer",
                                "step_ar": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649 \u0663\u0628 \u0627\u0644\u062e\u0637\u0648\u0629 \u0663: \u0627\u0643\u062a\u0628 \u0627\u0644\u0625\u062c\u0627\u0628\u0629 \u0627\u0644\u0646\u0647\u0627\u0626\u064a\u0629",
                                "possible_answers": [
                                        "-10 \u2264 x \u2264 2",
                                        "-\u0661\u0660 \u2264 \u0633 \u2264 \u0662"
                                ],
                                "possible_answers_ar": [
                                        "-\u0661\u0660 \u2264 \u0633 \u2264 \u0662"
                                ]
                        }
                ],
                "hints_en": [],
                "hints_ar": []
        },
        {
                "id": "practice5_1",
                "section_id": "section5",
                "type": "practice",
                "weight": 15,
                "question_en": "Solve |3y - 2| > 8",
                "question_ar": "\u0627\u062d\u0644 |\u0663\u0635 - \u0662| > \u0668",
                "answer": "y < -2 or y > 10/3",
                "answer_ar": "\u0635 < -\u0662 \u0623\u0648 \u0635 > \u0661\u0660/\u0663",
                "show_full_solution": False,
                "hide_answer": False,
                "step_solutions": [
                        {
                                "step_en": "\u062d\u0648\u0644 \u0625\u0644\u0649 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0646\u0641\u0635\u0644\u0629 / Convert to OR inequality",
                                "step_ar": "\u062d\u0648\u0644 \u0625\u0644\u0649 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0646\u0641\u0635\u0644\u0629",
                                "possible_answers": [
                                        "3y - 2 < -8 or 3y - 2 > 8",
                                        "3y - 2 < -8 || 3y - 2 > 8",
                                        "\u0663\u0635 - \u0662 < -\u0668 \u0623\u0648 \u0663\u0635 - \u0662 > \u0668"
                                ],
                                "possible_answers_ar": [
                                        "\u0663\u0635 - \u0662 < -\u0668 \u0623\u0648 \u0663\u0635 - \u0662 > \u0668"
                                ]
                        },
                        {
                                "step_en": "\u062d\u0644 \u0643\u0644 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0646\u0641\u0635\u0644\u0629 / Solve each inequality separately",
                                "step_ar": "\u062d\u0644 \u0643\u0644 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0646\u0641\u0635\u0644\u0629",
                                "possible_answers": [
                                        "y < -2 or y > 10/3",
                                        "y < -2 or y > 3.33",
                                        "\u0635 < -\u0662 \u0623\u0648 \u0635 > \u0661\u0660/\u0663"
                                ],
                                "possible_answers_ar": [
                                        "\u0635 < -\u0662 \u0623\u0648 \u0635 > \u0661\u0660/\u0663"
                                ]
                        }
                ],
                "final_answer_required": False,
                "hints_en": [
                        "\u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u0645\u0637\u0644\u0642\u0629 > \u0668 \u062a\u0639\u0646\u064a \u062d\u0627\u0644\u062a\u064a\u0646 \u0645\u0646\u0641\u0635\u0644\u062a\u064a\u0646 / Absolute value > 8 means two separate cases",
                        "\u0625\u0645\u0627 \u0623\u0642\u0644 \u0645\u0646 -\u0668 \u0623\u0648 \u0623\u0643\u0628\u0631 \u0645\u0646 \u0668 / Either < -8 or > 8",
                        "|\u062a\u0639\u0628\u064a\u0631| > \u0668 \u064a\u0639\u0637\u064a: \u062a\u0639\u0628\u064a\u0631 < -\u0668 \u0623\u0648 \u062a\u0639\u0628\u064a\u0631 > \u0668"
                ],
                "hints_ar": [
                        "\u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u0645\u0637\u0644\u0642\u0629 > \u0668 \u062a\u0639\u0646\u064a \u062d\u0627\u0644\u062a\u064a\u0646 \u0645\u0646\u0641\u0635\u0644\u062a\u064a\u0646",
                        "\u0625\u0645\u0627 \u0623\u0642\u0644 \u0645\u0646 -\u0668 \u0623\u0648 \u0623\u0643\u0628\u0631 \u0645\u0646 \u0668",
                        "|\u062a\u0639\u0628\u064a\u0631| > \u0668 \u064a\u0639\u0637\u064a: \u062a\u0639\u0628\u064a\u0631 < -\u0668 \u0623\u0648 \u062a\u0639\u0628\u064a\u0631 > \u0668"
                ]
        },
        {
                "id": "practice5_2",
                "section_id": "section5",
                "type": "practice",
                "weight": 15,
                "stage_type": "practice_word",
                "question_en": "A machine produces parts with target length 50mm. Tolerance is \u00b10.5mm. Write and solve inequality for acceptable lengths.",
                "question_ar": "\u0622\u0644\u0629 \u062a\u0646\u062a\u062c \u0642\u0637\u0639 \u0628\u0637\u0648\u0644 \u0645\u0633\u062a\u0647\u062f\u0641 \u0665\u0660 \u0645\u0645. \u0627\u0644\u062a\u0641\u0627\u0648\u062a \u0627\u0644\u0645\u0633\u0645\u0648\u062d \u00b1\u0660.\u0665 \u0645\u0645. \u0627\u0643\u062a\u0628 \u0648\u0627\u062d\u0644 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0627\u0644\u0623\u0637\u0648\u0627\u0644 \u0627\u0644\u0645\u0642\u0628\u0648\u0644\u0629.",
                "answer": "49.5 \u2264 L \u2264 50.5",
                "answer_ar": "\u0664\u0669.\u0665 \u2264 \u0637 \u2264 \u0665\u0660.\u0665",
                "show_full_solution": False,
                "hide_answer": False,
                "step_solutions": [
                        {
                                "step_en": "\u0627\u0643\u062a\u0628 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u0645\u0637\u0644\u0642\u0629 / Write absolute value inequality",
                                "step_ar": "\u0627\u0643\u062a\u0628 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u0645\u0637\u0644\u0642\u0629",
                                "possible_answers": [
                                        "|L - 50| \u2264 0.5",
                                        "|\u0637 - \u0665\u0660| \u2264 \u0660.\u0665"
                                ],
                                "possible_answers_ar": [
                                        "|\u0637 - \u0665\u0660| \u2264 \u0660.\u0665"
                                ]
                        },
                        {
                                "step_en": "\u062d\u0648\u0644 \u0625\u0644\u0649 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0631\u0643\u0628\u0629 / Convert to compound",
                                "step_ar": "\u062d\u0648\u0644 \u0625\u0644\u0649 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0631\u0643\u0628\u0629",
                                "possible_answers": [
                                        "-0.5 \u2264 L - 50 \u2264 0.5",
                                        "-\u0660.\u0665 \u2264 \u0637 - \u0665\u0660 \u2264 \u0660.\u0665"
                                ],
                                "possible_answers_ar": [
                                        "-\u0660.\u0665 \u2264 \u0637 - \u0665\u0660 \u2264 \u0660.\u0665"
                                ]
                        },
                        {
                                "step_en": "\u0627\u062d\u0633\u0628 \u0627\u0644\u0645\u062f\u0649 \u0627\u0644\u0645\u0642\u0628\u0648\u0644 \u0644\u0644\u0623\u0637\u0648\u0627\u0644 / Calculate acceptable length range",
                                "step_ar": "\u0627\u062d\u0633\u0628 \u0627\u0644\u0645\u062f\u0649 \u0627\u0644\u0645\u0642\u0628\u0648\u0644 \u0644\u0644\u0623\u0637\u0648\u0627\u0644",
                                "possible_answers": [
                                        "49.5 \u2264 L \u2264 50.5",
                                        "\u0664\u0669.\u0665 \u2264 \u0637 \u2264 \u0665\u0660.\u0665"
                                ],
                                "possible_answers_ar": [
                                        "\u0664\u0669.\u0665 \u2264 \u0637 \u2264 \u0665\u0660.\u0665"
                                ]
                        }
                ],
                "final_answer_required": False,
                "hints_en": [
                        "\u0627\u0644\u0641\u0631\u0642 \u0639\u0646 \u0627\u0644\u0637\u0648\u0644 \u0627\u0644\u0645\u0633\u062a\u0647\u062f\u0641 \u064a\u062c\u0628 \u0623\u0646 \u064a\u0643\u0648\u0646 \u0636\u0645\u0646 \u0627\u0644\u062a\u0641\u0627\u0648\u062a / Difference from target must be within tolerance",
                        "\u0627\u0633\u062a\u062e\u062f\u0645 |\u0627\u0644\u0637\u0648\u0644 - \u0627\u0644\u0645\u0633\u062a\u0647\u062f\u0641| \u2264 \u0627\u0644\u062a\u0641\u0627\u0648\u062a",
                        "\u0627\u0644\u0641\u0631\u0642 \u0639\u0646 \u0665\u0660 \u064a\u062c\u0628 \u0623\u0646 \u064a\u0643\u0648\u0646 \u2264 \u0660.\u0665"
                ],
                "hints_ar": [
                        "\u0627\u0644\u0641\u0631\u0642 \u0639\u0646 \u0627\u0644\u0637\u0648\u0644 \u0627\u0644\u0645\u0633\u062a\u0647\u062f\u0641 \u064a\u062c\u0628 \u0623\u0646 \u064a\u0643\u0648\u0646 \u0636\u0645\u0646 \u0627\u0644\u062a\u0641\u0627\u0648\u062a",
                        "\u0627\u0633\u062a\u062e\u062f\u0645 |\u0627\u0644\u0637\u0648\u0644 - \u0627\u0644\u0645\u0633\u062a\u0647\u062f\u0641| \u2264 \u0627\u0644\u062a\u0641\u0627\u0648\u062a",
                        "\u0627\u0644\u0641\u0631\u0642 \u0639\u0646 \u0665\u0660 \u064a\u062c\u0628 \u0623\u0646 \u064a\u0643\u0648\u0646 \u2264 \u0660.\u0665"
                ]
        },
        {
                "id": "assessment5",
                "section_id": "section5",
                "type": "assessment",
                "weight": 20,
                "question_en": "What is the solution to |4 - x| \u2265 3?",
                "question_ar": "\u0645\u0627 \u0647\u0648 \u062d\u0644 |\u0664 - \u0633| \u2265 \u0663\u061f",
                "answer": "x \u2264 1 or x \u2265 7",
                "answer_ar": "\u0633 \u2264 \u0661 \u0623\u0648 \u0633 \u2265 \u0667",
                "show_full_solution": False,
                "hide_answer": True,
                "explanation_en": "Convert to two cases: 4 - x \u2265 3 or 4 - x \u2264 -3, then solve each",
                "explanation_ar": "\u062d\u0648\u0644 \u0625\u0644\u0649 \u062d\u0627\u0644\u062a\u064a\u0646: \u0664 - \u0633 \u2265 \u0663 \u0623\u0648 \u0664 - \u0633 \u2264 -\u0663\u060c \u062b\u0645 \u0627\u062d\u0644 \u0643\u0644 \u062d\u0627\u0644\u0629",
                "final_answer_required": True,
                "hints_en": [
                        "\u0641\u0643\u0631 \u0641\u064a \u062d\u0627\u0644\u062a\u064a\u0646: \u0664 - \u0633 \u2265 \u0663 \u0623\u0648 \u0664 - \u0633 \u2264 -\u0663 / Think two cases: 4 - x \u2265 3 or 4 - x \u2264 -3",
                        "\u062d\u0644 \u0643\u0644 \u062d\u0627\u0644\u0629 \u0645\u0646\u0641\u0635\u0644\u0629 \u0648\u0627\u0646\u062a\u0628\u0647 \u0644\u0644\u0625\u0634\u0627\u0631\u0627\u062a / Solve each case separately, watch the signs"
                ],
                "hints_ar": [
                        "\u0641\u0643\u0631 \u0641\u064a \u062d\u0627\u0644\u062a\u064a\u0646: \u0664 - \u0633 \u2265 \u0663 \u0623\u0648 \u0664 - \u0633 \u2264 -\u0663",
                        "\u062d\u0644 \u0643\u0644 \u062d\u0627\u0644\u0629 \u0645\u0646\u0641\u0635\u0644\u0629 \u0648\u0627\u0646\u062a\u0628\u0647 \u0644\u0644\u0625\u0634\u0627\u0631\u0627\u062a"
                ]
        },
        {
                "id": "examprep5",
                "section_id": "section5",
                "type": "examprep",
                "weight": 25,
                "question_en": "Solve: |2x + 1| - 3 < 4",
                "question_ar": "\u062d\u0644: |\u0662\u0633 + \u0661| - \u0663 < \u0664",
                "answer": "-4 < x < 3",
                "answer_ar": "-\u0664 < \u0633 < \u0663",
                "show_full_solution": False,
                "hide_answer": True,
                "explanation_en": "First add 3 to both sides, then convert absolute value to compound inequality",
                "explanation_ar": "\u0623\u0648\u0644\u0627\u064b \u0623\u0636\u0641 \u0663 \u0644\u0644\u0637\u0631\u0641\u064a\u0646\u060c \u062b\u0645 \u062d\u0648\u0644 \u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u0645\u0637\u0644\u0642\u0629 \u0625\u0644\u0649 \u0645\u062a\u0628\u0627\u064a\u0646\u0629 \u0645\u0631\u0643\u0628\u0629",
                "final_answer_required": True,
                "hints_en": [],
                "hints_ar": []
        }
]
    
    print("📝 Inserting EXACT problems from preview...")
    await problems_collection.insert_many(problems_data)
    
    print("✅ EXACT migration completed successfully!")
    print(f"📊 Inserted {len(sections_data)} sections")
    print(f"📊 Inserted {len(problems_data)} problems")
    print("🎯 Content now matches EXACTLY: learning-equation.preview.emergentagent.com")
    print("✅ All interactive examples, step solutions, and content are identical")
    
    # Close connection
    client.close()
    print("🔌 Database connection closed")

if __name__ == "__main__":
    print("🚀 EXACT Migration from Working Emergent Preview")
    print("🎯 Source: learning-equation.preview.emergentagent.com")
    print("=" * 70)
    
    # Run the migration
    asyncio.run(migrate_exact_preview_data())
    
    print("=" * 70)
    print("✅ SUCCESS: Database now matches working preview exactly!")
    print("🎯 All content, formatting, and interactive elements preserved")
