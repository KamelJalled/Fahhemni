import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth, useLanguage } from '../App';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Globe, ArrowLeft, Lightbulb, CheckCircle, XCircle, RotateCcw, Trophy, Keyboard, Mic, BookOpen, Target } from 'lucide-react';
import { useToast } from '../hooks/use-toast';
import VoiceInput from './VoiceInput';
import MathKeyboard from './MathKeyboard';

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

  // Helper function for basic normalization without recursion
  const basicNormalizeAnswer = (answer) => {
    if (!answer) return '';
    
    // Convert Arabic numerals to Western and س to x
    const arabicToWestern = {'٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'};
    let normalized = answer.toLowerCase()
      .replace(/س/g, 'x')
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

  // UPDATED: Redesigned stage structure for proper Socratic tutoring
  const getStageType = (problemType, problemId) => {
    // PREPARATION STAGE: Final answer only with auto-hints
    if (problemType === 'preparation' || problemId?.includes('prep')) {
      return 'preparation';
    }
    
    // EXPLANATION STAGE: Teaching + step-by-step practice
    if (problemType === 'explanation') {
      return 'explanation';
    }
    
    // PRACTICE STAGES: Step-by-step guided (no hints needed)
    if (problemType === 'practice' || problemId?.includes('practice')) {
      return 'practice';
    }
    
    // ASSESSMENT & EXAM PREP: Final answer with score penalties
    if (problemType === 'assessment' || problemType === 'examprep' ||
        problemId?.includes('assess') || problemId?.includes('exam')) {
      return 'assessment';
    }
    
    return 'preparation'; // Default
  };

  // FIXED: Enhanced answer normalization with proper validation (NO RECURSION)
  const normalizeAnswer = (answer) => {
    if (!answer) return '';
    
    let normalized = basicNormalizeAnswer(answer);
    
    // ENHANCEMENT: For preparation stage, accept both "x = 7" and "7" formats
    if (problem && (problem.type === 'preparation' || problem.id?.includes('prep'))) {
      // If input is just a number and expected answer has "x =", add "x ="
      if (/^-?\d+(\.\d+)?$/.test(normalized)) {
        // Use basicNormalizeAnswer to avoid recursion
        const expectedNormalized = basicNormalizeAnswer(problem.answer || '');
        if (expectedNormalized.includes('x=') && !normalized.includes('x')) {
          normalized = 'x=' + normalized;
        }
      }
    }
    
    console.log(`🔍 Answer normalization: "${answer}" → "${normalized}"`);
    return normalized;
  };

  useEffect(() => {
    if (!user || !problemId) {
      navigate('/dashboard');
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

      // Fetch problem details
      const problemResponse = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/problems/${problemId}`
      );
      
      if (problemResponse.ok) {
        const problemData = await problemResponse.json();
        setProblem(problemData);
      }

      // Fetch user progress
      const progressResponse = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/students/${user.username}/progress`
      );
      
      if (progressResponse.ok) {
        const progressData = await progressResponse.json();
        setUserProgress(progressData.progress);
        setAttempts(progressData.progress.section1[problemId]?.attempts || 0);
      }

    } catch (error) {
      console.error('Error fetching data:', error);
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
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
      
      // Enhanced step validation - prevent skipping steps with final answers
      const possibleAnswers = language === 'en' ? 
        currentStepSolution.possible_answers : 
        currentStepSolution.possible_answers_ar;
      
      // Check if user entered a final answer instead of step work
      const userEnteredFinalAnswer = normalizedAnswer.includes('<') || normalizedAnswer.includes('>') || 
                                   normalizedAnswer.includes('≤') || normalizedAnswer.includes('≥');
      const stepRequiresWork = currentStepSolution.step_type !== 'final_answer';
      
      if (userEnteredFinalAnswer && stepRequiresWork && stepIndex < problem.step_solutions.length - 1) {
        // User entered final answer in intermediate step - reject it
        const stepHint = language === 'en' 
          ? `This step requires showing your work step by step. Don't skip to the final answer. Show: ${currentStepSolution.hint_en || 'your work for this step'}`
          : `هذه الخطوة تتطلب إظهار عملك خطوة بخطوة. لا تقفز إلى الإجابة النهائية. أظهر: ${currentStepSolution.hint_ar || 'عملك لهذه الخطوة'}`;
        
        setShowEncouragement(stepHint);
        setTimeout(() => setShowEncouragement(''), 7000);
        return;
      }
      
      const isStepCorrect = possibleAnswers.some(possibleAnswer => 
        normalizeAnswer(possibleAnswer) === normalizedAnswer
      );
      
      if (isStepCorrect) {
        // Step is correct
        const newStepResults = [...stepResults];
        newStepResults[stepIndex] = true;
        setStepResults(newStepResults);
        
        if (stepIndex < problem.step_solutions.length - 1) {
          // Move to next step
          setCurrentStep(stepIndex + 1);
          setShowEncouragement(`✅ ${language === 'en' ? 'Great! Now continue with the next step.' : 'رائع! الآن تابع مع الخطوة التالية.'}`);
          setTimeout(() => setShowEncouragement(''), 2000);
        } else {
          // All steps complete - now require final answer if needed
          if (problem.final_answer_required) {
            setAllStepsComplete(true);
            setShowEncouragement(`✅ ${language === 'en' ? 'Excellent! Now enter your final answer below.' : 'ممتاز! الآن أدخل إجابتك النهائية أدناه.'}`);
            setTimeout(() => setShowEncouragement(''), 3000);
          } else {
            // Complete the problem and submit to backend
            setAllStepsComplete(true);
            setIsCorrect(true);
            await submitToBackend();
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
        // First wrong attempt - auto-show Hint 1
        let errorMessage = language === 'en' ? 'Try again.' : 'حاول مرة أخرى.';
        
        if (problem.hints_en?.length > 0 || problem.hints_ar?.length > 0) {
          const hint1 = language === 'en' ? problem.hints_en[0] : problem.hints_ar[0];
          errorMessage += ` 💡 ${hint1}`;
          setHintsUsed(1);
        }
        
        setShowEncouragement(errorMessage);
        setTimeout(() => setShowEncouragement(''), 8000);
        
      } else if (currentAttempts === 2) {
        // Second wrong attempt - auto-show Hint 2
        let errorMessage = language === 'en' ? 'Try again.' : 'حاول مرة أخرى.';
        
        if (problem.hints_en?.length > 1 || problem.hints_ar?.length > 1) {
          const hint2 = language === 'en' ? problem.hints_en[1] : problem.hints_ar[1];
          errorMessage += ` 💡 ${hint2}`;
          setHintsUsed(2);
        }
        
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
    
    let isStepCorrect = false;
    if (possibleAnswers) {
      isStepCorrect = possibleAnswers.some(possibleAnswer => 
        normalizeAnswer(possibleAnswer) === normalizedUserAnswer
      );
    }
    
    if (isStepCorrect) {
      // ✅ CORRECT STEP
      const newStepResults = [...stepResults];
      newStepResults[currentStep] = true;
      setStepResults(newStepResults);
      
      if (currentStep < expectedStepAnswers.length - 1) {
        setCurrentStep(currentStep + 1);
        setAttempts(0);
        setShowEncouragement(language === 'en' ? "Good! Now for the next step..." : "جيد! الآن للخطوة التالية...");
      } else {
        setAllStepsComplete(true);
        setIsCorrect(true);
        setShowEncouragement(language === 'en' ? "🎉 Perfect! You've mastered this problem!" : "🎉 ممتاز! لقد أتقنت هذه المسألة!");
        await submitToBackend();
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
        let errorMessage = language === 'en' ? 'Try again.' : 'حاول مرة أخرى.';
        
        if (problem.hints_en?.length > hintIndex && problem.hints_ar?.length > hintIndex) {
          const hint = language === 'en' ? problem.hints_en[hintIndex] : problem.hints_ar[hintIndex];
          errorMessage += ` 💡 ${hint}`;
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
      
      // Update progress immediately
      await fetchData();
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
    setCurrentScore(100); // Reset score
    setExplanationStep(0); // Reset explanation step
    setExplanationAnswers(['', '', '']); // Reset explanation answers
  };

  const handleNextProblem = () => {
    // Get next problem in sequence
    const problemOrder = ['prep1', 'explanation1', 'practice1', 'practice2', 'assessment1', 'examprep1'];
    const currentIndex = problemOrder.indexOf(problemId);
    
    if (currentIndex < problemOrder.length - 1) {
      const nextProblemId = problemOrder[currentIndex + 1];
      // Reset state before navigating
      resetProblemState();
      navigate(`/problem/${nextProblemId}`);
    } else {
      // FIXED: Completed examprep1 - navigate to dashboard with message to start next section
      console.log('🎯 Completed examprep1 - redirecting to dashboard');
      resetProblemState();
      
      // Show completion message and redirect to dashboard
      const completionMessage = language === 'en' 
        ? 'Congratulations! You have completed Section 1. You can now start the next section.'
        : 'تهانينا! لقد أكملت القسم الأول. يمكنك الآن البدء في القسم التالي.';
      
      // Redirect to dashboard to select next section
      navigate('/dashboard', { 
        state: { 
          message: completionMessage,
          completedSection: 'section1' 
        }
      });
    }
  };

  const handleGoToExplanation = () => {
    // Navigate back to explanation stage for review
    console.log('🔄 Navigating back to explanation stage for review');
    resetProblemState();
    navigate('/problem/explanation1');
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
              onClick={() => navigate('/dashboard')}
              className="w-full h-12 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700"
            >
              {text[language].completion.returnToDashboard}
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const problemProgress = userProgress?.section1[problemId] || { completed: false, score: 0, attempts: 0 };
  const isCompleted = problemProgress.completed;
  const earnedScore = problemProgress.score;

  return (
    <div className="min-h-screen p-4">
      {/* Header */}
      <div className="flex justify-between items-center mb-6 max-w-7xl mx-auto">
        <Button onClick={() => navigate('/dashboard')} variant="outline">
          <ArrowLeft className="w-4 h-4 mr-2" />
          {text[language].back}
        </Button>
        <Button onClick={toggleLanguage} variant="outline" size="sm">
          <Globe className="w-4 h-4 mr-2" />
          {language === 'en' ? 'العربية' : 'English'}
        </Button>
      </div>

      {/* Main Content Container - Expanded Width */}
      <div className="max-w-7xl mx-auto w-full">
        {/* Problem Header */}
        <Card className="mb-6">
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
          {/* Problem Card */}
          <Card className="w-full">
            <CardHeader>
              <CardTitle className="text-center">
                {language === 'en' ? 'Solve the inequality:' : 'حل المتباينة:'}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {renderMathExpression(language === 'en' ? problem.question_en : problem.question_ar)}
                
            {/* COMPREHENSIVE EXPLANATION STAGE CONTENT - FULL WIDTH */}
            {problem.show_full_solution && problem.explanation_en && (
              <Card className="mb-6 w-full">
                <CardContent className="p-8">
                  <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-8 rounded-lg border-l-4 border-blue-500 mb-6">
                    <h3 className="font-bold text-2xl mb-6 text-blue-800 flex items-center justify-center">
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

            {/* INTERACTIVE PRACTICE EXAMPLES - TABBED INTERFACE - FULL WIDTH */}
            {problem.interactive_examples && (
              <Card className="mb-6 w-full">
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

                        {/* Show Solution Button */}
                        {!showExample && (
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

                        {/* Solution Display */}
                        {showExample && (
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
                                          {explanationAnswers.slice(0, explanationStep).map((answer, stepIdx) => (
                                            answer && (
                                              <div key={stepIdx} className="mb-2 p-2 bg-blue-100 rounded text-center text-sm text-blue-800">
                                                {language === 'en' ? `Step ${stepIdx + 1}: ` : `الخطوة ${stepIdx + 1}: `}{answer}
                                              </div>
                                            )
                                          ))}
                                        </div>
                                      )}
                                      
                                      {/* Symbol Shortcut Buttons */}
                                      <div className="symbol-buttons-container flex flex-wrap justify-center gap-2 md:flex-nowrap mb-3">
                                        {['<', '>', '≤', '≥', '=', '≠'].map((symbol) => (
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
                                        className="mb-3 text-center text-lg font-mono border-2 border-blue-300 bg-white p-3 min-h-[50px]"
                                      />

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
                                            
                                            stepCorrect = possibleAnswers?.some(ans => normalizeAnswer(ans) === normalized) || false;
                                          }
                                          
                                          console.log(`🔍 Step ${explanationStep + 1} correct:`, stepCorrect);
                                          
                                          if (stepCorrect) {
                                            if (explanationStep < levelSteps.length - 1) {
                                              // Move to next step
                                              setExplanationStep(explanationStep + 1);
                                              const newAnswers = [...explanationAnswers];
                                              newAnswers[index] = ''; // Clear for next step
                                              setExplanationAnswers(newAnswers);
                                              setShowEncouragement(language === 'en' ? "Excellent! Continue to the next step." : "ممتاز! انتقل للخطوة التالية.");
                                            } else {
                                              // Completed all steps for this level
                                              const newPracticeComplete = [...practiceComplete];
                                              newPracticeComplete[index] = true;
                                              setPracticeComplete(newPracticeComplete);
                                              setExplanationStep(0);
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
                                                setAllStepsComplete(true);
                                                setIsCorrect(true);
                                                setTimeout(async () => {
                                                  setShowEncouragement('');
                                                  await submitToBackend();
                                                }, 3000);
                                              }
                                            }
                                            setTimeout(() => setShowEncouragement(''), 3000);
                                          } else {
                                            const hintIndex = stepSolutionIndex;
                                            const correctHints = language === 'ar' ? problem.hints_en : problem.hints_ar;
                                            const stepHint = correctHints?.[hintIndex] || '';
                                            
                                            const feedback = stepHint || (language === 'en' 
                                              ? `Not quite. Please try again.`
                                              : `ليس تماماً. يرجى المحاولة مرة أخرى.`);
                                            
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
                        onClick={handleNextProblem}
                        className="mt-8 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white px-16 py-6 text-2xl font-semibold"
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
                            handleNextProblem();
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
                            
                            {/* Final Answer Input */}
                            <Input
                              value={userAnswer}
                              onChange={(e) => setUserAnswer(e.target.value)}
                              placeholder={language === 'en' ? 'Enter your final answer (e.g., x < 4)...' : 'أدخل إجابتك النهائية (مثال: س < 4)...'}
                              className="mb-4 text-lg h-12"
                            />
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
                            
                            {/* Step Progress Indicator */}
                            <div className="mb-4">
                              <div className="flex items-center justify-center space-x-2 mb-2">
                                {[0, 1, 2].map((step) => (
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
                                ))}
                              </div>
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
                              className="mb-4 text-lg h-12"
                            />
                          </div>
                        );
                        
                      case 'assessment':
                        return (
                          // 4. ASSESSMENT STAGE: Final answer with score penalties
                          <div>
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
                            
                            {/* Final Answer Input */}
                            <Input
                              value={userAnswer}
                              onChange={(e) => setUserAnswer(e.target.value)}
                              placeholder={language === 'en' ? 'Enter your final answer (e.g., x < 4)...' : 'أدخل إجابتك النهائية (مثال: س < 4)...'}
                              className="mb-4 text-lg h-12"
                            />
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
                        if (stageType === 'practice') {
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
                          const stageType = getStageType(problem.type, problem.id);
                          if (stageType === 'practice') {
                            return language === 'en' ? 'Submit Step' : 'إرسال الخطوة';
                          } else {
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
                          if (stageType === 'practice') {
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
                          if (stageType === 'practice') {
                            const newStepAnswers = [...stepAnswers];
                            newStepAnswers[currentStep] = (newStepAnswers[currentStep] || '') + symbol;
                            setStepAnswers(newStepAnswers);
                          } else {
                            setUserAnswer(prev => prev + symbol);
                          }
                        }}
                        onNumberSelect={(number) => {
                          const stageType = getStageType(problem.type, problem.id);
                          if (stageType === 'practice') {
                            const newStepAnswers = [...stepAnswers];
                            newStepAnswers[currentStep] = (newStepAnswers[currentStep] || '') + number;
                            setStepAnswers(newStepAnswers);
                          } else {
                            setUserAnswer(prev => prev + number);
                          }
                        }}
                        onOperatorSelect={(operator) => {
                          const stageType = getStageType(problem.type, problem.id);
                          if (stageType === 'practice') {
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
                            if (stageType === 'practice') {
                              const newStepAnswers = [...stepAnswers];
                              newStepAnswers[currentStep] = '';
                              setStepAnswers(newStepAnswers);
                            } else {
                              setUserAnswer('');
                            }
                          } else if (action === 'backspace') {
                            if (stageType === 'practice') {
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
                          navigate('/problem/explanation1');
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
                    {/* Continue to Next Stage */}
                    {(isCorrect || allStepsComplete) && (
                      <Button 
                        onClick={() => {
                          console.log('🔍 Continue button clicked, navigating to next stage');
                          handleNextProblem();
                        }}
                        className="flex-1 h-12 bg-gradient-to-r from-green-500 to-emerald-600"
                      >
                        <Trophy className="w-4 h-4 mr-2" />
                        {(() => {
                          const stageType = getStageType(problem.type, problem.id);
                          if (stageType === 'preparation') {
                            return language === 'en' ? 'Continue to Explanation Stage →' : 'انتقل لمرحلة الشرح ←';
                          } else if (problem.id === 'examprep1') {
                            return language === 'en' ? 'Start the Next Section →' : 'ابدأ القسم التالي ←';
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
    </div>
  );
};

export default ProblemView;