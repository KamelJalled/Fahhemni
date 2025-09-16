// Mock data for math tutoring app
export const mockProblems = {
  section1: {
    title: {
      en: "Section 1: Solving Inequalities by Addition or Subtraction",
      ar: "القسم الأول: حل المتباينات بالجمع أو بالطرح"
    },
    problems: [
      {
        id: "prep1",
        type: "preparation",
        weight: 10,
        question: {
          en: "x + 5 = 12",
          ar: "س + ٥ = ١٢"
        },
        explanation: {
          en: "This is a review problem. Subtract 5 from both sides: x = 12 - 5 = 7",
          ar: "هذه مسألة مراجعة. اطرح ٥ من الطرفين: س = ١٢ - ٥ = ٧"
        },
        answer: "7",
        answerAr: "٧",
        showFullSolution: true
      },
      {
        id: "explanation1",
        type: "explanation",
        weight: 0,
        question: {
          en: "x + 7 > 10",
          ar: "س + ٧ > ١٠"
        },
        explanation: {
          en: "Step 1: Subtract 7 from both sides\nStep 2: x > 10 - 7\nStep 3: x > 3\nSolution: x > 3",
          ar: "الخطوة ١: اطرح ٧ من الطرفين\nالخطوة ٢: س > ١٠ - ٧\nالخطوة ٣: س > ٣\nالحل: س > ٣"
        },
        answer: "x > 3",
        answerAr: "س > ٣",
        showFullSolution: true
      },
      {
        id: "practice1",
        type: "practice",
        weight: 15,
        question: {
          en: "x - 3 ≤ 8",
          ar: "س - ٣ ≤ ٨"
        },
        answer: "x ≤ 11",
        answerAr: "س ≤ ١١",
        hints: [
          {
            en: "What operation will isolate x on the left side?",
            ar: "ما العملية التي ستعزل س في الطرف الأيسر؟"
          },
          {
            en: "Add 3 to both sides of the inequality.",
            ar: "أضف ٣ إلى طرفي المتباينة."
          },
          {
            en: "x - 3 + 3 ≤ 8 + 3, so x ≤ ?",
            ar: "س - ٣ + ٣ ≤ ٨ + ٣، إذن س ≤ ؟"
          }
        ]
      },
      {
        id: "practice2",
        type: "practice",
        weight: 15,
        question: {
          en: "4x < 20",
          ar: "٤س < ٢٠"
        },
        answer: "x < 5",
        answerAr: "س < ٥",
        hints: [
          {
            en: "What operation will isolate x?",
            ar: "ما العملية التي ستعزل س؟"
          },
          {
            en: "Divide both sides by 4.",
            ar: "اقسم الطرفين على ٤."
          },
          {
            en: "4x ÷ 4 < 20 ÷ 4, so x < ?",
            ar: "٤س ÷ ٤ < ٢٠ ÷ ٤، إذن س < ؟"
          }
        ]
      },
      {
        id: "assessment1",
        type: "assessment",
        weight: 30,
        question: {
          en: "6x ≥ 18",
          ar: "٦س ≥ ١٨"
        },
        answer: "x ≥ 3",
        answerAr: "س ≥ ٣",
        hints: [
          {
            en: "Think about what operation will help you solve for x.",
            ar: "فكر في العملية التي ستساعدك في حل س."
          },
          {
            en: "You need to isolate x by using division.",
            ar: "تحتاج إلى عزل س باستخدام القسمة."
          },
          {
            en: "That's all the hints available.",
            ar: "هذه كل الإرشادات المتاحة."
          }
        ],
        hideAnswer: true
      },
      {
        id: "examprep1",
        type: "examprep",
        weight: 30,
        question: {
          en: "-2x > 8",
          ar: "-٢س > ٨"
        },
        answer: "x < -4",
        answerAr: "س < -٤",
        hints: [
          {
            en: "What happens to the inequality when you divide by a negative number?",
            ar: "ماذا يحدث للمتباينة عندما تقسم على عدد سالب؟"
          },
          {
            en: "The inequality sign flips when dividing by negative numbers.",
            ar: "تنقلب إشارة المتباينة عند القسمة على الأعداد السالبة."
          },
          {
            en: "That's all the hints available.",
            ar: "هذه كل الإرشادات المتاحة."
          }
        ],
        hideAnswer: true
      }
    ]
  }
};

export const mockUsers = [
  {
    username: "ahmed123",
    progress: {
      section1: {
        prep1: { completed: true, score: 100, attempts: 1 },
        explanation1: { completed: true, score: 100, attempts: 1 },
        practice1: { completed: true, score: 85, attempts: 2 },
        practice2: { completed: false, score: 0, attempts: 0 },
        assessment1: { completed: false, score: 0, attempts: 0 },
        examprep1: { completed: false, score: 0, attempts: 0 }
      }
    },
    totalPoints: 285,
    badges: ["First Steps", "Practice Master"]
  }
];

export const badges = [
  { id: "first_steps", name: { en: "First Steps", ar: "الخطوات الأولى" }, description: { en: "Complete your first problem", ar: "أكمل مسألتك الأولى" }, icon: "trophy" },
  { id: "practice_master", name: { en: "Practice Master", ar: "أستاذ التمرين" }, description: { en: "Complete all practice problems", ar: "أكمل جميع مسائل التدريب" }, icon: "star" },
  { id: "assessment_ace", name: { en: "Assessment Ace", ar: "بطل التقييم" }, description: { en: "Score 80+ on assessment", ar: "احصل على ٨٠+ في التقييم" }, icon: "medal" },
  { id: "inequality_expert", name: { en: "Inequality Expert", ar: "خبير المتباينات" }, description: { en: "Complete entire section", ar: "أكمل القسم بالكامل" }, icon: "crown" }
];

// Helper functions for number conversion
export const convertToArabicNumerals = (str) => {
  const arabicNumerals = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
  return str.replace(/[0-9]/g, (digit) => arabicNumerals[parseInt(digit)]);
};

export const convertToWesternNumerals = (str) => {
  const arabicToWestern = {'٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'};
  return str.replace(/[٠-٩]/g, (digit) => arabicToWestern[digit]);
};

export const normalizeAnswer = (answer) => {
  // Convert Arabic numerals to Western and س to x
  return convertToWesternNumerals(answer.toLowerCase().replace(/س/g, 'x').trim());
};