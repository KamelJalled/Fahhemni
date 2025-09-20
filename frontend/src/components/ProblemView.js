import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth, useLanguage } from '../App';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Globe, ArrowLeft, Lightbulb, CheckCircle, XCircle, RotateCcw, Trophy, Keyboard, Mic, BookOpen, Target, HelpCircle } from 'lucide-react';
import { useToast } from '../hooks/use-toast';
import VoiceInput from './VoiceInput';
import MathKeyboard from './MathKeyboard';
import RulesModal from './RulesModal';

const ProblemView = () => {
  const { problemId } = useParams();
  const { user } = useAuth();
  const { language, toggleLanguage } = useLanguage();
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const [stepAnswers, setStepAnswers] = useState(['', '', '']); // For 3-step solving
  const [currentStep, setCurrentStep] = useState(0);
  const [currentHint, setCurrentHint] = useState(0);
  const [showHints, setShowHints] = useState([false, false, false]); // Per-step hint visibility
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [stepResults, setStepResults] = useState([false, false, false]); // Track each step result
  const [attempts, setAttempts] = useState(0);
  const [showEncouragement, setShowEncouragement] = useState(false);
  const [userProgress, setUserProgress] = useState(null);
  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showVoiceInput, setShowVoiceInput] = useState(false);
  const [showMathKeyboard, setShowMathKeyboard] = useState(false);
  const [activeInputIndex, setActiveInputIndex] = useState(0);
  const [allStepsComplete, setAllStepsComplete] = useState(false);
  const [userAnswer, setUserAnswer] = useState('');
  const [showCompletionScreen, setShowCompletionScreen] = useState(false);
  const [completionType, setCompletionType] = useState('section'); // 'section' or 'final'
  const [isChecking, setIsChecking] = useState(false);
  const [checkingStepIndex, setCheckingStepIndex] = useState(-1);
  
  // For interactive explanation/preparation
  const [currentExample, setCurrentExample] = useState(0);
  const [showExample, setShowExample] = useState(false);
  const [practiceAnswer, setPracticeAnswer] = useState('');
  const [practiceComplete, setPracticeComplete] = useState([]);
  const [hintsUsed, setHintsUsed] = useState(0);
  const [showRedirectionButton, setShowRedirectionButton] = useState(false);
  const [currentScore, setCurrentScore] = useState(100); // Start with 100%
  const [explanationStep, setExplanationStep] = useState(0); // For explanation stage step tracking
  const [explanationAnswers, setExplanationAnswers] = useState(['', '', '']); // Single input per example (simplified management)
  const [explanationStepHistory, setExplanationStepHistory] = useState([]); // Store completed step answers for display
  const [showRulesModal, setShowRulesModal] = useState(false); // Rules modal state
  const [navigationInProgress, setNavigationInProgress] = useState(false); // Prevent navigation loops

  // GLOBAL: Enhanced normalization for negative numbers and mathematical expressions
  const normalizeAnswer = (answer) => {
    if (!answer) return '';
    
    // Process alternative absolute value input methods first
    let processed = processAbsoluteValueAlternatives(answer);
    
    // Use basic normalization
    let normalized = basicNormalizeAnswer(processed);
    
    // GLOBAL NEGATIVE NUMBER VALIDATION ENHANCEMENT
    // Handle negative numbers with or without parentheses: -5 vs (-5)
    normalized = normalizeNegativeNumbers(normalized);
    
    // Enhanced space and operator normalization
    normalized = normalized
      .replace(/\s+/g, '') // Remove all spaces completely
      .replace(/\(\s*(-?\d+\.?\d*)\s*\)/g, '$1') // Convert (number) to number
      .replace(/\(\s*(-?\d+\.?\d*\/?\d*\.?\d*)\s*\)/g, '$1') // Handle fractions in parentheses
      .toLowerCase();
    
    return normalized;
  };

  // ABSOLUTE VALUE: Process alternative input methods
  const processAbsoluteValueAlternatives = (input) => {
    if (!input) return '';
    
    // Convert abs(expression) to |expression|
    let processed = input.replace(/abs\s*\(\s*([^)]+)\s*\)/gi, '|$1|');
    
    // Convert ABS(expression) to |expression|
    processed = processed.replace(/ABS\s*\(\s*([^)]+)\s*\)/gi, '|$1|');
    
    // Convert //expression// to |expression|
    processed = processed.replace(/\/\/\s*([^\/]+)\s*\/\//g, '|$1|');
    
    // Clean up any extra spaces around the converted expressions
    processed = processed.replace(/\|\s*([^|]*)\s*\|/g, '|$1|');
    
    return processed;
  };

  // GLOBAL: Normalize negative numbers with multiple format support
  const normalizeNegativeNumbers = (expression) => {
    if (!expression) return '';
    
    let normalized = expression.trim();
    
    // Handle Arabic numerals to Western conversion
    const arabicToWestern = {'٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'};
    normalized = normalized.replace(/[٠-٩]/g, (digit) => arabicToWestern[digit]);
    
    // Convert Arabic variable names
    normalized = normalized.replace(/س/g, 'x').replace(/ص/g, 'y').replace(/ك/g, 'k').replace(/م/g, 'm').replace(/ن/g, 'n');
    
    // Remove spaces around operators and parentheses
    normalized = normalized.replace(/\s+/g, '');
    
    // Normalize parentheses around negative numbers: (-5) → -5
    normalized = normalized.replace(/\((-?\d+\.?\d*)\)/g, '$1');
    
    // Handle fractions with parentheses: (-3)/(-6) → -3/-6
    normalized = normalized.replace(/\((-?\d+\.?\d*)\)\/\((-?\d+\.?\d*)\)/g, '$1/$2');
    
    // Handle mixed parentheses: -3m/(-3) → -3m/-3
    normalized = normalized.replace(/\((-?\d+\.?\d*)\)/g, '$1');
    
    // Normalize inequality operators
    normalized = normalized.replace(/≥/g, '>=').replace(/≤/g, '<=');
    
    return normalized;
  };

  // GLOBAL: Enhanced validation that accepts multiple formats
  const normalizeAndValidateAnswer = (userInput, expectedAnswers) => {
    if (!userInput || !Array.isArray(expectedAnswers)) return false;
    
    const normalizedInput = normalizeAnswer(userInput);
    
    // Check against all expected answer formats
    return expectedAnswers.some(expected => {
      const normalizedExpected = normalizeAnswer(expected);
      return normalizedInput === normalizedExpected || 
             areBidirectionallyEqual(normalizedInput, normalizedExpected);
    });
  };

  // NEW: Handle bidirectional inequality validation for Sections 3, 4, and 5
  const areBidirectionallyEqual = (userAnswer, expectedAnswer) => {
    // Only apply bidirectional logic for Sections 3, 4, and 5
    const currentSectionNum = problemId ? parseInt(problemId.match(/\d+/)?.[0]) : 0;
    if (currentSectionNum < 3 || currentSectionNum > 5) return false;
    
    // Check if both expressions contain inequality operators
    const inequalityOperators = ['>=', '<=', '>', '<', '≥', '≤'];
    const userHasInequality = inequalityOperators.some(op => userAnswer.includes(op));
    const expectedHasInequality = inequalityOperators.some(op => expectedAnswer.includes(op));
    
    if (!userHasInequality || !expectedHasInequality) return false;
    
    // Parse the inequality expressions
    const userParsed = parseInequalityExpression(userAnswer);
    const expectedParsed = parseInequalityExpression(expectedAnswer);
    
    if (!userParsed || !expectedParsed) return false;
    
    // Check if they're equivalent but reversed
    // e.g., "250 ≥ 100 + 2k" equals "100 + 2k ≤ 250"
    const userReversed = reverseInequality(userParsed);
    return isEquivalentExpression(userReversed, expectedParsed);
  };

  // Helper: Parse inequality expression into components
  const parseInequalityExpression = (expression) => {
    const operators = ['>=', '<=', '>', '<'];
    let operator = null;
    let leftSide = '';
    let rightSide = '';
    
    for (const op of operators) {
      if (expression.includes(op)) {
        const parts = expression.split(op);
        if (parts.length === 2) {
          leftSide = parts[0].trim();
          rightSide = parts[1].trim();
          operator = op;
          break;
        }
      }
    }
    
    if (!operator) return null;
    
    return { leftSide, operator, rightSide };
  };

  // Helper: Reverse the inequality
  const reverseInequality = (parsed) => {
    const operatorMap = {
      '>=': '<=',
      '<=': '>=',
      '>': '<',
      '<': '>'
    };
    
    return {
      leftSide: parsed.rightSide,
      operator: operatorMap[parsed.operator],
      rightSide: parsed.leftSide
    };
  };

  // Helper: Check if two parsed expressions are equivalent
  const isEquivalentExpression = (expr1, expr2) => {
    return expr1.leftSide === expr2.leftSide && 
           expr1.operator === expr2.operator && 
           expr1.rightSide === expr2.rightSide;
  };

  // CRITICAL: Pedagogical hint system - NEVER show direct answers
  const generateGuidanceHint = (problem, attemptNumber) => {
    const isWordProblem = problem.question_en?.length > 50 || 
                         problem.question_ar?.length > 50 ||
                         problem.question_en?.toLowerCase().includes('word') ||
                         problem.question_en?.includes('tickets') ||
                         problem.question_en?.includes('candy') ||
                         problem.question_ar?.includes('ريال');
    
    // Attempt 1: General guidance (process-focused)
    if (attemptNumber === 1) {
      if (isWordProblem) {
        return {
          en: "Start by identifying the variable. What are we trying to find? Look for key phrases that indicate mathematical operations.",
          ar: "ابدأ بتحديد المتغير. ما الذي نحاول إيجاده؟ ابحث عن العبارات المفتاحية التي تشير إلى العمليات الرياضية."
        };
      } else {
        return {
          en: "Remember: we want to isolate the variable on one side. What operation would help you do that?",
          ar: "تذكر: نريد عزل المتغير في جانب واحد. ما العملية التي ستساعدك في ذلك؟"
        };
      }
    }
    
    // Attempt 2: More specific guidance (method-focused)
    if (attemptNumber === 2) {
      if (isWordProblem) {
        return {
          en: "Think about the relationship described. What mathematical symbol represents 'at least', 'more than', or 'less than'?",
          ar: "فكر في العلاقة الموصوفة. ما الرمز الرياضي الذي يمثل 'على الأقل' أو 'أكثر من' أو 'أقل من'؟"
        };
      } else {
        return {
          en: "Look at the coefficient of the variable. Is it positive or negative? This affects what operation you need.",
          ar: "انظر إلى معامل المتغير. هل هو موجب أم سالب؟ هذا يؤثر على العملية التي تحتاجها."
        };
      }
    }
    
    // Attempt 3: Process hint (still no direct answer)
    if (attemptNumber >= 3) {
      if (isWordProblem) {
        return {
          en: "Break it down: identify the variable, write the mathematical relationship, then solve step by step.",
          ar: "قسّم المسألة: حدد المتغير، اكتب العلاقة الرياضية، ثم حل خطوة بخطوة."
        };
      } else {
        return {
          en: "Focus on the process: what operation undoes the current one? Remember the rules for inequalities.",
          ar: "ركز على العملية: ما العملية التي تلغي العملية الحالية؟ تذكر قواعد المتباينات."
        };
      }
    }
    
    // Default fallback
    return {
      en: "Think about the mathematical concept step by step. What is the next logical operation?",
      ar: "فكر في المفهوم الرياضي خطوة بخطوة. ما العملية المنطقية التالية؟"
    };
  };

  // ENHANCED: Error-specific guidance (never shows direct answers)
  const generateErrorSpecificHint = (userAnswer, expectedAnswers, problemType) => {
    // Analyze the error type without revealing the correct answer
    const userNormalized = normalizeAnswer(userAnswer);
    
    // Check for common error patterns
    if (userNormalized.includes('>') && expectedAnswers?.some(ans => normalizeAnswer(ans).includes('<'))) {
      return {
        en: "Check the direction of your inequality sign. When you multiply or divide by a negative number, what happens?",
        ar: "تحقق من اتجاه إشارة المتباينة. عندما تضرب أو تقسم على عدد سالب، ماذا يحدث؟"
      };
    }
    
    if (userNormalized.includes('<') && expectedAnswers?.some(ans => normalizeAnswer(ans).includes('>'))) {
      return {
        en: "Look at your inequality sign again. Did you remember to flip it when needed?",
        ar: "انظر إلى إشارة المتباينة مرة أخرى. هل تذكرت قلبها عند الحاجة؟"
      };
    }
    
    // Check for calculation errors (without showing correct calculation)
    if (userAnswer && !userAnswer.includes('x') && !userAnswer.includes('س')) {
      return {
        en: "Your answer should include the variable. Are you solving for the variable or just calculating numbers?",
        ar: "يجب أن تتضمن إجابتك المتغير. هل تحل للمتغير أم تحسب الأرقام فقط؟"
      };
    }
    
    // Default error guidance
    return {
      en: "Review your calculation step by step. What operation did you perform, and did you apply it correctly?",
      ar: "راجع حسابك خطوة بخطوة. ما العملية التي نفذتها، وهل طبقتها بشكل صحيح؟"
    };
  };

  // CRITICAL: Step validation logic with enforced business rules
  const getRequiredSteps = (problemType, problemId, problemQuestion) => {
    // Business Rule 1: Simple inequalities ALWAYS require 2 steps
    if (problemType === 'explanation' || problemType === 'preparation') {
      return 2; // Step 1: Show operation, Step 2: Simplified answer
    }
    
    // Business Rule 2: Word problems ALWAYS require 3 steps  
    if (problemType === 'practice' && problemQuestion) {
      const questionText = (language === 'en' ? problemQuestion.question_en : problemQuestion.question_ar) || '';
      const isWordProblem = questionText.length > 50 || 
                           questionText.toLowerCase().includes('word') ||
                           questionText.includes('ريال') ||
                           questionText.includes('tickets') ||
                           questionText.includes('candy') ||
                           questionText.includes('children');
      
      if (isWordProblem) {
        return 3; // Step 1: Write inequality, Step 2: Show operation, Step 3: Simplified answer
      } else {
        return 2; // Simple practice problems: Step 1: Show operation, Step 2: Simplified answer  
      }
    }
    
    // Business Rule 3: Assessment and Exam Prep word problems ALSO require 3 steps
    if (problemType === 'assessment' || problemType === 'examprep') {
      // Check if this is a word problem
      const questionText = (language === 'en' ? problemQuestion?.question_en : problemQuestion?.question_ar) || '';
      const isWordProblem = questionText.length > 50 || 
                           questionText.toLowerCase().includes('word') ||
                           questionText.includes('ريال') ||
                           questionText.includes('tickets') ||
                           questionText.includes('candy') ||
                           questionText.includes('children');
      
      if (isWordProblem) {
        return 3; // Step 1: Write inequality, Step 2: Show operation, Step 3: Simplified answer
      } else {
        return 2; // Simple assessment problems: Step 1: Show operation, Step 2: Simplified answer
      }
    }
    
    return 2; // Default: 2 steps for most problems
  };

  const validateStepProgression = (problemType, problemId, currentStep, problem) => {
    const requiredSteps = getRequiredSteps(problemType, problemId, problem);
    
    console.log(`🔍 Step Validation: Problem ${problemId}, Current Step: ${currentStep + 1}, Required Steps: ${requiredSteps}`);
    
    if (currentStep + 1 < requiredSteps) {
      // More steps required
      return {
        valid: true,
        nextStep: currentStep + 1,
        complete: false,
        message: language === 'en' 
          ? `Good! Move to step ${currentStep + 2} of ${requiredSteps}`
          : `جيد! انتقل إلى الخطوة ${currentStep + 2} من ${requiredSteps}`
      };
    } else if (currentStep + 1 === requiredSteps) {
      // This is the final required step
      return {
        valid: true,
        complete: true,
        message: language === 'en' 
          ? `Excellent! You completed all ${requiredSteps} required steps`
          : `ممتاز! لقد أكملت جميع الخطوات المطلوبة ${requiredSteps}`
      };
    } else {
      // Should not happen - too many steps
      return {
        valid: false,
        error: true,
        message: language === 'en' 
          ? `Error: This problem requires exactly ${requiredSteps} steps`
          : `خطأ: هذه المسألة تتطلب بالضبط ${requiredSteps} خطوات`
      };
    }
  };
  const validateInequalityStep = (userAnswer, expectedAnswers, stepInstruction) => {
    const normalizedUserAnswer = normalizeAnswer(userAnswer);
    
    // Enhanced validation with bidirectional support for Sections 3, 4, 5
    let isCorrect = false;
    
    if (expectedAnswers) {
      // Check direct matches first
      isCorrect = expectedAnswers.some(expectedAnswer => 
        normalizeAnswer(expectedAnswer) === normalizedUserAnswer
      );
      
      // If not direct match, check bidirectional equivalence for Sections 3, 4, 5
      if (!isCorrect) {
        isCorrect = expectedAnswers.some(expectedAnswer => 
          areBidirectionallyEqual(normalizedUserAnswer, normalizeAnswer(expectedAnswer))
        );
      }
    }
    
    return isCorrect;
  };

  // FIXED: Redesigned stage structure for proper word problem handling
  const getStageType = (problemType, problemId) => {
    // PREPARATION STAGE: Final answer only with auto-hints
    if (problemType === 'preparation' || problemId?.startsWith('prep')) {
      return 'preparation';
    }
    
    // EXPLANATION STAGE: Teaching + step-by-step practice
    if (problemType === 'explanation') {
      return 'explanation';
    }
    
    // PRACTICE STAGES: Check if it's a word problem that needs special handling
    if (problemType === 'practice' || problemId?.includes('practice')) {
      // CRITICAL FIX: Word problems in practice stages should use 3-step process with hints
      const questionText = (language === 'en' ? problem?.question_en : problem?.question_ar) || '';
      const isWordProblem = questionText.length > 50 || 
                           questionText.toLowerCase().includes('word') ||
                           questionText.includes('ريال') ||
                           questionText.includes('tickets') ||
                           questionText.includes('candy') ||
                           questionText.includes('children');
      
      if (isWordProblem) {
        return 'practice_word'; // NEW: Special type for practice word problems
      } else {
        return 'practice'; // Regular step-by-step guided for non-word problems
      }
    }
    
    // ASSESSMENT & EXAM PREP: Final answer with score penalties
    if (problemType === 'assessment' || problemType === 'examprep' ||
        problemId?.includes('assess') || problemId?.includes('exam')) {
      return 'assessment';
    }
    
    return 'preparation'; // Default
  };

  // GLOBAL: Helper function for basic normalization without recursion
  const basicNormalizeAnswer = (answer) => {
    if (!answer) return '';
    
    // Convert Arabic numerals to Western and Arabic variables to English
    const arabicToWestern = {'٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'};
    let normalized = answer.toLowerCase()
      .replace(/س/g, 'x')
      .replace(/ص/g, 'y')
      .replace(/ك/g, 'k')
      .replace(/م/g, 'm')
      .replace(/ن/g, 'n')
      .replace(/[٠-٩]/g, (digit) => arabicToWestern[digit])
      .trim();
    
    // Normalize operators and spaces more carefully
    normalized = normalized
      .replace(/÷/g, '/') // Convert ÷ to /
      .replace(/×/g, '*') // Convert × to *
      .replace(/\s+/g, ' ') // Normalize multiple spaces to single
      .replace(/\s*([+\-*/=])\s*/g, '$1') // Remove spaces around basic operators
      .replace(/\s*([<>])\s*/g, '$1') // Remove spaces around inequality signs
      .replace(/\s*([≤≥])\s*/g, '$1') // Remove spaces around unicode inequalities
      .replace(/\s*([<>]=?)\s*/g, '$1'); // Handle <= >= combinations
    
    return normalized;
  };

  // CRITICAL: Server-side access control to prevent cheating via direct URL access
  const checkStageAccessSecurity = (problemData, userProgressData) => {
    if (!problemData || !userProgressData) return { access: true };
    
    const problemId = problemData.id;
    const problemType = problemData.type;
    const sectionId = problemData.section_id;
    const sectionProgress = userProgressData[sectionId] || {};
    
    // SECURITY: Lock Assessment and Exam Prep stages until ALL practice stages are completed
    if (problemType === 'assessment' || problemType === 'examprep') {
      const practiceProblems = Object.keys(sectionProgress).filter(id => 
        id.includes('practice')
      );
      
      if (practiceProblems.length > 0) {
        const allPracticeComplete = practiceProblems.every(practiceId => 
          sectionProgress[practiceId]?.completed === true
        );
        
        if (!allPracticeComplete) {
          return {
            access: false,
            message: language === 'en' 
              ? 'Access denied: You must complete all practice stages first'
              : 'تم رفض الوصول: يجب إكمال جميع مراحل التدريب أولاً',
            redirectTo: '/dashboard'
          };
        }
      }
    }
    
    // SECURITY: Lock Exam Prep until Assessment is completed
    if (problemType === 'examprep') {
      const assessmentId = `assessment${sectionId.slice(-1)}`;
      const assessmentComplete = sectionProgress[assessmentId]?.completed === true;
      
      if (!assessmentComplete) {
        return {
          access: false,
          message: language === 'en' 
            ? 'Access denied: You must complete the Assessment stage first'
            : 'تم رفض الوصول: يجب إكمال مرحلة التقييم أولاً',
          redirectTo: '/dashboard'
        };
      }
    }
    
    return { access: true };
  };

  useEffect(() => {
    if (!user || !problemId) {
      navigateToSectionDashboard();
      return;
    }

    fetchData();
  }, [user, problemId, navigate]);

  // Auto-scroll when virtual keyboard opens to keep input field visible
  useEffect(() => {
    if (showMathKeyboard) {
      // Add body class for mobile spacing
      if (window.innerWidth <= 768) {
        document.body.classList.add('keyboard-active');
      }
      
      // Find the currently active input field
      const activeInput = document.activeElement;
      if (activeInput && activeInput.tagName === 'INPUT') {
        // Calculate the keyboard height (approximately 300px for mobile)
        const keyboardHeight = window.innerWidth <= 768 ? 300 : 0;
        const viewportHeight = window.innerHeight;
        const scrollOffset = keyboardHeight + 20; // Extra 20px padding
        
        // Scroll the active input into view above the keyboard
        setTimeout(() => {
          activeInput.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
          });
          
          // Additional scroll adjustment for mobile to account for keyboard
          if (window.innerWidth <= 768) {
            const currentScroll = window.pageYOffset;
            const inputRect = activeInput.getBoundingClientRect();
            const inputBottom = inputRect.bottom + currentScroll;
            const visibleAreaTop = viewportHeight - keyboardHeight - 100; // 100px buffer
            
            if (inputRect.bottom > visibleAreaTop) {
              window.scrollTo({
                top: currentScroll + (inputRect.bottom - visibleAreaTop),
                behavior: 'smooth'
              });
            }
          }
        }, 100); // Small delay to ensure keyboard is rendered
      }
    } else {
      // Remove body class when keyboard is closed
      document.body.classList.remove('keyboard-active');
    }
    
    // Cleanup function
    return () => {
      document.body.classList.remove('keyboard-active');
    };
  }, [showMathKeyboard]);

  // Auto-scroll when voice input opens
  useEffect(() => {
    if (showVoiceInput) {
      const activeInput = document.activeElement;
      if (activeInput && activeInput.tagName === 'INPUT') {
        setTimeout(() => {
          activeInput.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
          });
        }, 100);
      }
    }
  }, [showVoiceInput]);

  const fetchData = async () => {
    try {
      setLoading(true);

      // Fetch problem details with username for access control
      const problemResponse = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/problems/${problemId}?username=${user.username}`
      );
      
      let problemData = null;
      if (problemResponse.ok) {
        problemData = await problemResponse.json();
        setProblem(problemData);
      }

      // Fetch user progress
      const progressResponse = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/students/${user.username}/progress`
      );
      
      if (progressResponse.ok) {
        const progressData = await progressResponse.json();
        setUserProgress(progressData.progress);
        
        // CRITICAL: Check stage access security before allowing problem access
        if (problemData) {
          const securityCheck = checkStageAccessSecurity(problemData, progressData.progress);
          
          if (!securityCheck.access) {
            // SECURITY: Block access and redirect to dashboard with alert
            alert(`🔒 ${securityCheck.message}`);
            if (securityCheck.redirectTo === '/dashboard' || !securityCheck.redirectTo) {
              navigateToSectionDashboard();
            } else {
              navigate(securityCheck.redirectTo);
            }
            return;
          }
        }
        
        // FIXED: Dynamic section-aware progress tracking
        const getSectionNumber = (id) => {
          const match = id.match(/(\d+)$/);
          return match ? parseInt(match[1]) : 1;
        };
        
        const currentSectionNum = getSectionNumber(problemId);
        const sectionKey = `section${currentSectionNum}`;
        const sectionProgress = progressData.progress[sectionKey] || {};
        
        setAttempts(sectionProgress[problemId]?.attempts || 0);
        console.log(`📊 Progress loaded for ${problemId} in ${sectionKey}: ${sectionProgress[problemId]?.attempts || 0} attempts`);
      }

    } catch (error) {
      console.error('Error fetching data:', error);
      navigateToSectionDashboard();
    } finally {
      setLoading(false);
    }
  };

  // Helper function to get absolute value hint for Section 5
  const getAbsoluteValueHint = () => {
    if (problem?.section_id === 'section5') {
      return {
        en: '💡 Use | symbol for absolute value: |x|',
        ar: '💡 استخدم رمز | للقيمة المطلقة: |س|'
      };
    }
    return null;
  };

  const text = {
    en: {
      back: "Back to Dashboard",
      submit: "Submit Answer",
      tryAgain: "Try Again",
      showHint: "Show Hint",
      nextHint: "Next Hint",
      noMoreHints: "No more hints available",
      yourAnswer: "Your Answer",
      placeholder: "Enter your answer (e.g., x > 5)",
      correct: "Correct! Well done!",
      incorrect: "Not quite right. Try again!",
      explanation: "Explanation",
      attempts: "Attempts",
      weight: "Weight",
      encouragement: [
        "Great effort! Keep going!",
        "You're getting closer!",
        "Don't give up, you can do this!",
        "Learning from mistakes makes you stronger!",
        "Every attempt brings you closer to success!"
      ],
      completed: "Problem Completed!",
      points: "Points Earned",
      backToDashboard: "Back to Dashboard",
      nextProblem: "Next Problem →",
      stepByStep: "Solve Step by Step:",
      nextStep: "Next Step →",
      showSolution: "Show Solution",
      completion: {
        sectionTitle: "🎉 Congratulations!",
        sectionMessage: "You've completed this section!",
        finalTitle: "🎉 Demo Completed!",
        finalMessage: "Thank you for testing Fahhemni. Please share your feedback to help us improve the learning experience!",
        returnToDashboard: "Return to Dashboard",
        checking: "Checking...",
        processing: "Processing your answer..."
      },
      tryItYourself: "Try It Yourself:",
      checkAnswer: "Check Answer",
      hint: "Hint",
      continueNext: "Continue to Next Problem →",
      operatorInstructions: "Use +, -, *, / or ×, ÷"
    },
    ar: {
      back: "العودة للوحة التحكم",
      submit: "إرسال الإجابة",
      tryAgain: "حاول مرة أخرى",
      showHint: "إظهار الإرشاد",
      nextHint: "الإرشاد التالي",
      noMoreHints: "لا توجد إرشادات أخرى متاحة",
      yourAnswer: "إجابتك",
      placeholder: "أدخل إجابتك (مثل: س > ٥)",
      correct: "صحيح! أحسنت!",
      incorrect: "ليس صحيحاً تماماً. حاول مرة أخرى!",
      explanation: "الشرح",
      attempts: "المحاولات",
      weight: "الوزن",
      encouragement: [
        "مجهود رائع! استمر!",
        "أنت تقترب من الحل!",
        "لا تستسلم، يمكنك فعل ذلك!",
        "التعلم من الأخطاء يجعلك أقوى!",
        "كل محاولة تقربك من النجاح!"
      ],
      completed: "تم إكمال المسألة!",
      points: "النقاط المكتسبة",
      backToDashboard: "العودة للوحة التحكم",
      nextProblem: "المسألة التالية ←",
      stepByStep: "حل خطوة بخطوة:",
      nextStep: "الخطوة التالية ←",
      showSolution: "إظهار الحل",
      tryItYourself: "جربه بنفسك:",
      checkAnswer: "تحقق من الإجابة",
      hint: "إرشاد",
      continueNext: "تابع للمسألة التالية ←",
      operatorInstructions: "استخدم +, -, *, / أو ×, ÷",
      completion: {
        sectionTitle: "🎉 مبروك!",
        sectionMessage: "لقد أكملت هذا القسم!",
        finalTitle: "🎉 اكتملت التجربة!",
        finalMessage: "شكراً لك لتجربة فهّمني. يرجى مشاركة ملاحظاتك لمساعدتنا في تحسين تجربة التعلم!",
        returnToDashboard: "العودة إلى لوحة التحكم",
        checking: "جاري التحقق...",
        processing: "معالجة إجابتك..."
      }
    }
  };

  const handleCheckStep = async (stepIndex) => {
    const currentAnswer = stepAnswers[stepIndex].trim();
    if (!currentAnswer) return;

    try {
      // Show loading indicator
      setIsChecking(true);
      setCheckingStepIndex(stepIndex);
      
      // Add 1.5 second delay for AI processing feel
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const currentStepSolution = problem.step_solutions[stepIndex];
      const normalizedAnswer = normalizeAnswer(currentAnswer);
      
      // Enhanced step validation using the new validation function
      const possibleAnswers = language === 'en' ? 
        currentStepSolution.possible_answers : 
        currentStepSolution.possible_answers_ar;
      
      const stepInstruction = language === 'en' ? 
        currentStepSolution.step_en : 
        currentStepSolution.step_ar;
      
      // FIXED: Use enhanced validation with sign flipping support
      const isStepCorrect = validateInequalityStep(currentAnswer, possibleAnswers, stepInstruction);
      
      if (isStepCorrect) {
        // Step is correct - FIXED: Use business rule validation
        const newStepResults = [...stepResults];
        newStepResults[stepIndex] = true;
        setStepResults(newStepResults);
        
        // CRITICAL: Enforce correct number of steps using business rules
        const stepValidation = validateStepProgression(problem.type, problem.id, stepIndex, problem);
        
        if (!stepValidation.complete) {
          // Move to next step
          setCurrentStep(stepValidation.nextStep);
          setShowEncouragement(`✅ ${stepValidation.message}`);
          setTimeout(() => setShowEncouragement(''), 3000);
        } else {
          // All required steps complete - now require final answer if needed
          if (problem.final_answer_required) {
            setAllStepsComplete(true);
            setShowEncouragement(`✅ ${stepValidation.message}`);
            setTimeout(() => setShowEncouragement(''), 3000);
          } else {
            // Complete the problem and submit to backend
            setAllStepsComplete(true);
            setIsCorrect(true);
            setShowEncouragement(`✅ ${stepValidation.message}`);
            setTimeout(() => submitToBackend(), 1000);
          }
        }
      } else {
        // Step is incorrect - Enhanced error feedback with hints after multiple attempts
        setAttempts(prev => prev + 1);
        
        let errorMessage;
        if (attempts >= 1) {
          errorMessage = language === 'en' 
            ? `${text[language].encouragement[Math.floor(Math.random() * text[language].encouragement.length)]} 💡 Tip: Review the Explanation stage for help!`
            : `${text[language].encouragement[Math.floor(Math.random() * text[language].encouragement.length)]} 💡 نصيحة: راجع مرحلة الشرح للمساعدة!`;
        } else {
          errorMessage = text[language].encouragement[Math.floor(Math.random() * text[language].encouragement.length)];
        }
        
        setShowEncouragement(errorMessage);
        setTimeout(() => setShowEncouragement(''), 7000); // Extended to 7 seconds
      }
    } catch (error) {
      console.error('Error checking step:', error);
    } finally {
      // Hide loading indicator
      setIsChecking(false);
      setCheckingStepIndex(-1);
    }
  };

  const handleSubmit = async () => {
    setIsChecking(true);
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    try {
      const stageType = getStageType(problem.type, problem.id);
      
      switch (stageType) {
        case 'preparation':
          await handlePreparationStage();
          break;
        case 'explanation':
          await handleExplanationStage();
          break;
        case 'practice':
          await handlePracticeStage();
          break;
        case 'practice_word':
          await handlePracticeWordStage();
          break;
        case 'assessment':
          await handleAssessmentStage();
          break;
        default:
          await handlePreparationStage();
      }
    } catch (error) {
      console.error('Error submitting answer:', error);
    } finally {
      setIsChecking(false);
    }
  };

  // 1. PREPARATION STAGE: Final answer only with auto-hints
  const handlePreparationStage = async () => {
    console.log('🎯 PREPARATION STAGE: Final answer with auto-hints');
    
    const userSubmittedAnswer = userAnswer?.trim();
    if (!userSubmittedAnswer) {
      setShowEncouragement(language === 'en' ? 'Please enter your final answer.' : 'يرجى إدخال إجابتك النهائية.');
      setTimeout(() => setShowEncouragement(''), 3000);
      return;
    }
    
    const normalizedUserAnswer = normalizeAnswer(userSubmittedAnswer);
    const normalizedCorrectAnswer = normalizeAnswer(problem.answer || '');
    
    const acceptableAnswers = [
      normalizedCorrectAnswer,
      normalizedCorrectAnswer.replace('x=', ''),
      'x=' + normalizedCorrectAnswer.replace('x=', ''),
    ].filter(Boolean);
    
    const isCorrect = acceptableAnswers.includes(normalizedUserAnswer);
    
    if (isCorrect) {
      // ✅ CORRECT ANSWER
      setIsCorrect(true);
      const successMessage = language === 'en' 
        ? `🎉 Excellent! That's correct! Ready to learn the step-by-step process?`
        : `🎉 ممتاز! هذا صحيح! جاهز لتعلم العملية خطوة بخطوة؟`;
      
      setShowEncouragement(successMessage);
      setTimeout(() => setShowEncouragement(''), 5000);
      await submitToBackend();
    } else {
      // ❌ WRONG ANSWER - Auto-show hints
      setIsCorrect(false);
      setAttempts(prev => prev + 1);
      const currentAttempts = attempts + 1;
      
      if (currentAttempts === 1) {
        // First wrong attempt - Use progressive hints from database
        let errorMessage = language === 'en' ? 'Not quite right.' : 'ليس صحيحاً تماماً.';
        
        // Use backend hints directly for progressive guidance
        const backendHints = language === 'en' ? problem.hints_en : problem.hints_ar;
        const firstHint = backendHints?.[0] || '';
        
        if (firstHint) {
          errorMessage += ` 💡 ${firstHint}`;
        } else {
          // Fallback to old system if no backend hints
          const guidanceHint = generateGuidanceHint(problem, 1);
          const pedagogicalHint = language === 'en' ? guidanceHint.en : guidanceHint.ar;
          errorMessage += ` 💡 ${pedagogicalHint}`;
        }
        setHintsUsed(1);
        
        setShowEncouragement(errorMessage);
        setTimeout(() => setShowEncouragement(''), 8000);
        
      } else if (currentAttempts === 2) {
        // Second wrong attempt - Use second progressive hint from database
        let errorMessage = language === 'en' ? 'Still not quite right.' : 'ما زال ليس صحيحاً تماماً.';
        
        // Use backend hints directly for progressive guidance
        const backendHints = language === 'en' ? problem.hints_en : problem.hints_ar;
        const secondHint = backendHints?.[1] || '';
        
        if (secondHint) {
          errorMessage += ` 💡 ${secondHint}`;
        } else {
          // Fallback to old system if no backend hints
          const errorSpecificHint = generateErrorSpecificHint(userAnswer, [problem.answer], problem.type);
          const pedagogicalHint = language === 'en' ? errorSpecificHint.en : errorSpecificHint.ar;
          errorMessage += ` 💡 ${pedagogicalHint}`;
        }
        setHintsUsed(2);
        
        setShowEncouragement(errorMessage);
        setTimeout(() => setShowEncouragement(''), 8000);
        
      } else {
        // Third wrong attempt - guide to explanation
        const redirectMessage = language === 'en' 
          ? `Having trouble? Let's learn how to solve this step by step.`
          : `تواجه صعوبة؟ دعنا نتعلم كيفية حل هذا خطوة بخطوة.`;
        
        setShowEncouragement(redirectMessage);
        setShowRedirectionButton(true);
        setTimeout(() => setShowEncouragement(''), 6000);
      }
    }
    
    setIsSubmitted(true);
  };

  // 2. EXPLANATION STAGE: Teaching + step-by-step practice (handled in tabbed interface)
  const handleExplanationStage = async () => {
    // This is handled in the tabbed interface section
    console.log('📚 EXPLANATION STAGE: Handled in tabbed interface');
  };

  // 3. PRACTICE STAGE: Step-by-step guided (no hints)
  const handlePracticeStage = async () => {
    console.log('📝 PRACTICE STAGE: Step-by-step guided');
    
    const currentAnswer = stepAnswers[currentStep]?.trim() || '';
    
    if (!currentAnswer) {
      setShowEncouragement(language === 'en' 
        ? 'Please enter your answer for this step.'
        : 'يرجى إدخال إجابتك لهذه الخطوة.');
      setTimeout(() => setShowEncouragement(''), 3000);
      return;
    }
    
    const expectedStepAnswers = problem.step_solutions || [];
    const currentStepData = expectedStepAnswers[currentStep];
    
    if (!currentStepData) {
      console.error('No step data found for current step:', currentStep);
      return;
    }
    
    const normalizedUserAnswer = normalizeAnswer(currentAnswer);
    const possibleAnswers = language === 'en' ? currentStepData.possible_answers : currentStepData.possible_answers_ar;
    const stepInstruction = language === 'en' ? currentStepData.step_en : currentStepData.step_ar;
    
    // FIXED: Use enhanced validation with sign flipping support
    const isStepCorrect = validateInequalityStep(currentAnswer, possibleAnswers, stepInstruction);
    
    if (isStepCorrect) {
      // ✅ CORRECT STEP - FIXED: Use business rule validation
      const newStepResults = [...stepResults];
      newStepResults[currentStep] = true;
      setStepResults(newStepResults);
      
      // CRITICAL: Enforce correct number of steps using business rules
      const stepValidation = validateStepProgression(problem.type, problem.id, currentStep, problem);
      
      if (!stepValidation.complete) {
        // Move to next step
        setCurrentStep(stepValidation.nextStep);
        setAttempts(0);
        setShowEncouragement(`✅ ${stepValidation.message}`);
      } else {
        // All required steps complete
        setAllStepsComplete(true);
        setIsCorrect(true);
        setShowEncouragement(`✅ ${stepValidation.message}`);
        setTimeout(() => submitToBackend(), 1000);
      }
      
      setTimeout(() => setShowEncouragement(''), 4000);
      
    } else {
      // ❌ WRONG STEP - Specific feedback (no hints needed)
      const stepInstruction = language === 'en' ? currentStepData.step_en : currentStepData.step_ar;
      const feedback = language === 'en' 
        ? `Not quite. Remember: ${stepInstruction}`
        : `ليس تماماً. تذكر: ${stepInstruction}`;
      
      setShowEncouragement(feedback);
      setTimeout(() => setShowEncouragement(''), 6000);
    }
    
    setIsSubmitted(true);
  };

  // 4. ASSESSMENT & EXAM PREP: Final answer with score penalties
  const handleAssessmentStage = async () => {
    console.log('🏆 ASSESSMENT STAGE: Final answer with penalties');
    
    const userSubmittedAnswer = userAnswer?.trim();
    if (!userSubmittedAnswer) {
      setShowEncouragement(language === 'en' ? 'Please enter your final answer.' : 'يرجى إدخال إجابتك النهائية.');
      setTimeout(() => setShowEncouragement(''), 3000);
      return;
    }
    
    const normalizedUserAnswer = normalizeAnswer(userSubmittedAnswer);
    const normalizedCorrectAnswer = normalizeAnswer(problem.answer || '');
    
    const acceptableAnswers = [
      normalizedCorrectAnswer,
      normalizedCorrectAnswer.replace('x=', ''),
      'x=' + normalizedCorrectAnswer.replace('x=', ''),
    ].filter(Boolean);
    
    const isCorrect = acceptableAnswers.includes(normalizedUserAnswer);
    
    if (isCorrect) {
      // ✅ CORRECT ANSWER
      setIsCorrect(true);
      const scoreDisplay = currentScore < 100 
        ? `Score: ${currentScore}% - ${hintsUsed} hint${hintsUsed > 1 ? 's' : ''} used`
        : 'Score: 100% - Perfect!';
      
      const successMessage = language === 'en' 
        ? `✅ Correct! ${scoreDisplay}`
        : `✅ صحيح! النتيجة: ${currentScore}%`;
      
      setShowEncouragement(successMessage);
      setTimeout(() => setShowEncouragement(''), 5000);
      await submitToBackend();
    } else {
      // ❌ WRONG ANSWER - Auto-show hints with penalties
      setIsCorrect(false);
      setAttempts(prev => prev + 1);
      const currentAttempts = attempts + 1;
      
      if (currentAttempts <= 2) {
        // Deduct points for hint usage
        const newScore = currentScore - (15 * currentAttempts); // 15% penalty per hint
        setCurrentScore(Math.max(newScore, 10)); // Minimum 10%
        setHintsUsed(currentAttempts);
        
        const hintIndex = currentAttempts - 1;
        let errorMessage = language === 'en' ? 'Incorrect.' : 'غير صحيح.';
        
        // CRITICAL: Use progressive hints from database (never show direct answers)
        if (currentAttempts <= 3) {
          // Use backend hints directly for progressive guidance
          const backendHints = language === 'en' ? problem.hints_en : problem.hints_ar;
          const hintIndex = Math.min(currentAttempts - 1, (backendHints?.length || 3) - 1);
          const progressiveHint = backendHints?.[hintIndex] || '';
          
          if (progressiveHint) {
            errorMessage += ` 💡 ${progressiveHint}`;
          } else {
            // Fallback to old system if no backend hints
            const guidanceHint = generateGuidanceHint(problem, currentAttempts);
            const pedagogicalHint = language === 'en' ? guidanceHint.en : guidanceHint.ar;
            errorMessage += ` 💡 ${pedagogicalHint}`;
          }
        } else {
          // After 3 attempts, suggest going to explanation stage
          errorMessage += language === 'en' 
            ? ' 💡 Consider reviewing the Explanation stage for more guidance.'
            : ' 💡 فكر في مراجعة مرحلة الشرح للحصول على مزيد من التوجيه.';
        }
        
        const scoreDisplay = `Score: ${Math.max(newScore, 10)}% - ${currentAttempts} hint${currentAttempts > 1 ? 's' : ''} used`;
        errorMessage += ` (${scoreDisplay})`;
        
        setShowEncouragement(errorMessage);
        setTimeout(() => setShowEncouragement(''), 10000);
        
      } else {
        // Third attempt - redirect to explanation
        const redirectMessage = language === 'en' 
          ? `Review the Explanation stage to master this concept.`
          : `راجع مرحلة الشرح لإتقان هذا المفهوم.`;
        
        setShowEncouragement(redirectMessage);
        setShowRedirectionButton(true);
        setTimeout(() => setShowEncouragement(''), 6000);
      }
    }
    
    setIsSubmitted(true);
  };

  // 5. PRACTICE WORD PROBLEMS: 3-step process with hints visible from start
  const handlePracticeWordStage = async () => {
    console.log('📝 PRACTICE WORD PROBLEM: 3-step process with hints');
    
    const currentAnswer = stepAnswers[currentStep]?.trim() || '';
    
    if (!currentAnswer) {
      setShowEncouragement(language === 'en' 
        ? 'Please enter your answer for this step.'
        : 'يرجى إدخال إجابتك لهذه الخطوة.');
      setTimeout(() => setShowEncouragement(''), 3000);
      return;
    }
    
    const expectedStepAnswers = problem.step_solutions || [];
    const currentStepData = expectedStepAnswers[currentStep];
    
    if (!currentStepData) {
      console.error('No step data found for current step:', currentStep);
      return;
    }
    
    const normalizedUserAnswer = normalizeAnswer(currentAnswer);
    const possibleAnswers = language === 'en' ? currentStepData.possible_answers : currentStepData.possible_answers_ar;
    const stepInstruction = language === 'en' ? currentStepData.step_en : currentStepData.step_ar;
    
    // Use enhanced validation
    const isStepCorrect = validateInequalityStep(currentAnswer, possibleAnswers, stepInstruction);
    
    if (isStepCorrect) {
      // ✅ CORRECT STEP
      console.log(`✅ Step ${currentStep + 1} correct for practice word problem`);
      
      const requiredSteps = getRequiredSteps(problem.type, problem.id, problem);
      
      if (currentStep < requiredSteps - 1) {
        // Move to next step
        setCurrentStep(prev => prev + 1);
        const nextStepMessage = language === 'en' 
          ? `Great! Step ${currentStep + 1} complete. Continue to Step ${currentStep + 2}.`
          : `رائع! تم إكمال الخطوة ${currentStep + 1}. انتقل للخطوة ${currentStep + 2}.`;
        
        setShowEncouragement(nextStepMessage);
        setTimeout(() => setShowEncouragement(''), 3000);
      } else {
        // All steps complete
        console.log('🎉 PRACTICE WORD PROBLEM COMPLETED: All 3 steps finished!');
        console.log(`🔍 Problem ID: ${problemId}, Current Step: ${currentStep}, Required Steps: ${getRequiredSteps(problem.type, problem.id, problem)}`);
        
        setAllStepsComplete(true);
        setIsCorrect(true);
        
        const completionMessage = language === 'en' 
          ? `🎉 Excellent! You've completed all 3 steps of this word problem!`
          : `🎉 ممتاز! لقد أكملت جميع الخطوات الثلاث لهذه المسألة الكلامية!`;
        
        setShowEncouragement(completionMessage);
        setTimeout(() => setShowEncouragement(''), 5000);
        
        console.log('🚀 Submitting to backend and updating progress...');
        await submitToBackend();
        console.log('✅ Backend submission completed, allStepsComplete should trigger Continue button');
      }
    } else {
      // ❌ WRONG ANSWER - Show progressive hints (hints are already visible)
      setIsCorrect(false);
      setAttempts(prev => prev + 1);
      const currentAttempts = attempts + 1;
      
      if (currentAttempts <= 2) {
        // Show encouragement and additional hint
        const backendHints = language === 'en' ? problem.hints_en : problem.hints_ar;
        const hintIndex = Math.min(currentAttempts - 1, backendHints?.length - 1 || 0);
        const additionalHint = backendHints?.[hintIndex] || '';
        
        let errorMessage = language === 'en' 
          ? `Not quite right for Step ${currentStep + 1}. Try again!`
          : `ليس صحيحاً تماماً للخطوة ${currentStep + 1}. حاول مرة أخرى!`;
        
        if (additionalHint && currentAttempts > 1) {
          errorMessage += ` 💡 ${additionalHint}`;
        }
        
        setShowEncouragement(errorMessage);
        setTimeout(() => setShowEncouragement(''), 8000);
      } else {
        // Third attempt - redirect to explanation of SAME section
        const redirectMessage = language === 'en' 
          ? `Let's review the explanation for this section to master this concept.`
          : `لنراجع شرح هذا القسم لإتقان هذا المفهوم.`;
        
        setShowEncouragement(redirectMessage);
        setShowRedirectionButton(true);
        setTimeout(() => setShowEncouragement(''), 6000);
      }
    }
    
    setIsSubmitted(true);
  };

  // Helper function to get current section number from problem  
  const getCurrentSection = () => {
    if (problemId?.includes('1') || problem?.section_id === 'section1') return 1;
    if (problemId?.includes('2') || problem?.section_id === 'section2') return 2;
    if (problemId?.includes('3') || problem?.section_id === 'section3') return 3;
    if (problemId?.includes('4') || problem?.section_id === 'section4') return 4;
    if (problemId?.includes('5') || problem?.section_id === 'section5') return 5;
    return 1; // Default to section 1
  };

  // NAVIGATION CONTEXT FIX: Helper to save navigation context
  const saveNavigationContext = (section, stage = null) => {
    const context = {
      section: `section${section}`,
      stage: stage,
      timestamp: Date.now()
    };
    localStorage.setItem('mathapp_navigation_context', JSON.stringify(context));
  };

  // NAVIGATION CONTEXT FIX: Navigate back to dashboard with context preservation
  const navigateToSectionDashboard = () => {
    const currentSection = getCurrentSection();
    saveNavigationContext(currentSection);
    navigate('/dashboard');
  };

  // NAVIGATION CONTEXT FIX: Redirect to correct section's explanation after failure
  const redirectToExplanation = () => {
    const currentSection = getCurrentSection();
    navigate(`/section${currentSection}/explanation`);
  };

  const submitToBackend = async () => {
    // Get the user's actual answer
    const userSubmittedAnswer = problem.step_solutions ? 
      (stepAnswers[problem.step_solutions.length - 1] || userAnswer) : 
      (stepAnswers[0] || userAnswer);
      
    const response = await fetch(
      `${process.env.REACT_APP_BACKEND_URL}/api/students/${user.username}/attempt`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          problem_id: problemId,
          answer: userSubmittedAnswer, // FIXED: Send user's answer, not correct answer
          hints_used: hintsUsed
        }),
      }
    );

    if (response.ok) {
      const result = await response.json();
      setAttempts(result.attempts);
      setIsCorrect(true);
      setIsSubmitted(true);
      
      toast({
        title: text[language].correct,
        description: `${text[language].points}: ${result.score}`,
      });
      
      // FIXED: Complete stage immediately with proper progress tracking
      const currentSection = getCurrentSection();
      await completeStage(currentSection, problemId);
      
      // Update progress immediately
      console.log('🔄 Updating progress after successful submission...');
      await fetchData();
      console.log('✅ Progress update completed');
      
      // Add explicit progress check
      setTimeout(async () => {
        console.log('🔍 Checking if progress was updated properly...');
        await fetchData();
        console.log('🔍 Final progress check completed');
      }, 1000);
    }
  };

  // PROGRESS FIX: Complete stage and update both backend and frontend
  const completeStage = async (section, stage) => {
    console.log(`🎯 Completing stage: section${section}_${stage}`);
    
    try {
      // Update backend via API
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/updateProgress`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: user.username,
          section: section,
          stage: stage,
          status: 'complete'
        })
      });
      
      if (response.ok) {
        console.log('✅ Backend progress updated successfully');
      }
    } catch (error) {
      console.log('⚠️ Backend update failed, continuing with localStorage update:', error);
    }
    
    // Update localStorage immediately for instant UI feedback
    const progress = JSON.parse(localStorage.getItem('progress') || '{}');
    progress[`section${section}_${stage}`] = 'complete';
    localStorage.setItem('progress', JSON.stringify(progress));
    console.log(`✅ localStorage updated: section${section}_${stage} = complete`);
    
    // Check if Assessment should unlock
    checkAndUnlockAssessment(section);
  };

  // PROGRESS FIX: Check and unlock assessment when both practice stages are complete
  const checkAndUnlockAssessment = (section) => {
    console.log(`🔍 Checking if Assessment should unlock for section ${section}`);
    
    const progress = JSON.parse(localStorage.getItem('progress') || '{}');
    const practice1Complete = progress[`section${section}_practice${section}_1`] === 'complete' || 
                              progress[`section${section}_practice1`] === 'complete';
    const practice2Complete = progress[`section${section}_practice${section}_2`] === 'complete' || 
                              progress[`section${section}_practice2`] === 'complete';
    
    console.log(`🔍 Practice1 complete: ${practice1Complete}, Practice2 complete: ${practice2Complete}`);
    
    if (practice1Complete && practice2Complete) {
      console.log('🎉 Both practice stages complete - Assessment should unlock!');
      
      // Mark assessment as unlocked in localStorage
      progress[`section${section}_assessment_unlocked`] = true;
      localStorage.setItem('progress', JSON.stringify(progress));
      
      // Force refresh progress from backend to update UI
      setTimeout(() => {
        fetchData();
      }, 500);
    }
  };

  // Helper function to get correct hint text based on language
  const getHintText = (stage, step, language) => {
    // CHECK the current language setting
    const isEnglish = language === 'en' || localStorage.getItem('language') === 'en';
    
    const hints = {
      'explanation_step1': {
        ar: 'اقسم كلا الطرفين على 4',
        en: 'Divide both sides by 4'
      },
      'explanation_step2': {
        ar: 'بسّط الطرفين',
        en: 'Simplify both sides'
      },
      'practice_step1': {
        ar: 'اكتب المتباینة من الكلمات',
        en: 'Write the inequality from the word problem'
      },
      'practice_step2': {
        ar: 'قم بالعملية الحسابية',
        en: 'Perform the mathematical operation'
      },
      'practice_step3': {
        ar: 'بسّط للحصول على الإجابة النهائية',
        en: 'Simplify to get the final answer'
      }
    };
    
    return hints[`${stage}_step${step}`]?.[isEnglish ? 'en' : 'ar'];
  };

  // Fix navigation button not working - force navigation
  const handleNavigationClick = () => {
    // Prevent multiple navigation attempts
    if (navigationInProgress) {
      console.log('🔄 Navigation already in progress, ignoring duplicate call');
      return;
    }
    
    setNavigationInProgress(true);
    
    // Get the next stage using existing logic
    const getSectionNumber = (id) => {
      const match = id.match(/[a-zA-Z]+(\d+)/);
      return match ? parseInt(match[1]) : 1;
    };
    
    const currentSectionNum = getSectionNumber(problemId);
    
    const sectionSequences = {
      1: ['prep1', 'explanation1', 'practice1', 'practice2', 'assessment1', 'examprep1'],
      2: ['prep2', 'explanation2', 'practice2_1', 'practice2_2', 'assessment2', 'examprep2'],
      3: ['prep3', 'explanation3', 'practice3_1', 'practice3_2', 'assessment3', 'examprep3'],
      4: ['prep4', 'explanation4', 'practice4_1', 'practice4_2', 'assessment4', 'examprep4'],
      5: ['prep5', 'explanation5', 'practice5_1', 'practice5_2', 'assessment5', 'examprep5']
    };
    
    const currentSequence = sectionSequences[currentSectionNum] || sectionSequences[1];
    const currentIndex = currentSequence.indexOf(problemId);
    
    let nextStage = null;
    if (currentIndex < currentSequence.length - 1) {
      nextStage = `/problem/${currentSequence[currentIndex + 1]}`;
    } else {
      // Move to next section
      const nextSectionNum = currentSectionNum + 1;
      if (nextSectionNum <= 5 && sectionSequences[nextSectionNum]) {
        nextStage = `/problem/${sectionSequences[nextSectionNum][0]}`;
      } else {
        nextStage = '/dashboard';
      }
    }
    
    if (nextStage) {
      console.log(`🚀 FORCE NAVIGATION: Navigating to ${nextStage}`);
      
      // Don't just update URL, actually navigate
      resetProblemState();
      
      // Try React Router navigate first
      try {
        navigate(nextStage);
        
        // Force component reload if navigation doesn't work
        setTimeout(() => {
          if (window.location.pathname !== nextStage) {
            console.log(`🔄 React Router failed, forcing with window.location`);
            window.location.href = nextStage;
          }
          // Reset navigation flag after navigation attempt
          setNavigationInProgress(false);
        }, 100);
        
      } catch (error) {
        console.error('Navigation error:', error);
        // Fallback: Force navigation with window.location
        window.location.href = nextStage;
        setNavigationInProgress(false);
      }
    } else {
      setNavigationInProgress(false);
    }
  };

  const resetProblemState = () => {
    setStepAnswers(['', '', '']);
    setCurrentStep(0);
    setCurrentHint(0);
    setShowHints([false, false, false]);
    setIsSubmitted(false);
    setIsCorrect(false);
    setStepResults([false, false, false]);
    setAllStepsComplete(false);
    setUserAnswer('');
    setCurrentExample(0);
    setShowExample(false);
    setPracticeAnswer('');
    setPracticeComplete([]);
    setHintsUsed(0);
    setShowEncouragement('');
    setAttempts(0);
    setShowVoiceInput(false);
    setShowMathKeyboard(false);
    setShowRedirectionButton(false);
    setNavigationInProgress(false); // Reset navigation flag
    setCurrentScore(100); // Reset score
    setExplanationStep(0); // Reset explanation step
    setExplanationAnswers(['', '', '']); // Reset explanation answers
    setExplanationStepHistory([]); // Reset explanation step history
  };

  const handleNextProblem = () => {
    // FIXED: Dynamic section-aware navigation for all sections
    const getSectionNumber = (id) => {
      // CRITICAL FIX: Match first digit after letters, not last digit in string
      // This fixes practice2_1 returning 2 instead of 1
      const match = id.match(/[a-zA-Z]+(\d+)/);
      return match ? parseInt(match[1]) : 1;
    };
    
    const currentSectionNum = getSectionNumber(problemId);
    
    // Define problem sequences for each section
    const sectionSequences = {
      1: ['prep1', 'explanation1', 'practice1', 'practice2', 'assessment1', 'examprep1'],
      2: ['prep2', 'explanation2', 'practice2_1', 'practice2_2', 'assessment2', 'examprep2'],
      3: ['prep3', 'explanation3', 'practice3_1', 'practice3_2', 'assessment3', 'examprep3'],
      4: ['prep4', 'explanation4', 'practice4_1', 'practice4_2', 'assessment4', 'examprep4'],
      5: ['prep5', 'explanation5', 'practice5_1', 'practice5_2', 'assessment5', 'examprep5']
    };
    
    const currentSequence = sectionSequences[currentSectionNum] || sectionSequences[1];
    const currentIndex = currentSequence.indexOf(problemId);
    
    console.log(`🎯 Navigation: ${problemId} (section ${currentSectionNum}, index ${currentIndex})`);
    
    if (currentIndex < currentSequence.length - 1) {
      // Move to next problem in same section
      const nextProblemId = currentSequence[currentIndex + 1];
      console.log(`🎯 Next problem in section ${currentSectionNum}: ${nextProblemId}`);
      resetProblemState();
      navigate(`/problem/${nextProblemId}`);
    } else {
      // Completed current section - move to next section
      const nextSectionNum = currentSectionNum + 1;
      if (nextSectionNum <= 5 && sectionSequences[nextSectionNum]) {
        const nextSectionFirstProblem = sectionSequences[nextSectionNum][0];
        console.log(`🎯 Completed section ${currentSectionNum} - moving to section ${nextSectionNum}: ${nextSectionFirstProblem}`);
        resetProblemState();
        navigate(`/problem/${nextSectionFirstProblem}`);
      } else {
        // All sections completed
        console.log('🎯 All sections completed - returning to dashboard');
        navigateToSectionDashboard();
      }
    }
  };

  const handleGoToExplanation = () => {
    // FIXED: Navigate to explanation stage of CURRENT section, not always explanation1
    const getSectionNumber = (id) => {
      const match = id.match(/(\d+)$/);
      return match ? parseInt(match[1]) : 1;
    };
    
    const currentSectionNum = getSectionNumber(problemId);
    const explanationId = `explanation${currentSectionNum}`;
    
    console.log(`🔄 Navigating to explanation stage for section ${currentSectionNum}: ${explanationId}`);
    resetProblemState();
    navigate(`/problem/${explanationId}`);
  };

  const handleTryAgain = () => {
    resetProblemState();
  };

  // Voice input handlers
  const handleVoiceResult = (result) => {
    if (problem?.type === 'explanation') {
      // For explanation stage, update the current example's answer
      const newAnswers = [...explanationAnswers];
      newAnswers[currentExample] = result;
      setExplanationAnswers(newAnswers);
    } else if (problem?.step_solutions && problem.step_solutions.length > 0) {
      const newAnswers = [...stepAnswers];
      newAnswers[activeInputIndex] = result;
      setStepAnswers(newAnswers);
    } else {
      setUserAnswer(result);
    }
    setShowVoiceInput(false);
  };

  const handleVoiceError = (error) => {
    toast({
      title: language === 'ar' ? 'خطأ في الإدخال الصوتي' : 'Voice Input Error',
      description: error,
      variant: 'destructive'
    });
  };

  // Math keyboard handlers
  const handleSymbolSelect = (symbol) => {
    insertSymbolAtCursor(symbol);
  };

  const handleNumberSelect = (number) => {
    insertSymbolAtCursor(number);
  };

  const handleOperatorSelect = (operator) => {
    insertSymbolAtCursor(` ${operator} `);
  };

  const handleKeyboardAction = (action) => {
    switch (action) {
      case 'clear':
        if (problem.type === 'explanation') {
          // Clear the current example's answer
          const newAnswers = [...explanationAnswers];
          newAnswers[currentExample] = '';
          setExplanationAnswers(newAnswers);
        } else if (problem?.step_solutions && problem.step_solutions.length > 0) {
          const newAnswers = [...stepAnswers];
          newAnswers[activeInputIndex] = '';
          setStepAnswers(newAnswers);
        } else {
          setUserAnswer('');
        }
        break;
      case 'backspace':
        if (problem.type === 'explanation') {
          // Backspace the current example's answer
          const newAnswers = [...explanationAnswers];
          newAnswers[currentExample] = newAnswers[currentExample].slice(0, -1);
          setExplanationAnswers(newAnswers);
        } else if (problem?.step_solutions && problem.step_solutions.length > 0) {
          const newAnswers = [...stepAnswers];
          const current = newAnswers[activeInputIndex] || '';
          newAnswers[activeInputIndex] = current.slice(0, -1);
          setStepAnswers(newAnswers);
        } else {
          setUserAnswer(prev => prev.slice(0, -1));
        }
        break;
      case 'voice':
        setShowVoiceInput(!showVoiceInput);
        setShowMathKeyboard(false);
        break;
    }
  };

  const insertSymbolAtCursor = (symbol) => {
    // Use Practice stage logic for Explanation stage (simplified management)
    if (problem.type === 'explanation') {
      console.log('🔍 Explanation keyboard input:', symbol, 'currentExample:', currentExample);
      
      // Update the current example's answer - same logic as Practice stage
      const newAnswers = [...explanationAnswers];
      const currentValue = newAnswers[currentExample] || '';
      newAnswers[currentExample] = currentValue + symbol;
      setExplanationAnswers(newAnswers);
      
      console.log('🔍 Updated explanation answer for example', currentExample, ':', newAnswers[currentExample]);
    } else if (problem.type === 'preparation') {
      setUserAnswer(prev => prev + symbol);
    } else if (problem?.step_solutions && problem.step_solutions.length > 0) {
      // Practice stage - this is the working code we're copying
      const newAnswers = [...stepAnswers];
      const currentValue = newAnswers[activeInputIndex] || '';
      newAnswers[activeInputIndex] = currentValue + symbol;
      setStepAnswers(newAnswers);
    } else {
      setUserAnswer(prev => prev + symbol);
    }
  };

  const handleInputFocus = (index) => {
    setActiveInputIndex(index);
  };

  const getStepLabel = (stepIndex, step) => {
    if (!step) return '';
    
    const labels = {
      en: {
        0: "Step 1: Isolate variable term",
        1: "Step 2: Solve for the variable", 
        2: "Step 3: Write final answer"
      },
      ar: {
        0: "الخطوة ١: عزل حد المتغير",
        1: "الخطوة ٢: حل للمتغير",
        2: "الخطوة ٣: كتابة الإجابة النهائية"
      }
    };
    
    return labels[language][stepIndex] || `${language === 'en' ? 'Step' : 'الخطوة'} ${stepIndex + 1}`;
  };

  const handleStepHintToggle = (stepIndex) => {
    const newShowHints = [...showHints];
    newShowHints[stepIndex] = !newShowHints[stepIndex];
    setShowHints(newShowHints);
    if (!newShowHints[stepIndex]) {
      setHintsUsed(hintsUsed + 1);
    }
  };

  const handleNextHint = () => {
    if (currentHint < ((language === 'en' ? problem.hints_en : problem.hints_ar)?.length || 0) - 1) {
      setCurrentHint(currentHint + 1);
    }
    setShowHints(true);
  };

  const handleStepAnswerChange = (stepIndex, value) => {
    const newAnswers = [...stepAnswers];
    newAnswers[stepIndex] = value;
    setStepAnswers(newAnswers);
  };

  const renderMathExpression = (expression) => {
    return (
      <div className="text-3xl font-mono bg-gray-50 p-6 rounded-lg border text-center">
        {expression}
      </div>
    );
  };

  if (loading || !problem) {
    return <div className="min-h-screen flex items-center justify-center">
      <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-emerald-500"></div>
    </div>;
  }

  // Show completion screen when section is finished
  if (showCompletionScreen) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <Card className="w-full max-w-md mx-auto bg-gradient-to-br from-green-50 to-emerald-50 border-green-200 shadow-xl">
          <CardContent className="p-8 text-center">
            <div className="mb-6">
              <div className="text-6xl mb-4">
                {completionType === 'final' ? '🎉' : '🏆'}
              </div>
              <h1 className="text-2xl font-bold text-green-800 mb-2">
                {completionType === 'final' 
                  ? text[language].completion.finalTitle 
                  : text[language].completion.sectionTitle}
              </h1>
              <p className="text-green-700 leading-relaxed">
                {completionType === 'final' 
                  ? text[language].completion.finalMessage 
                  : text[language].completion.sectionMessage}
              </p>
            </div>
            
            <Button 
              onClick={() => navigateToSectionDashboard()}
              className="w-full h-12 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700"
            >
              {text[language].completion.returnToDashboard}
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  // FIXED: Dynamic section-aware progress display
  const getSectionNumber = (id) => {
    const match = id.match(/(\d+)$/);
    return match ? parseInt(match[1]) : 1;
  };

  const currentSectionNum = problemId ? getSectionNumber(problemId) : 1;
  const sectionKey = `section${currentSectionNum}`;
  const problemProgress = userProgress?.[sectionKey]?.[problemId] || { completed: false, score: 0, attempts: 0 };
  const isCompleted = problemProgress.completed;
  const earnedScore = problemProgress.score;

  return (
    <div className="min-h-screen p-4">
      {/* Header - FIXED: Reduced margin */}
      <div className="flex justify-between items-center mb-4 max-w-7xl mx-auto problem-view-header">
        <Button onClick={() => navigateToSectionDashboard()} variant="outline">
          <ArrowLeft className="w-4 h-4 mr-2" />
          {text[language].back}
        </Button>
        <div className="flex gap-2">
          <Button 
            onClick={() => setShowRulesModal(true)}
            variant="outline" 
            size="sm"
            className="text-blue-600 border-blue-300 hover:bg-blue-50"
            title={language === 'en' ? 'Show solving rules' : 'عرض قواعد الحل'}
          >
            <HelpCircle className="w-4 h-4" />
          </Button>
          <Button onClick={toggleLanguage} variant="outline" size="sm">
            <Globe className="w-4 h-4 mr-2" />
            {language === 'en' ? 'العربية' : 'English'}
          </Button>
        </div>
      </div>

      {/* Main Content Container - Expanded Width */}
      <div className="max-w-7xl mx-auto w-full">
        {/* Problem Header - FIXED: Reduced margin */}
        <Card className="mb-4 problem-card">
          <CardHeader>
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-4">
                <Badge variant={
                  problem.type === 'preparation' ? 'secondary' :
                  problem.type === 'explanation' ? 'outline' :
                  problem.type === 'practice' ? 'default' :
                  problem.type === 'assessment' ? 'destructive' : 'secondary'
                }>
                  {problem.type.charAt(0).toUpperCase() + problem.type.slice(1)}
                </Badge>
                <span className="text-sm text-gray-500">
                  {text[language].weight}: {problem.weight}%
                </span>
                <span className="text-sm text-gray-500">
                  {text[language].attempts}: {attempts}
                </span>
              </div>
              {isCompleted && (
                <div className="flex items-center text-green-600">
                  <CheckCircle className="w-5 h-5 mr-2" />
                  <span className="font-semibold">{earnedScore}%</span>
                </div>
              )}
            </div>
          </CardHeader>
        </Card>

        <div className="grid grid-cols-1 gap-6">
          {/* Problem Card - FIXED: Compact layout */}
          <Card className="w-full problem-display">
            <CardHeader className="pb-3">
              <CardTitle className="text-center problem-title">
                {language === 'en' ? 'Solve the inequality:' : 'حل المتباينة:'}
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-0 problem-math-display">
              <div className="math-expression-container">
                {renderMathExpression(language === 'en' ? problem.question_en : problem.question_ar)}
              </div>
                
            {/* COMPREHENSIVE EXPLANATION STAGE CONTENT - FIXED: Section title positioning */}
            {problem.show_full_solution && problem.explanation_en && (
              <Card className="mb-4 w-full">
                <CardContent className="p-8">
                  <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-8 rounded-lg border-l-4 border-blue-500 mb-4 section-title-container">
                    <h3 className="font-bold text-2xl mb-4 text-blue-800 flex items-center justify-center explanation-section-title">
                      <BookOpen className="w-8 h-8 mr-3" />
                      {language === 'en' ? 'Complete Guide to Solving Inequalities' : 'دليل شامل لحل المتباينات'}
                    </h3>
                    
                    <div className="prose prose-blue max-w-none text-lg">
                      <div className="whitespace-pre-wrap text-blue-700 leading-relaxed">
                        {language === 'en' ? problem.explanation_en : problem.explanation_ar}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* INTERACTIVE PRACTICE EXAMPLES - FIXED: Reduced spacing */}
            {problem.interactive_examples && !problem.show_full_solution && (
              <Card className="mb-4 w-full">
                <CardHeader className="pb-4">
                  <CardTitle className="text-center text-2xl font-bold text-gray-800">
                    {language === 'en' ? '🎯 Practice Examples' : '🎯 أمثلة تطبيقية'}
                  </CardTitle>
                  <p className="text-center text-gray-600 text-base">
                    {language === 'en' 
                      ? 'Practice what you learned with these guided examples'
                      : 'تدرب على ما تعلمته مع هذه الأمثلة الموجهة'}
                  </p>
                </CardHeader>
                
                <CardContent className="p-8">
                  {/* TABBED NAVIGATION - MOBILE OPTIMIZED HORIZONTAL SCROLLING */}
                  <div className="border-b border-gray-200 mb-8">
                    <div className="explanation-tabs-container overflow-x-auto pb-2">
                      <nav className="-mb-px flex min-w-max md:justify-center space-x-6 md:space-x-12" aria-label="Tabs">
                        {problem.interactive_examples.map((example, index) => (
                          <button
                            key={index}
                            onClick={() => {
                              setCurrentExample(index);
                              setShowExample(false); // Reset to show button state
                              setPracticeAnswer(''); // Clear practice answer when switching tabs
                            }}
                            className={`explanation-tab-button flex-shrink-0 whitespace-nowrap py-3 px-4 md:px-6 border-b-2 font-semibold text-sm md:text-lg min-w-[120px] md:min-w-0 ${
                              currentExample === index
                                ? 'border-blue-500 text-blue-600'
                                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                            }`}
                          >
                            {language === 'en' ? example.title_en : example.title_ar}
                          </button>
                        ))}
                      </nav>
                    </div>
                  </div>

                  {/* SINGLE EXAMPLE CONTENT - FULL WIDTH */}
                  {problem.interactive_examples.map((example, index) => (
                    currentExample === index && (
                      <div key={index} className="w-full max-w-6xl mx-auto">
                        {/* Example Header */}
                        <div className="text-center mb-8">
                          <h3 className="font-bold text-3xl text-blue-700 mb-6">
                            {language === 'en' ? example.title_en : example.title_ar}
                          </h3>
                          <div className="bg-gray-100 p-8 rounded-lg max-w-2xl mx-auto">
                            <div className="text-3xl font-mono text-center text-gray-800">
                              {language === 'en' ? example.problem_en : example.problem_ar}
                            </div>
                          </div>
                        </div>

                        {/* Show Solution Button - Only for read-only mode */}
                        {!showExample && problem.show_full_solution && (
                          <div className="text-center mb-8">
                            <Button 
                              onClick={() => setShowExample(true)}
                              className="px-12 py-4 text-xl bg-blue-500 hover:bg-blue-600"
                              variant="default"
                            >
                              {language === 'en' ? '👁️ Show Solution' : '👁️ إظهار الحل'}
                            </Button>
                          </div>
                        )}

                        {/* Interactive Step-by-Step Mode - For interactive explanation stages */}
                        {!problem.show_full_solution && (
                          <div>
                            {/* Display the step-by-step solution first */}
                            <div className="bg-green-50 p-8 rounded-lg mb-8 border border-green-200 max-w-5xl mx-auto">
                              <h4 className="font-bold text-2xl text-green-800 mb-6">
                                {language === 'en' ? '💡 Step-by-Step Solution:' : '💡 الحل خطوة بخطوة:'}
                              </h4>
                              <pre className="whitespace-pre-wrap text-lg text-green-700 leading-relaxed font-mono">
                                {language === 'en' ? example.solution_en : example.solution_ar}
                              </pre>
                            </div>
                            
                            {/* Display the practice question directly */}
                            <div className="bg-yellow-50 p-8 rounded-lg border border-yellow-200 max-w-3xl mx-auto mb-6">
                              <h4 className="font-bold text-2xl text-yellow-800 mb-6 text-center">
                                {language === 'en' ? '✏️ Interactive Practice:' : '✏️ تدريب تفاعلي:'}
                              </h4>
                              
                              <div className="text-center mb-6">
                                <div className="bg-white p-6 rounded border text-2xl font-mono text-gray-800 max-w-lg mx-auto">
                                  {language === 'en' ? example.practice_question_en : example.practice_question_ar}
                                </div>
                              </div>
                              
                              {/* RESTORED: Step-by-Step Practice with Simplified Input Management */}
                              <div className="space-y-6">
                                {/* Dynamic Multi-Step System */}
                                {(() => {
                                  // Determine how many steps this level has
                                  const levelSteps = problem.step_solutions?.filter(step => 
                                    step.step_en.includes(`Level ${index + 1}B Step`)
                                  ) || [];
                                  
                                  const currentStepIndex = explanationStep;
                                  const currentStep = levelSteps[currentStepIndex];
                                  
                                  if (!currentStep) return null;
                                  
                                  return (
                                    <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                                      <h5 className="font-semibold text-blue-800 mb-3">
                                        {language === 'ar' ? currentStep.step_ar : currentStep.step_en}
                                      </h5>
                                      
                                      {/* Show previous steps */}
                                      {explanationStep > 0 && (
                                        <div className="mb-3">
                                          <p className="text-sm text-gray-600 mb-2">
                                            {language === 'en' ? 'Your previous steps:' : 'خطواتك السابقة:'}
                                          </p>
                                          {explanationStepHistory.slice(0, explanationStep).map((stepAnswer, stepIdx) => (
                                            stepAnswer && (
                                              <div key={stepIdx} className="mb-2 p-2 bg-green-100 rounded text-center text-sm text-green-800 border border-green-300">
                                                <span className="inline-block bg-green-200 px-2 py-1 rounded-full text-xs font-semibold mr-2">
                                                  {language === 'en' ? `Step ${stepIdx + 1}` : `الخطوة ${stepIdx + 1}`}
                                                </span>
                                                <span className="font-mono">{stepAnswer}</span>
                                              </div>
                                            )
                                          ))}
                                        </div>
                                      )}
                                      
                                      {/* Symbol Shortcut Buttons */}
                                      <div className="symbol-buttons-container flex flex-wrap justify-center gap-2 md:flex-nowrap mb-3">
                                        {['<', '>', '≤', '≥', '=', '≠', '|'].map((symbol) => (
                                          <Button
                                            key={symbol}
                                            variant="outline"
                                            className="symbol-button px-3 py-2 text-lg font-mono border-gray-300 hover:bg-gray-50 min-w-[45px] h-[45px] flex-shrink-0"
                                            onClick={() => {
                                              const newAnswers = [...explanationAnswers];
                                              newAnswers[index] = (newAnswers[index] || '') + symbol;
                                              setExplanationAnswers(newAnswers);
                                            }}
                                          >
                                            {symbol}
                                          </Button>
                                        ))}
                                      </div>

                                      {/* Input field for current step */}
                                      <Input
                                        value={explanationAnswers[index] || ''}
                                        onChange={(e) => {
                                          const newAnswers = [...explanationAnswers];
                                          newAnswers[index] = e.target.value;
                                          setExplanationAnswers(newAnswers);
                                        }}
                                        onFocus={(e) => {
                                          setActiveInputIndex(index);
                                          e.target.setAttribute('data-active-input', 'true');
                                        }}
                                        onBlur={(e) => {
                                          e.target.removeAttribute('data-active-input');
                                        }}
                                        placeholder=""
                                        className="mb-2 text-center text-lg font-mono border-2 border-blue-300 bg-white p-3 min-h-[50px]"
                                      />
                                      
                                      {/* Section 5 Absolute Value Hint */}
                                      {getAbsoluteValueHint() && (
                                        <div className="mb-3 p-2 bg-amber-50 border border-amber-200 rounded text-xs text-amber-800 text-center">
                                          {getAbsoluteValueHint()[language]}
                                        </div>
                                      )}

                                      <Button 
                                        onClick={() => {
                                          console.log(`🔍 Explanation stage - checking step ${explanationStep + 1}, index:`, index);
                                          console.log('🔍 User answer:', explanationAnswers[index]);
                                          
                                          const normalized = normalizeAnswer(explanationAnswers[index]);
                                          
                                          // Find the current step solution for this level
                                          const levelStepSolutions = problem.step_solutions?.filter(step => 
                                            step.step_en.includes(`Level ${index + 1}B Step`)
                                          ) || [];
                                          
                                          const currentStepSolution = levelStepSolutions[explanationStep];
                                          
                                          let stepCorrect = false;
                                          if (currentStepSolution) {
                                            const possibleAnswers = language === 'ar' 
                                              ? currentStepSolution.possible_answers_ar 
                                              : currentStepSolution.possible_answers;
                                            
                                            // Enhanced validation with bidirectional support
                                            stepCorrect = possibleAnswers?.some(ans => 
                                              normalizeAnswer(ans) === normalized || 
                                              areBidirectionallyEqual(normalized, normalizeAnswer(ans))
                                            ) || false;
                                          }
                                          
                                          console.log(`🔍 Step ${explanationStep + 1} correct:`, stepCorrect);
                                          
                                          if (stepCorrect) {
                                            if (explanationStep < levelSteps.length - 1) {
                                              // Store the current step answer in history before moving to next step
                                              const newHistory = [...explanationStepHistory];
                                              newHistory[explanationStep] = explanationAnswers[index];
                                              setExplanationStepHistory(newHistory);
                                              
                                              // Move to next step
                                              setExplanationStep(explanationStep + 1);
                                              const newAnswers = [...explanationAnswers];
                                              newAnswers[index] = ''; // Clear for next step
                                              setExplanationAnswers(newAnswers);
                                              setShowEncouragement(language === 'en' ? "Excellent! Continue to the next step." : "ممتاز! انتقل للخطوة التالية.");
                                            } else {
                                              // Store the final step answer in history
                                              const newHistory = [...explanationStepHistory];
                                              newHistory[explanationStep] = explanationAnswers[index];
                                              setExplanationStepHistory(newHistory);
                                              
                                              // Completed all steps for this level
                                              const newPracticeComplete = [...practiceComplete];
                                              newPracticeComplete[index] = true;
                                              setPracticeComplete(newPracticeComplete);
                                              setExplanationStep(0);
                                              // Reset step history for next level
                                              setExplanationStepHistory([]);
                                              const newAnswers = [...explanationAnswers];
                                              newAnswers[index] = '';
                                              setExplanationAnswers(newAnswers);
                                              setShowEncouragement(language === 'en' ? "Perfect! Level completed!" : "ممتاز! تم إكمال المستوى!");
                                              
                                              // Auto-move to next level or complete
                                              if (index < problem.interactive_examples.length - 1) {
                                                setTimeout(() => {
                                                  setCurrentExample(index + 1);
                                                  setShowExample(false);
                                                  setShowEncouragement('');
                                                }, 3000);
                                              } else {
                                                // All examples completed - mark as complete but DON'T set isCorrect for explanation stage
                                                setAllStepsComplete(true);
                                                // Don't set isCorrect here to prevent conflicting navigation buttons
                                                // Remove automatic timeout - let user click Continue button manually
                                                setShowEncouragement(language === 'en' ? "Perfect! All examples completed!" : "ممتاز! تم إكمال جميع الأمثلة!");
                                              }
                                            }
                                            // Only clear encouragement for incorrect answers, not for completion
                                            if (!stepCorrect) {
                                              setTimeout(() => setShowEncouragement(''), 3000);
                                            }
                                          } else {
                                            // Show error feedback
                                            const feedback = language === 'en' 
                                              ? `Not quite. Please try again.`
                                              : `ليس تماماً. يرجى المحاولة مرة أخرى.`;
                                            
                                            setShowEncouragement(feedback);
                                            setTimeout(() => setShowEncouragement(''), 6000);
                                          }
                                        }}
                                        className="w-full bg-blue-500 hover:bg-blue-600"
                                        disabled={!explanationAnswers[index]?.trim()}
                                      >
                                        {language === 'en' ? `Check Step ${explanationStep + 1}` : `تحقق من الخطوة ${explanationStep + 1}`}
                                      </Button>
                                    </div>
                                  );
                                })()}

                                {/* Success Message */}
                                {practiceComplete[index] && (
                                  <div className="bg-green-100 border border-green-300 text-green-800 p-6 rounded text-center font-semibold text-lg">
                                    🎉 {language === 'en' ? 'Perfect! Well done!' : 'ممتاز! أحسنت!'}
                                    {index < problem.interactive_examples.length - 1 && (
                                      <p className="text-base mt-2">
                                        {language === 'en' ? 'Moving to next example in 3 seconds...' : 'الانتقال للمثال التالي خلال 3 ثوان...'}
                                      </p>
                                    )}
                                  </div>
                                )}
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Solution Display - Only for read-only mode */}
                        {showExample && problem.show_full_solution && (
                          <div>
                            <div className="bg-green-50 p-8 rounded-lg mb-8 border border-green-200 max-w-5xl mx-auto">
                              <h4 className="font-bold text-2xl text-green-800 mb-6">
                                {language === 'en' ? '💡 Step-by-Step Solution:' : '💡 الحل خطوة بخطوة:'}
                              </h4>
                              <pre className="whitespace-pre-wrap text-lg text-green-700 leading-relaxed font-mono">
                                {language === 'en' ? example.solution_en : example.solution_ar}
                              </pre>
                            </div>

                            {/* FIXED: Practice Section with Step-by-Step Guidance */}
                            <div className="bg-yellow-50 p-8 rounded-lg border border-yellow-200 max-w-3xl mx-auto">
                              <h4 className="font-bold text-2xl text-yellow-800 mb-6 text-center">
                                {language === 'en' ? '✏️ Now You Try:' : '✏️ الآن جربه بنفسك:'}
                              </h4>
                              
                              <div className="text-center mb-6">
                                <div className="bg-white p-6 rounded border text-2xl font-mono text-gray-800 max-w-lg mx-auto">
                                  {language === 'en' ? example.practice_question_en : example.practice_question_ar}
                                </div>
                              </div>
                              
                              {/* RESTORED: Step-by-Step Practice with Simplified Input Management */}
                              <div className="space-y-6">
                                {/* Dynamic Multi-Step System */}
                                {(() => {
                                  // Determine how many steps this level has
                                  const levelSteps = problem.step_solutions?.filter(step => 
                                    step.step_en.includes(`Level ${index + 1}B Step`)
                                  ) || [];
                                  
                                  const currentStepIndex = explanationStep;
                                  const currentStep = levelSteps[currentStepIndex];
                                  
                                  if (!currentStep) return null;
                                  
                                  return (
                                    <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                                      <h5 className="font-semibold text-blue-800 mb-3">
                                        {language === 'ar' ? currentStep.step_ar : currentStep.step_en}
                                      </h5>
                                      
                                      {/* Show previous steps */}
                                      {explanationStep > 0 && (
                                        <div className="mb-3">
                                          <p className="text-sm text-gray-600 mb-2">
                                            {language === 'en' ? 'Your previous steps:' : 'خطواتك السابقة:'}
                                          </p>
                                          {explanationStepHistory.slice(0, explanationStep).map((stepAnswer, stepIdx) => (
                                            stepAnswer && (
                                              <div key={stepIdx} className="mb-2 p-2 bg-green-100 rounded text-center text-sm text-green-800 border border-green-300">
                                                <span className="inline-block bg-green-200 px-2 py-1 rounded-full text-xs font-semibold mr-2">
                                                  {language === 'en' ? `Step ${stepIdx + 1}` : `الخطوة ${stepIdx + 1}`}
                                                </span>
                                                <span className="font-mono">{stepAnswer}</span>
                                              </div>
                                            )
                                          ))}
                                        </div>
                                      )}
                                      
                                      {/* Symbol Shortcut Buttons */}
                                      <div className="symbol-buttons-container flex flex-wrap justify-center gap-2 md:flex-nowrap mb-3">
                                        {['<', '>', '≤', '≥', '=', '≠', '|'].map((symbol) => (
                                          <Button
                                            key={symbol}
                                            variant="outline"
                                            size="sm"
                                            onClick={() => {
                                              const newAnswers = [...explanationAnswers];
                                              newAnswers[index] = (newAnswers[index] || '') + symbol;
                                              setExplanationAnswers(newAnswers);
                                            }}
                                            className="symbol-button px-3 py-2 text-lg font-mono border-gray-300 hover:bg-gray-50 min-w-[45px] h-[45px] flex-shrink-0"
                                          >
                                            {symbol}
                                          </Button>
                                        ))}
                                      </div>
                                      
                                      <Input
                                        value={explanationAnswers[index] || ''}
                                        onChange={(e) => {
                                          const newAnswers = [...explanationAnswers];
                                          newAnswers[index] = e.target.value;
                                          setExplanationAnswers(newAnswers);
                                        }}
                                        onFocus={(e) => {
                                          setActiveInputIndex(index);
                                          e.target.setAttribute('data-active-input', 'true');
                                        }}
                                        onBlur={(e) => {
                                          e.target.removeAttribute('data-active-input');
                                        }}
                                        placeholder=""
                                        className="mb-2 text-center text-lg font-mono border-2 border-blue-300 bg-white p-3 min-h-[50px]"
                                      />
                                      
                                      {/* Section 5 Absolute Value Hint */}
                                      {getAbsoluteValueHint() && (
                                        <div className="mb-3 p-2 bg-amber-50 border border-amber-200 rounded text-xs text-amber-800 text-center">
                                          {getAbsoluteValueHint()[language]}
                                        </div>
                                      )}

                                      <Button 
                                        onClick={() => {
                                          console.log(`🔍 Explanation stage - checking step ${explanationStep + 1}, index:`, index);
                                          console.log('🔍 User answer:', explanationAnswers[index]);
                                          
                                          const normalized = normalizeAnswer(explanationAnswers[index]);
                                          
                                          // Find the current step solution for this level
                                          const levelStepSolutions = problem.step_solutions?.filter(step => 
                                            step.step_en.includes(`Level ${index + 1}B Step`)
                                          ) || [];
                                          
                                          const currentStepSolution = levelStepSolutions[explanationStep];
                                          
                                          let stepCorrect = false;
                                          if (currentStepSolution) {
                                            const possibleAnswers = language === 'ar' 
                                              ? currentStepSolution.possible_answers_ar 
                                              : currentStepSolution.possible_answers;
                                            
                                            // Enhanced validation with bidirectional support
                                            stepCorrect = possibleAnswers?.some(ans => 
                                              normalizeAnswer(ans) === normalized || 
                                              areBidirectionallyEqual(normalized, normalizeAnswer(ans))
                                            ) || false;
                                          }
                                          
                                          console.log(`🔍 Step ${explanationStep + 1} correct:`, stepCorrect);
                                          
                                          if (stepCorrect) {
                                            if (explanationStep < levelSteps.length - 1) {
                                              // Store the current step answer in history before moving to next step
                                              const newHistory = [...explanationStepHistory];
                                              newHistory[explanationStep] = explanationAnswers[index];
                                              setExplanationStepHistory(newHistory);
                                              
                                              // Move to next step
                                              setExplanationStep(explanationStep + 1);
                                              const newAnswers = [...explanationAnswers];
                                              newAnswers[index] = ''; // Clear for next step
                                              setExplanationAnswers(newAnswers);
                                              setShowEncouragement(language === 'en' ? "Excellent! Continue to the next step." : "ممتاز! انتقل للخطوة التالية.");
                                            } else {
                                              // Store the final step answer in history
                                              const newHistory = [...explanationStepHistory];
                                              newHistory[explanationStep] = explanationAnswers[index];
                                              setExplanationStepHistory(newHistory);
                                              
                                              // Completed all steps for this level
                                              const newPracticeComplete = [...practiceComplete];
                                              newPracticeComplete[index] = true;
                                              setPracticeComplete(newPracticeComplete);
                                              setExplanationStep(0);
                                              // Reset step history for next level
                                              setExplanationStepHistory([]);
                                              const newAnswers = [...explanationAnswers];
                                              newAnswers[index] = '';
                                              setExplanationAnswers(newAnswers);
                                              setShowEncouragement(language === 'en' ? "Perfect! Level completed!" : "ممتاز! تم إكمال المستوى!");
                                              
                                              // Auto-move to next level or complete
                                              if (index < problem.interactive_examples.length - 1) {
                                                setTimeout(() => {
                                                  setCurrentExample(index + 1);
                                                  setShowExample(false);
                                                  setShowEncouragement('');
                                                }, 3000);
                                              } else {
                                                // All examples completed - mark as complete but DON'T submit to backend yet
                                                setAllStepsComplete(true);
                                                setIsCorrect(true);
                                                // Remove automatic timeout - let user click Continue button manually
                                                setShowEncouragement(language === 'en' ? "Perfect! All examples completed!" : "ممتاز! تم إكمال جميع الأمثلة!");
                                              }
                                            }
                                            // Only clear encouragement for incorrect answers, not for completion
                                            if (!stepCorrect) {
                                              setTimeout(() => setShowEncouragement(''), 3000);
                                            }
                                          } else {
                                            // Find the hint index for this specific level and step
                                            const levelStepSolutions = problem.step_solutions?.filter(step => 
                                              step.step_en.includes(`Level ${index + 1}B Step`)
                                            ) || [];
                                            const currentStepSolution = levelStepSolutions[explanationStep];
                                            
                                            // Use improved hints - find the specific hint for this step
                                            let feedback;
                                            if (index === 1 && explanationStep === 1 && normalized.includes('12') && normalized.includes('≤') && normalized.includes('m')) {
                                              // Special case for Level 2B Step 2 when student enters "12 ≤ m"
                                              feedback = language === 'en' 
                                                ? "Good! Now write this in standard form: m ≥ 12"
                                                : "جيد! الآن اكتب هذا بالشكل القياسي: م ≥ ١٢";
                                            } else {
                                              // Use the general hint from backend or default
                                              const allSteps = problem.step_solutions || [];
                                              const globalStepIndex = allSteps.findIndex(step => 
                                                step.step_en === currentStepSolution?.step_en
                                              );
                                              const correctHints = language === 'en' ? problem.hints_en : problem.hints_ar;
                                              const stepHint = correctHints?.[globalStepIndex] || '';
                                              
                                              feedback = stepHint || (language === 'en' 
                                                ? `Not quite. Please try again.`
                                                : `ليس تماماً. يرجى المحاولة مرة أخرى.`);
                                            }
                                            
                                            setShowEncouragement(feedback);
                                            setTimeout(() => setShowEncouragement(''), 6000);
                                          }
                                        }}
                                        className="w-full bg-blue-500 hover:bg-blue-600"
                                        disabled={!explanationAnswers[index]?.trim()}
                                      >
                                        {language === 'en' ? `Check Step ${explanationStep + 1}` : `تحقق من الخطوة ${explanationStep + 1}`}
                                      </Button>
                                    </div>
                                  );
                                })()}

                                {/* Success Message */}
                                {practiceComplete[index] && (
                                  <div className="bg-green-100 border border-green-300 text-green-800 p-6 rounded text-center font-semibold text-lg">
                                    🎉 {language === 'en' ? 'Perfect! Well done!' : 'ممتاز! أحسنت!'}
                                    {index < problem.interactive_examples.length - 1 && (
                                      <p className="text-base mt-2">
                                        {language === 'en' ? 'Moving to next example in 3 seconds...' : 'الانتقال للمثال التالي خلال 3 ثوان...'}
                                      </p>
                                    )}
                                  </div>
                                )}
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    )
                  ))}
                  
                  {/* Global Voice Input Component */}
                  {showVoiceInput && (
                    <div className="mt-10 p-6 bg-blue-50 rounded-lg border border-blue-200 max-w-lg mx-auto">
                      <VoiceInput
                        onResult={handleVoiceResult}
                        onError={handleVoiceError}
                        language={language}
                        isActive={showVoiceInput}
                      />
                    </div>
                  )}

                  {/* Global Math Keyboard Component */}
                  {showMathKeyboard && (
                    <div className="mt-10 p-6 bg-purple-50 rounded-lg border border-purple-200 max-w-4xl mx-auto">
                      <MathKeyboard
                        onSymbolSelect={(symbol) => {
                          setPracticeAnswer(prev => prev + symbol);
                        }}
                        onNumberSelect={(number) => {
                          setPracticeAnswer(prev => prev + number);
                        }}
                        onOperatorSelect={(operator) => {
                          setPracticeAnswer(prev => prev + ` ${operator} `);
                        }}
                        onAction={(action) => {
                          if (action === 'clear') {
                            setPracticeAnswer('');
                          } else if (action === 'backspace') {
                            setPracticeAnswer(prev => prev.slice(0, -1));
                          } else if (action === 'voice') {
                            setShowVoiceInput(!showVoiceInput);
                            setShowMathKeyboard(false);
                          }
                        }}
                      />
                    </div>
                  )}
                  
                  {/* Completion Message */}
                  {practiceComplete.length === problem.interactive_examples.length && 
                   practiceComplete.every(completed => completed) && (
                    <div className="mt-12 text-center p-10 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-200 max-w-4xl mx-auto">
                      <div className="text-green-600 mb-6">
                        <CheckCircle className="w-24 h-24 mx-auto mb-6" />
                        <h3 className="text-4xl font-bold mb-4">
                          {language === 'en' ? '🎊 Explanation Complete!' : '🎊 اكتمل الشرح!'}
                        </h3>
                        <p className="text-2xl">
                          {language === 'en' 
                            ? 'Outstanding work! You have mastered all the examples. Ready for the practice stage!' 
                            : 'عمل رائع! لقد أتقنت جميع الأمثلة. جاهز لمرحلة التطبيق!'}
                        </p>
                      </div>
                      
                      <Button 
                        onClick={async () => {
                          // Prevent multiple clicks
                          if (navigationInProgress) return;
                          
                          // Submit explanation completion to backend first
                          await submitToBackend();
                          // Then navigate to next problem with forced navigation
                          handleNavigationClick();
                        }}
                        disabled={navigationInProgress}
                        className="mt-8 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white px-16 py-6 text-2xl font-semibold disabled:opacity-50"
                      >
                        <Trophy className="w-8 h-8 mr-4" />
                        {language === 'en' ? 'Continue to Practice Stage →' : 'انتقل لمرحلة التطبيق ←'}
                      </Button>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Interactive Practice for Preparation */}
            {problem.practice_problems && (
              <Card className="mb-6">
                <CardContent className="p-6">
                  <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500 mb-4">
                    <h4 className="font-semibold mb-2 text-blue-800">
                      {text[language].explanation}
                    </h4>
                    <pre className="whitespace-pre-wrap text-sm text-blue-700">
                      {language === 'en' ? problem.explanation_en : problem.explanation_ar}
                    </pre>
                  </div>
                  
                  <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                    <h5 className="font-medium mb-2 text-yellow-800">
                      {language === 'en' ? 'Try It Yourself:' : 'جربه بنفسك:'}
                    </h5>
                    <div className="text-lg font-mono text-center mb-3">
                      {language === 'en' ? problem.practice_problems[0].question_en : problem.practice_problems[0].question_ar}
                    </div>
                    
                    <Input
                      value={practiceAnswer}
                      onChange={(e) => setPracticeAnswer(e.target.value)}
                      placeholder={language === 'en' ? 'Enter your answer...' : 'أدخل إجابتك...'}
                      className="mb-3"
                    />
                    
                    <div className="flex gap-2">
                      <Button 
                        onClick={() => {
                          const correct = normalizeAnswer(practiceAnswer) === normalizeAnswer(problem.practice_problems[0].answer);
                          if (correct) {
                            setPracticeComplete([true]);
                          } else {
                            setShowEncouragement(text[language].encouragement[Math.floor(Math.random() * text[language].encouragement.length)]);
                            setTimeout(() => setShowEncouragement(''), 3000);
                          }
                        }}
                        className="flex-1"
                        disabled={!practiceAnswer.trim()}
                      >
                        {language === 'en' ? 'Check Answer' : 'تحقق من الإجابة'}
                      </Button>
                      
                      <Button 
                        onClick={() => {
                          alert(language === 'en' ? problem.practice_problems[0].hint_en : problem.practice_problems[0].hint_ar);
                        }}
                        variant="outline"
                      >
                        {language === 'en' ? 'Hint' : 'إرشاد'}
                      </Button>
                    </div>
                    
                    {practiceComplete[0] && (
                      <div className="mt-4">
                        <div className="p-2 bg-green-100 text-green-800 rounded text-center mb-3">
                          ✓ {language === 'en' ? 'Correct! Well done!' : 'صحيح! أحسنت!'}
                        </div>
                        <Button 
                          onClick={async () => {
                            // Mark preparation stage as completed
                            await submitToBackend();
                            handleNavigationClick();
                          }}
                          className="w-full bg-gradient-to-r from-green-500 to-emerald-600"
                        >
                          {language === 'en' ? 'Continue to Next Problem →' : 'تابع للمسألة التالية ←'}
                        </Button>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}
              </CardContent>
                
                {/* COPIED FROM PRACTICE STAGE: Error Message Display Component */}
                {showEncouragement && (
                  <div className={`mt-4 mx-6 mb-4 p-3 rounded-lg ${
                    showEncouragement.includes('✅') || showEncouragement.includes('🎉') || showEncouragement.includes('Excellent') || showEncouragement.includes('Perfect') ? 'bg-green-50 border border-green-200' :
                    showEncouragement.includes('❌') || showEncouragement.includes('Not quite') || showEncouragement.includes('Try again') ? 'bg-red-50 border border-red-200' :
                    'bg-yellow-50 border border-yellow-200'
                  }`}>
                    <p className={`text-center font-medium ${
                      showEncouragement.includes('✅') || showEncouragement.includes('🎉') || showEncouragement.includes('Excellent') || showEncouragement.includes('Perfect') ? 'text-green-800' :
                      showEncouragement.includes('❌') || showEncouragement.includes('Not quite') || showEncouragement.includes('Try again') ? 'text-red-800' :
                      'text-yellow-800'
                    }`}>
                      {showEncouragement}
                    </p>
                  </div>
                )}
              </Card>

            {/* REDESIGNED DUAL INTERACTION MODEL */}
            {problem.type !== 'explanation' && (
              <Card>
                <CardContent className="p-6">
                  {(() => {
                    const stageType = getStageType(problem.type, problem.id);
                    
                    switch (stageType) {
                      case 'preparation':
                        return (
                          // 1. PREPARATION STAGE: Final answer only
                          <div>
                            <h4 className="font-semibold mb-4 text-blue-800 flex items-center">
                              <Target className="w-5 h-5 mr-2" />
                              {language === 'en' ? 'Final Answer:' : 'الإجابة النهائية:'}
                            </h4>
                            
                            {/* Attempt Counter */}
                            {attempts > 0 && attempts < 3 && (
                              <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                                <p className="text-blue-800 text-sm">
                                  {language === 'en' 
                                    ? `Attempt ${attempts} of 3. Auto-hints provided to help you learn.`
                                    : `المحاولة ${attempts} من 3. تم توفير تلميحات تلقائية لمساعدتك على التعلم.`}
                                </p>
                              </div>
                            )}
                            
                            {/* Final Answer Input - FIXED: No gap above */}
                            <div className="answer-input-section">
                              <Input
                                value={userAnswer}
                                onChange={(e) => setUserAnswer(e.target.value)}
                                placeholder={language === 'en' ? 'Enter your final answer (e.g., x < 4)...' : 'أدخل إجابتك النهائية (مثال: س < 4)...'}
                                className="mb-2 text-lg h-12"
                              />
                              
                              {/* Section 5 Absolute Value Hint */}
                              {getAbsoluteValueHint() && (
                                <div className="mb-4 p-2 bg-amber-50 border border-amber-200 rounded text-sm text-amber-800 text-center">
                                  {getAbsoluteValueHint()[language]}
                                </div>
                              )}
                            </div>
                          </div>
                        );
                        
                      case 'practice':
                        return (
                          // 3. PRACTICE STAGE: Step-by-step guided (no hints)
                          <div>
                            <h4 className="font-semibold mb-4 text-green-800 flex items-center">
                              <BookOpen className="w-5 h-5 mr-2" />
                              {language === 'en' ? `Step ${currentStep + 1}: Guided Practice` : `الخطوة ${currentStep + 1}: تدريب موجه`}
                            </h4>
                            
                            {/* Step Progress Indicator - FIXED: Dynamic based on required steps */}
                            <div className="mb-3 stage-progress">
                              <div className="flex items-center justify-center space-x-2 mb-2">
                                {(() => {
                                  const requiredSteps = getRequiredSteps(problem.type, problem.id, problem);
                                  return Array.from({ length: requiredSteps }, (_, step) => (
                                    <div
                                      key={step}
                                      className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
                                        step < currentStep
                                          ? 'bg-green-500 text-white'
                                          : step === currentStep
                                          ? 'bg-blue-500 text-white'
                                          : 'bg-gray-200 text-gray-500'
                                      }`}
                                    >
                                      {step + 1}
                                    </div>
                                  ))
                                })()}
                              </div>
                              <p className="text-center text-sm text-gray-600">
                                {language === 'en' 
                                  ? `Step ${currentStep + 1} of ${getRequiredSteps(problem.type, problem.id, problem)}`
                                  : `الخطوة ${currentStep + 1} من ${getRequiredSteps(problem.type, problem.id, problem)}`}
                              </p>
                            </div>

                            {/* Show completed steps above current step */}
                            {currentStep > 0 && (
                              <div className="mb-4">
                                <h5 className="font-medium text-gray-700 mb-2">
                                  {language === 'en' ? 'Your previous steps:' : 'خطواتك السابقة:'}
                                </h5>
                                {stepAnswers.slice(0, currentStep).map((answer, index) => (
                                  answer && (
                                    <div key={index} className="mb-2 p-2 bg-blue-100 rounded text-sm text-blue-800">
                                      {language === 'en' ? `Step ${index + 1}: ` : `الخطوة ${index + 1}: `}{answer}
                                    </div>
                                  )
                                ))}
                              </div>
                            )}

                            {/* Explicit Step Instruction */}
                            <div className="mb-4 p-4 bg-green-50 rounded-lg border border-green-200">
                              <h5 className="font-medium text-green-800 mb-2">
                                {problem.step_solutions?.[currentStep] 
                                  ? (language === 'en' ? problem.step_solutions[currentStep].step_en : problem.step_solutions[currentStep].step_ar)
                                  : (language === 'en' ? `Complete this step` : `أكمل هذه الخطوة`)}
                              </h5>
                            </div>
                            
                            {/* Step Input */}
                            <Input
                              value={stepAnswers[currentStep] || ''}
                              onChange={(e) => {
                                const newStepAnswers = [...stepAnswers];
                                newStepAnswers[currentStep] = e.target.value;
                                setStepAnswers(newStepAnswers);
                              }}
                              placeholder={language === 'en' ? `Enter your answer for step ${currentStep + 1}...` : `أدخل إجابتك للخطوة ${currentStep + 1}...`}
                              className="mb-2 text-lg h-12"
                            />
                            
                            {/* Section 5 Absolute Value Hint */}
                            {getAbsoluteValueHint() && (
                              <div className="mb-4 p-2 bg-amber-50 border border-amber-200 rounded text-sm text-amber-800 text-center">
                                {getAbsoluteValueHint()[language]}
                              </div>
                            )}
                          </div>
                        );
                        
                      case 'practice_word':
                        return (
                          // 5. PRACTICE WORD PROBLEMS: 3-step process with hints visible from start
                          <div>
                            <h4 className="font-semibold mb-4 text-green-800 flex items-center">
                              <BookOpen className="w-5 h-5 mr-2" />
                              {language === 'en' ? `Step ${currentStep + 1}: Word Problem Solving` : `الخطوة ${currentStep + 1}: حل المسائل الكلامية`}
                            </h4>
                            
                            {/* HINTS VISIBLE FROM START - Key difference from regular practice */}
                            <div className="mb-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
                              <div className="flex items-start gap-2">
                                <Lightbulb className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                                <div>
                                  <h5 className="font-medium text-blue-800 mb-2">
                                    {language === 'en' ? 'Hint:' : 'تلميح:'}
                                  </h5>
                                  <p className="text-blue-700 text-sm">
                                    {(() => {
                                      const backendHints = language === 'en' ? problem.hints_en : problem.hints_ar;
                                      const currentStepHint = backendHints?.[currentStep] || 
                                        (language === 'en' ? 'Think step by step.' : 'فكر خطوة بخطوة.');
                                      return currentStepHint;
                                    })()}
                                  </p>
                                </div>
                              </div>
                            </div>
                            
                            {/* Step Progress Indicator */}
                            <div className="mb-3 stage-progress">
                              <div className="flex items-center justify-center space-x-2 mb-2">
                                {(() => {
                                  const requiredSteps = getRequiredSteps(problem.type, problem.id, problem);
                                  return Array.from({ length: requiredSteps }, (_, step) => (
                                    <div
                                      key={step}
                                      className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
                                        step < currentStep
                                          ? 'bg-green-500 text-white'
                                          : step === currentStep
                                          ? 'bg-blue-500 text-white'
                                          : 'bg-gray-200 text-gray-500'
                                      }`}
                                    >
                                      {step + 1}
                                    </div>
                                  ))
                                })()}
                              </div>
                              <p className="text-center text-sm text-gray-600">
                                {language === 'en' 
                                  ? `Step ${currentStep + 1} of ${getRequiredSteps(problem.type, problem.id, problem)}`
                                  : `الخطوة ${currentStep + 1} من ${getRequiredSteps(problem.type, problem.id, problem)}`}
                              </p>
                            </div>

                            {/* Show completed steps above current step */}
                            {currentStep > 0 && (
                              <div className="mb-4 previous-steps-container bg-gray-50 border border-gray-200 rounded-lg p-4">
                                <h5 className="font-medium text-gray-700 mb-3 flex items-center">
                                  <CheckCircle className="w-4 h-4 mr-2 text-green-600" />
                                  {language === 'en' ? 'Your previous steps:' : 'خطواتك السابقة:'}
                                </h5>
                                {stepAnswers.slice(0, currentStep).map((answer, index) => (
                                  answer && (
                                    <div key={index} className="step-display bg-white border border-green-200 rounded-md p-3 mb-2 shadow-sm">
                                      <div className="flex items-center gap-2">
                                        <span className="step-label font-semibold text-green-700 bg-green-100 px-2 py-1 rounded text-sm">
                                          {language === 'en' ? `Step ${index + 1}:` : `الخطوة ${index + 1}:`}
                                        </span>
                                        <span className="step-value font-mono text-green-800 bg-green-50 px-2 py-1 rounded">
                                          {answer}
                                        </span>
                                      </div>
                                    </div>
                                  )
                                ))}
                              </div>
                            )}

                            {/* Explicit Step Instruction */}
                            <div className="mb-4 p-4 bg-green-50 rounded-lg border border-green-200">
                              <h5 className="font-medium text-green-800 mb-2">
                                {problem.step_solutions?.[currentStep] 
                                  ? (language === 'en' ? problem.step_solutions[currentStep].step_en : problem.step_solutions[currentStep].step_ar)
                                  : (language === 'en' ? `Complete this step` : `أكمل هذه الخطوة`)}
                              </h5>
                            </div>
                            
                            {/* Step Input */}
                            <Input
                              value={stepAnswers[currentStep] || ''}
                              onChange={(e) => {
                                const newStepAnswers = [...stepAnswers];
                                newStepAnswers[currentStep] = e.target.value;
                                setStepAnswers(newStepAnswers);
                              }}
                              placeholder={language === 'en' ? `Enter your answer for step ${currentStep + 1}...` : `أدخل إجابتك للخطوة ${currentStep + 1}...`}
                              className="mb-2 text-lg h-12"
                            />
                            
                            {/* Section 5 Absolute Value Hint */}
                            {getAbsoluteValueHint() && (
                              <div className="mb-4 p-2 bg-amber-50 border border-amber-200 rounded text-sm text-amber-800 text-center">
                                {getAbsoluteValueHint()[language]}
                              </div>
                            )}
                          </div>
                        );
                        
                      case 'assessment':
                        return (
                          // 4. ASSESSMENT STAGE: Final answer with score penalties - FIXED: Layout classes
                          <div className="assessment-layout">
                            <h4 className="font-semibold mb-4 text-purple-800 flex items-center">
                              <Trophy className="w-5 h-5 mr-2" />
                              {language === 'en' ? 'Assessment - Final Answer:' : 'التقييم - الإجابة النهائية:'}
                            </h4>
                            
                            {/* Score Display */}
                            <div className="mb-4 p-3 bg-purple-50 border border-purple-200 rounded-lg">
                              <p className="text-purple-800 font-semibold">
                                {language === 'en' 
                                  ? `Current Score: ${currentScore}%${hintsUsed > 0 ? ` (${hintsUsed} hint${hintsUsed > 1 ? 's' : ''} used)` : ''}`
                                  : `النتيجة الحالية: ${currentScore}%${hintsUsed > 0 ? ` (${hintsUsed} تلميح مستخدم)` : ''}`}
                              </p>
                              {attempts > 0 && (
                                <p className="text-sm text-purple-600 mt-1">
                                  {language === 'en' 
                                    ? `Attempt ${attempts} of 3. Each hint reduces your score by 15%.`
                                    : `المحاولة ${attempts} من 3. كل تلميح يقلل النتيجة بـ 15%.`}
                                </p>
                              )}
                            </div>
                            
                            {/* Final Answer Input - FIXED: No gap above */}
                            <div className="answer-input-section">
                              <Input
                                value={userAnswer}
                                onChange={(e) => setUserAnswer(e.target.value)}
                                placeholder={language === 'en' ? 'Enter your final answer (e.g., x < 4)...' : 'أدخل إجابتك النهائية (مثال: س < 4)...'}
                                className="mb-2 text-lg h-12"
                              />
                              
                              {/* Section 5 Absolute Value Hint */}
                              {getAbsoluteValueHint() && (
                                <div className="mb-4 p-2 bg-amber-50 border border-amber-200 rounded text-sm text-amber-800 text-center">
                                  {getAbsoluteValueHint()[language]}
                                </div>
                              )}
                            </div>
                          </div>
                        );
                        
                      default:
                        return null;
                    }
                  })()}
                  
                  {/* Common Buttons Row */}
                  <div className="flex gap-2 mb-4">
                    <Button 
                      onClick={handleSubmit}
                      className="flex-1 h-12 bg-gradient-to-r from-emerald-500 to-teal-600"
                      disabled={isChecking || (() => {
                        const stageType = getStageType(problem.type, problem.id);
                        if (stageType === 'practice' || stageType === 'practice_word') {
                          return !stepAnswers[currentStep]?.trim();
                        } else {
                          return !userAnswer?.trim();
                        }
                      })()}
                    >
                      {isChecking ? (
                        <div className="flex items-center">
                          <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                          {text[language].completion.checking}
                        </div>
                      ) : (
                        (() => {
                          // FIXED: Dynamic submit button text based on stage and step
                          const stageType = getStageType(problem.type, problem.id);
                          
                          if (stageType === 'practice' || stageType === 'practice_word') {
                            const requiredSteps = getRequiredSteps(problem.type, problem.id, problem);
                            if (requiredSteps > 1) {
                              // Multi-step problems - show current step
                              return language === 'en' 
                                ? `Submit Step ${currentStep + 1} Answer`
                                : `أرسل إجابة الخطوة ${currentStep + 1}`;
                            } else {
                              // Single step practice problems
                              return language === 'en' ? 'Submit Answer' : 'إرسال الإجابة';
                            }
                          } else if (stageType === 'explanation') {
                            return language === 'en' ? 'Submit Step' : 'إرسال الخطوة';
                          } else {
                            // Assessment, exam prep, preparation
                            return language === 'en' ? 'Submit Final Answer' : 'إرسال الإجابة النهائية';
                          }
                        })()
                      )}
                    </Button>
                    
                    {/* Voice Input Button */}
                    <Button 
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        setShowVoiceInput(!showVoiceInput);
                        setShowMathKeyboard(false);
                      }}
                      className="px-3 border-blue-300 text-blue-600 hover:bg-blue-50"
                      title={language === 'ar' ? 'إدخال صوتي' : 'Voice Input'}
                    >
                      <Mic className="w-4 h-4" />
                    </Button>
                    
                    {/* Math Keyboard Button */}
                    <Button 
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        setShowMathKeyboard(!showMathKeyboard);
                        setShowVoiceInput(false);
                      }}
                      className="px-3 border-purple-300 text-purple-600 hover:bg-purple-50"
                      title={language === 'ar' ? 'لوحة مفاتيح رياضية' : 'Math Keyboard'}
                    >
                      <Keyboard className="w-4 h-4" />
                    </Button>
                  </div>

                  {/* Voice Input Component */}
                  {showVoiceInput && (
                    <div className="mt-4">
                      <VoiceInput
                        onResult={(result) => {
                          const stageType = getStageType(problem.type, problem.id);
                          if (stageType === 'practice' || stageType === 'practice_word') {
                            const newStepAnswers = [...stepAnswers];
                            newStepAnswers[currentStep] = result;
                            setStepAnswers(newStepAnswers);
                          } else {
                            setUserAnswer(result);
                          }
                          setShowVoiceInput(false);
                        }}
                        onError={handleVoiceError}
                        language={language}
                        isActive={showVoiceInput}
                      />
                    </div>
                  )}

                  {/* Math Keyboard Component */}
                  {showMathKeyboard && (
                    <div className="mt-4">
                      <MathKeyboard
                        onSymbolSelect={(symbol) => {
                          const stageType = getStageType(problem.type, problem.id);
                          if (stageType === 'practice' || stageType === 'practice_word') {
                            const newStepAnswers = [...stepAnswers];
                            newStepAnswers[currentStep] = (newStepAnswers[currentStep] || '') + symbol;
                            setStepAnswers(newStepAnswers);
                          } else {
                            setUserAnswer(prev => prev + symbol);
                          }
                        }}
                        onNumberSelect={(number) => {
                          const stageType = getStageType(problem.type, problem.id);
                          if (stageType === 'practice' || stageType === 'practice_word') {
                            const newStepAnswers = [...stepAnswers];
                            newStepAnswers[currentStep] = (newStepAnswers[currentStep] || '') + number;
                            setStepAnswers(newStepAnswers);
                          } else {
                            setUserAnswer(prev => prev + number);
                          }
                        }}
                        onOperatorSelect={(operator) => {
                          const stageType = getStageType(problem.type, problem.id);
                          if (stageType === 'practice' || stageType === 'practice_word') {
                            const newStepAnswers = [...stepAnswers];
                            newStepAnswers[currentStep] = (newStepAnswers[currentStep] || '') + ` ${operator} `;
                            setStepAnswers(newStepAnswers);
                          } else {
                            setUserAnswer(prev => prev + ` ${operator} `);
                          }
                        }}
                        onAction={(action) => {
                          const stageType = getStageType(problem.type, problem.id);
                          if (action === 'clear') {
                            if (stageType === 'practice' || stageType === 'practice_word') {
                              const newStepAnswers = [...stepAnswers];
                              newStepAnswers[currentStep] = '';
                              setStepAnswers(newStepAnswers);
                            } else {
                              setUserAnswer('');
                            }
                          } else if (action === 'backspace') {
                            if (stageType === 'practice' || stageType === 'practice_word') {
                              const newStepAnswers = [...stepAnswers];
                              newStepAnswers[currentStep] = (newStepAnswers[currentStep] || '').slice(0, -1);
                              setStepAnswers(newStepAnswers);
                            } else {
                              setUserAnswer(prev => prev.slice(0, -1));
                            }
                          } else if (action === 'voice') {
                            setShowVoiceInput(!showVoiceInput);
                            setShowMathKeyboard(false);
                          }
                        }}
                      />
                    </div>
                  )}

                  {/* Enhanced Encouragement Message */}
                  {showEncouragement && (
                    <div className={`mt-4 p-3 rounded-lg ${
                      showEncouragement.includes('✅') || showEncouragement.includes('🎉') || showEncouragement.includes('Excellent') || showEncouragement.includes('Perfect') ? 'bg-green-50 border border-green-200' :
                      showEncouragement.includes('❌') || showEncouragement.includes('Not quite') || showEncouragement.includes('Try again') ? 'bg-red-50 border border-red-200' :
                      'bg-yellow-50 border border-yellow-200'
                    }`}>
                      <p className={`text-center font-medium ${
                        showEncouragement.includes('✅') || showEncouragement.includes('🎉') || showEncouragement.includes('Excellent') || showEncouragement.includes('Perfect') ? 'text-green-800' :
                        showEncouragement.includes('❌') || showEncouragement.includes('Not quite') || showEncouragement.includes('Try again') ? 'text-red-800' :
                        'text-yellow-800'
                      }`}>
                        {showEncouragement}
                      </p>
                    </div>
                  )}

                  {/* MANDATORY REDIRECTION BUTTON */}
                  {showRedirectionButton && (
                    <div className="mt-4">
                      <Button 
                        onClick={() => {
                          resetProblemState();
                          redirectToExplanation();
                        }}
                        className="w-full h-12 bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700"
                      >
                        <BookOpen className="w-4 h-4 mr-2" />
                        {problem.id === 'examprep1' 
                          ? (language === 'en' ? '📚 Go Back to the Explanation Stage' : '📚 ارجع إلى مرحلة الشرح')
                          : (language === 'en' ? '📚 Go to Explanation Stage' : '📚 انتقل لمرحلة الشرح')}
                      </Button>
                    </div>
                  )}

                  {/* Action Buttons */}
                  <div className="mt-4 flex gap-2">
                    {/* Continue to Next Stage - FIXED: Better completion detection */}
                    {(isCorrect || allStepsComplete) && 
                     !(problem.stage_type === 'explanation' && 
                       practiceComplete.length === problem.interactive_examples.length && 
                       practiceComplete.every(completed => completed)) && (
                      <Button 
                        onClick={() => {
                          console.log('🔍 Continue button clicked, navigating to next stage with forced navigation');
                          console.log(`🔍 Current problem: ${problemId}, isCorrect: ${isCorrect}, allStepsComplete: ${allStepsComplete}`);
                          handleNavigationClick();
                        }}
                        className="flex-1 h-12 bg-gradient-to-r from-green-500 to-emerald-600"
                      >
                        <Trophy className="w-4 h-4 mr-2" />
                        {(() => {
                          const stageType = getStageType(problem.type, problem.id);
                          // FIXED: Better button text for practice word problems
                          if (stageType === 'preparation') {
                            return language === 'en' ? 'Continue to Explanation Stage →' : 'انتقل لمرحلة الشرح ←';
                          } else if (stageType === 'practice' || stageType === 'practice_word') {
                            return language === 'en' ? 'Continue to Assessment →' : 'انتقل للتقييم ←';
                          } else if (problem.id === 'examprep1') {
                            return language === 'en' ? 'Start Section 2: Multiplication/Division →' : 'ابدأ القسم ٢: الضرب/القسمة ←';
                          } else if (problem.id?.includes('examprep')) {
                            const currentSection = getCurrentSection();
                            const nextSection = currentSection + 1;
                            return language === 'en' ? `Start Section ${nextSection} →` : `ابدأ القسم ${nextSection} ←`;
                          } else {
                            return language === 'en' ? 'Continue to Next Stage →' : 'انتقل للمرحلة التالية ←';
                          }
                        })()}
                      </Button>
                    )}
                    
                    {/* Try Again - Only for preparation/assessment stages under 3 attempts */}
                    {isSubmitted && !isCorrect && !allStepsComplete && attempts < 3 && ['preparation', 'assessment'].includes(getStageType(problem.type, problem.id)) && (
                      <Button 
                        onClick={() => {
                          setIsSubmitted(false);
                          setShowEncouragement('');
                          setUserAnswer('');
                        }}
                        className="flex-1 h-12"
                        variant="outline"
                      >
                        <RotateCcw className="w-4 h-4 mr-2" />
                        {text[language].tryAgain}
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}

          {/* Hints section completely removed as per requirements */}
        </div>
      </div>

      {/* Rules Modal */}
      <RulesModal 
        isOpen={showRulesModal} 
        onClose={() => setShowRulesModal(false)} 
      />
    </div>
  );
};

export default ProblemView;