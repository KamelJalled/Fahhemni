# Section 2 problems data - Updated with new curriculum content (Multiplication/Division)
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
        "explanation_en": "This is a review problem for solving inequalities with multiplication/division.",
        "explanation_ar": "هذه مسألة مراجعة لحل المتباينات مع الضرب/القسمة.",
        "show_full_solution": True,
        "hide_answer": False,
        "step_solutions": [
            {
                "step_en": "Divide both sides by 4",
                "step_ar": "اقسم الطرفين على ٤", 
                "possible_answers": [
                    "4x / 4 < 20 / 4",
                    "x < 20 / 4",
                    "x < 5"
                ],
                "possible_answers_ar": [
                    "٤س / ٤ < ٢٠ / ٤",
                    "س < ٢٠ / ٤", 
                    "س < ٥"
                ]
            }
        ],
        "final_answer_required": True,
        "hints_en": [
            "What operation cancels out multiplication?",
            "Divide both sides by 4."
        ],
        "hints_ar": [
            "ما العملية التي تلغي الضرب؟",
            "اقسم الطرفين على ٤."
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
        "show_full_solution": True,
        "hide_answer": False,
        "explanation_en": "Learn to solve inequalities involving multiplication and division",
        "explanation_ar": "تعلم حل المتباينات التي تتضمن الضرب والقسمة",
        "interactive_examples": [
            {
                "title_en": "Level 1: Simple (Positive Coefficient - Example 1A - System Solved)",
                "title_ar": "المستوى ١: بسيط (المعامل الموجب - المثال ١أ - حل النظام)",
                "problem_en": "5x ≥ 30",
                "problem_ar": "٥س ≥ ٣٠",
                "solution_en": "Solution: x ≥ 30 / 5 → x ≥ 6",
                "solution_ar": "الحل: س ≥ ٣٠ / ٥ → س ≥ ٦",
                "practice_question_en": "Now solve: 4y < 24",
                "practice_question_ar": "الآن حل: ٤ص < ٢٤",
                "practice_answer": "y < 6",
                "practice_answer_ar": "ص < ٦"
            },
            {
                "title_en": "Level 2: Medium (Negative Coefficient - Example 2A - System Solved)",
                "title_ar": "المستوى ٢: متوسط (المعامل السالب - المثال ٢أ - حل النظام)",
                "problem_en": "-3m > 15",
                "problem_ar": "-٣م > ١٥",
                "solution_en": "Solution: m < 15 / (-3) → m < -5 (Sign flipped)",
                "solution_ar": "الحل: م < ١٥ / (-٣) → م < -٥ (انقلبت الإشارة)",
                "practice_question_en": "Now solve: -6k ≤ 30",
                "practice_question_ar": "الآن حل: -٦ك ≤ ٣٠",
                "practice_answer": "k ≥ -5",
                "practice_answer_ar": "ك ≥ -٥"
            },
            {
                "title_en": "Level 3: Advanced (Division by Negative - Example 3A - System Solved)",
                "title_ar": "المستوى ٣: متقدم (القسمة السالبة - المثال ٣أ - حل النظام)",
                "problem_en": "k / (-4) ≤ 2",
                "problem_ar": "ك / (-٤) ≤ ٢",
                "solution_en": "Solution: k ≥ 2 * (-4) → k ≥ -8 (Sign flipped)",
                "solution_ar": "الحل: ك ≥ ٢ * (-٤) → ك ≥ -٨ (انقلبت الإشارة)",
                "practice_question_en": "Now solve: n / (-3) > 5",
                "practice_question_ar": "الآن حل: ن / (-٣) > ٥",
                "practice_answer": "n < -15",
                "practice_answer_ar": "ن < -١٥"
            }
        ],
        "step_solutions": [
            {
                "step_en": "Level 1B Step 1: Divide both sides by 4",
                "step_ar": "المستوى ١ب الخطوة ١: اقسم كلا الطرفين على ٤",
                "possible_answers": [
                    "4y / 4 < 24 / 4",
                    "y < 6"
                ],
                "possible_answers_ar": [
                    "٤ص / ٤ < ٢٤ / ٤",
                    "ص < ٦"
                ]
            },
            {
                "step_en": "Level 1B Step 2: Check if sign changes (No, positive division)",
                "step_ar": "المستوى ١ب الخطوة ٢: تحقق من تغيير الإشارة (لا، قسمة موجبة)",
                "possible_answers": [
                    "y < 6"
                ],
                "possible_answers_ar": [
                    "ص < ٦"
                ]
            },
            {
                "step_en": "Level 2B Step 1: Divide both sides by -6",
                "step_ar": "المستوى ٢ب الخطوة ١: اقسم كلا الطرفين على -٦",
                "possible_answers": [
                    "-6k / (-6) ≤ 30 / (-6)"
                ],
                "possible_answers_ar": [
                    "-٦ك / (-٦) ≤ ٣٠ / (-٦)"
                ]
            },
            {
                "step_en": "Level 2B Step 2: Flip the inequality sign",
                "step_ar": "المستوى ٢ب الخطوة ٢: اقلب إشارة المتباينة",
                "possible_answers": [
                    "k ≥ -5"
                ],
                "possible_answers_ar": [
                    "ك ≥ -٥"
                ]
            },
            {
                "step_en": "Level 2B Step 3: Simplify",
                "step_ar": "المستوى ٢ب الخطوة ٣: بسّط",
                "possible_answers": [
                    "k ≥ -5"
                ],
                "possible_answers_ar": [
                    "ك ≥ -٥"
                ]
            },
            {
                "step_en": "Level 3B Step 1: Multiply both sides by -3",
                "step_ar": "المستوى ٣ب الخطوة ١: اضرب كلا الطرفين في -٣",
                "possible_answers": [
                    "n / (-3) * (-3) > 5 * (-3)"
                ],
                "possible_answers_ar": [
                    "ن / (-٣) * (-٣) > ٥ * (-٣)"
                ]
            },
            {
                "step_en": "Level 3B Step 2: Flip the inequality sign",
                "step_ar": "المستوى ٣ب الخطوة ٢: اقلب إشارة المتباينة",
                "possible_answers": [
                    "n < -15"
                ],
                "possible_answers_ar": [
                    "ن < -١٥"
                ]
            },
            {
                "step_en": "Level 3B Step 3: Calculate the result",
                "step_ar": "المستوى ٣ب الخطوة ٣: احسب الناتج",
                "possible_answers": [
                    "n < -15"
                ],
                "possible_answers_ar": [
                    "ن < -١٥"
                ]
            }
        ],
        "hints_en": [
            "To isolate 'y', what number should you divide by?",
            "Does the inequality sign change when dividing by a positive number?",
            "What operation is needed to isolate 'k'?",
            "Remember the rule! What happens to the inequality sign when you divide by a negative number?",
            "Simplify the calculation.",
            "To undo division, use multiplication.",
            "You multiplied by a negative number. What does that mean for the sign?",
            "What is the result of 5 * (-3)?"
        ],
        "hints_ar": [
            "لعزل 'ص'، على أي رقم يجب أن تقسم؟",
            "هل تتغير إشارة المتباينة عند القسمة على عدد موجب؟",
            "ما هي العملية اللازمة لعزل 'ك'؟",
            "تذكر القاعدة! ماذا يحدث لإشارة المتباينة عند القسمة على عدد سالب؟",
            "قم بتبسيط العملية الحسابية.",
            "للتخلص من القسمة، استخدم الضرب.",
            "لقد ضربت في عدد سالب. ماذا يعني ذلك للإشارة؟",
            "ما هو ناتج ٥ × (-٣)؟"
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
                "step_en": "Multiply both sides by -3/2", 
                "step_ar": "اضرب الطرفين في -٣/٢", 
                "possible_answers": [
                    "(-2/3 k) * (-3/2) > 8 * (-3/2)",
                    "k > 8 * (-3/2)"
                ],
                "possible_answers_ar": [
                    "(-٢/٣ ك) * (-٣/٢) > ٨ * (-٣/٢)",
                    "ك > ٨ * (-٣/٢)"
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
                "step_en": "Simplify calculation", 
                "step_ar": "بسّط الحساب",
                "possible_answers": [
                    "k < -12"
                ],
                "possible_answers_ar": [
                    "ك < -١٢"
                ]
            }
        ],
        "hints_en": [
            "Multiply by the reciprocal of the coefficient to isolate 'k'.",
            "Don't forget the rule when multiplying by a negative number.",
            "Simplify 8 * (-3/2)."
        ],
        "hints_ar": [
            "اضرب في مقلوب المعامل لعزل 'ك'.",
            "لا تنس القاعدة عند الضرب في عدد سالب.",
            "قم بتبسيط ٨ * (-٣/٢)."
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
                "step_en": "Set up the inequality: 10t ≥ 500", 
                "step_ar": "اكتب المتباينة: ١٠ت ≥ ٥٠٠",
                "possible_answers": [
                    "10t ≥ 500"
                ],
                "possible_answers_ar": [
                    "١٠ت ≥ ٥٠٠"
                ]
            },
            {
                "step_en": "Divide both sides by 10", 
                "step_ar": "اقسم الطرفين على ١٠",
                "possible_answers": [
                    "t ≥ 500 / 10",
                    "t ≥ 50"
                ],
                "possible_answers_ar": [
                    "ت ≥ ٥٠٠ / ١٠",
                    "ت ≥ ٥٠"
                ]
            }
        ],
        "hints_en": [
            "The total amount is the price per ticket times the number of tickets.",
            "Use division to isolate 't'."
        ],
        "hints_ar": [
            "المبلغ الإجمالي هو سعر التذكرة مضروبًا في عددها.",
            "استخدم القسمة لعزل 'ت'."
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
            "This involves division by a negative number.",
            "Multiply both sides by -2 and flip the inequality sign.",
            "That's all the hints available."
        ],
        "hints_ar": [
            "هذا يتضمن القسمة على عدد سالب.",
            "اضرب الطرفين في -٢ واقلب إشارة المتباينة.",
            "هذه كل الإرشادات المتاحة."
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
        "hints_en": [
            "The inequality is 15p ≥ 60",
            "Divide both sides by 15 to solve for p.",
            "That's all the hints available."
        ],
        "hints_ar": [
            "المتباينة هي ١٥ح ≥ ٦٠",
            "اقسم الطرفين على ١٥ لحل ح.",
            "هذه كل الإرشادات المتاحة."
        ]
    }
]