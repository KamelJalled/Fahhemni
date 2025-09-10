import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth, useLanguage } from '../App';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Globe, ArrowLeft, Lightbulb, CheckCircle, XCircle, RotateCcw, Trophy, Keyboard, Mic } from 'lucide-react';
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

  // FIXED: Enhanced answer normalization with proper validation
  const normalizeAnswer = (answer) => {
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
    
    // ENHANCEMENT: For preparation stage, accept both "x = 7" and "7" formats
    if (problem && (problem.type === 'preparation' || problem.id?.includes('prep'))) {
      // If input is just a number and expected answer has "x =", add "x ="
      if (/^-?\d+(\.\d+)?$/.test(normalized)) {
        const expectedNormalized = normalizeAnswer(problem.answer || '');
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

  // Reset state when problem changes
  useEffect(() => {
    resetProblemState();
  }, [problemId]);

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
      
      // Check against all possible answers for this step
      const possibleAnswers = language === 'en' ? 
        currentStepSolution.possible_answers : 
        currentStepSolution.possible_answers_ar;
      
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
    // Add loading delay for better UX
    setIsChecking(true);
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    try {
      // For step-by-step problems, validate current step
      if (problem.step_solutions && !allStepsComplete) {
        const currentAnswer = stepAnswers[currentStep].trim();
        if (!currentAnswer) return;
        
        const currentStepSolution = problem.step_solutions[currentStep];
        const normalizedAnswer = normalizeAnswer(currentAnswer);
        
        // Check against all possible answers for this step
        const possibleAnswers = language === 'en' ? 
          currentStepSolution.possible_answers : 
          currentStepSolution.possible_answers_ar;
        
        const isStepCorrect = possibleAnswers.some(possibleAnswer => 
          normalizeAnswer(possibleAnswer) === normalizedAnswer
        );
        
        if (isStepCorrect) {
          // Step is correct - move to next step or complete
          const newStepResults = [...stepResults];
          newStepResults[currentStep] = true;
          setStepResults(newStepResults);
          
          if (currentStep < problem.step_solutions.length - 1) {
            setCurrentStep(currentStep + 1);
            setShowEncouragement(`✅ ${language === 'en' ? 'Great! Now continue with the next step.' : 'رائع! الآن تابع مع الخطوة التالية.'}`);
            setTimeout(() => setShowEncouragement(''), 2000);
          } else if (problem.final_answer_required) {
            setAllStepsComplete(true);
            setShowEncouragement(`✅ ${language === 'en' ? 'Excellent! Now enter your final answer below.' : 'ممتاز! الآن أدخل إجابتك النهائية أدناه.'}`);
            setTimeout(() => setShowEncouragement(''), 3000);
          } else {
            setAllStepsComplete(true);
            setIsCorrect(true);
            await submitToBackend();
          }
        } else {
          setIsCorrect(false);
          
          // Enhanced error feedback with hints after multiple attempts
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
      } else if (problem.final_answer_required && allStepsComplete) {
        // Check final answer with enhanced logging
        const finalAnswer = stepAnswers[problem.step_solutions?.length || 0] || userAnswer;
        const normalizedFinalAnswer = normalizeAnswer(finalAnswer);
        const normalizedCorrectAnswer = normalizeAnswer(problem.answer);
        
        console.log(`🔍 Final answer validation:
          User answer: "${finalAnswer}" → "${normalizedFinalAnswer}"
          Correct answer: "${problem.answer}" → "${normalizedCorrectAnswer}"
          Match: ${normalizedFinalAnswer === normalizedCorrectAnswer}`);
        
        if (normalizedFinalAnswer === normalizedCorrectAnswer) {
          setIsCorrect(true);
          await submitToBackend();
        } else {
          setIsCorrect(false);
          
          // Enhanced error feedback with hints after multiple attempts
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
      } else {
        // FIXED: Single answer problems (like preparation stage)
        const userSubmittedAnswer = stepAnswers[0] || userAnswer;
        const normalizedUserAnswer = normalizeAnswer(userSubmittedAnswer);
        const normalizedCorrectAnswer = normalizeAnswer(problem.answer);
        
        console.log(`🔍 Single answer validation:
          User answer: "${userSubmittedAnswer}" → "${normalizedUserAnswer}"
          Correct answer: "${problem.answer}" → "${normalizedCorrectAnswer}"
          Match: ${normalizedUserAnswer === normalizedCorrectAnswer}`);
          
        if (normalizedUserAnswer === normalizedCorrectAnswer) {
          setIsCorrect(true);
          
          // FIXED: Special handling for preparation stage completion with learning invitation
          if (problem.type === 'preparation' || problem.id?.includes('prep')) {
            const sectionName = problem.section_title || 'One-Step Inequalities';
            const invitationMessage = language === 'en' 
              ? `🎉 Excellent work! You solved this correctly. Now let's learn how to solve ${sectionName} step by step. Click "Continue to Next Stage" to start the guided learning process.`
              : `🎉 عمل ممتاز! لقد حللت هذه المسألة بشكل صحيح. الآن دعنا نتعلم كيفية حل ${sectionName} خطوة بخطوة. انقر على "انتقل للمرحلة التالية" لبدء عملية التعلم الموجه.`;
            
            setShowEncouragement(invitationMessage);
            setTimeout(() => setShowEncouragement(''), 8000); // Extended time for longer message
          }
          
          await submitToBackend();
        } else {
          setIsCorrect(false);
          
          // Enhanced error feedback with hints after multiple attempts
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
      }
    } catch (error) {
      console.error('Error submitting answer:', error);
    } finally {
      setIsChecking(false);
    }
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
      // Completed last problem in section - show completion screen
      const currentSection = problemId.includes('section1') || problemOrder.includes(problemId) ? 'section1' : 'unknown';
      
      // Check if this is the final section (Section 5) - for now treating section1 as demo completion
      if (currentSection === 'section1') {
        setCompletionType('final'); // Demo completion
      } else {
        setCompletionType('section'); // Regular section completion
      }
      
      setShowCompletionScreen(true);
    }
  };

  const handleTryAgain = () => {
    resetProblemState();
  };

  // Voice input handlers
  const handleVoiceResult = (result) => {
    if (problem?.step_solutions && problem.step_solutions.length > 0) {
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
        if (problem?.step_solutions && problem.step_solutions.length > 0) {
          const newAnswers = [...stepAnswers];
          newAnswers[activeInputIndex] = '';
          setStepAnswers(newAnswers);
        } else {
          setUserAnswer('');
        }
        break;
      case 'backspace':
        if (problem?.step_solutions && problem.step_solutions.length > 0) {
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
    if (problem?.step_solutions && problem.step_solutions.length > 0) {
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
      <div className="flex justify-between items-center mb-6">
        <Button onClick={() => navigate('/dashboard')} variant="outline">
          <ArrowLeft className="w-4 h-4 mr-2" />
          {text[language].back}
        </Button>
        <Button onClick={toggleLanguage} variant="outline" size="sm">
          <Globe className="w-4 h-4 mr-2" />
          {language === 'en' ? 'العربية' : 'English'}
        </Button>
      </div>

      <div className="max-w-4xl mx-auto">
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

        {/* Problem Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column - Problem */}
          <div>
            <Card className="mb-6">
              <CardHeader>
                <CardTitle className="text-center">
                  {language === 'en' ? 'Solve the inequality:' : 'حل المتباينة:'}
                </CardTitle>
              </CardHeader>
              <CardContent>
                {renderMathExpression(language === 'en' ? problem.question_en : problem.question_ar)}
                
            {/* Show explanation or preparation content */}
            {problem.show_full_solution && problem.explanation_en && (
              <Card className="mb-6">
                <CardContent className="p-6">
                  <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                    <h4 className="font-semibold mb-2 text-blue-800">
                      {text[language].explanation}
                    </h4>
                    <pre className="whitespace-pre-wrap text-sm text-blue-700">
                      {language === 'en' ? problem.explanation_en : problem.explanation_ar}
                    </pre>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Interactive Examples for Explanation */}
            {problem.interactive_examples && (
              <Card className="mb-6">
                <CardContent className="p-6">
                  <div className="space-y-6">
                    {problem.interactive_examples.map((example, index) => (
                      <div key={index} className="border rounded-lg p-4">
                        <h4 className="font-semibold text-lg mb-3 text-blue-700">
                          {language === 'en' ? example.title_en : example.title_ar}
                        </h4>
                        
                        {/* Show example */}
                        <div className="bg-gray-50 p-4 rounded-lg mb-4">
                          <div className="text-xl font-mono text-center mb-2">
                            {language === 'en' ? example.problem_en : example.problem_ar}
                          </div>
                          
                          {(showExample && currentExample === index) && (
                            <div className="mt-4 text-sm">
                              <pre className="whitespace-pre-wrap text-gray-700">
                                {language === 'en' ? example.solution_en : example.solution_ar}
                              </pre>
                            </div>
                          )}
                          
                          {!showExample && currentExample === index && (
                            <Button 
                              onClick={() => setShowExample(true)}
                              className="mt-2 w-full"
                              variant="outline"
                            >
                              {language === 'en' ? 'Show Solution' : 'إظهار الحل'}
                            </Button>
                          )}
                        </div>

                        {/* Practice problem */}
                        {showExample && currentExample === index && (
                          <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                            <h5 className="font-medium mb-2 text-yellow-800">
                              {language === 'en' ? 'Try It Yourself:' : 'جربه بنفسك:'}
                            </h5>
                            <div className="text-lg font-mono text-center mb-3">
                              {language === 'en' ? example.practice_question_en : example.practice_question_ar}
                            </div>
                            
                            <Input
                              value={practiceAnswer}
                              onChange={(e) => setPracticeAnswer(e.target.value)}
                              placeholder={language === 'en' ? 'Enter your answer...' : 'أدخل إجابتك...'}
                              className="mb-3"
                            />
                            
                            <Button 
                              onClick={() => {
                                const correct = normalizeAnswer(practiceAnswer) === normalizeAnswer(example.practice_answer);
                                if (correct) {
                                  const newPracticeComplete = [...practiceComplete];
                                  newPracticeComplete[index] = true;
                                  setPracticeComplete(newPracticeComplete);
                                  setPracticeAnswer('');
                                  if (index < problem.interactive_examples.length - 1) {
                                    setCurrentExample(index + 1);
                                    setShowExample(false);
                                  }
                                } else {
                                  setShowEncouragement(text[language].encouragement[Math.floor(Math.random() * text[language].encouragement.length)]);
                                  setTimeout(() => setShowEncouragement(''), 3000);
                                }
                              }}
                              className="w-full"
                              disabled={!practiceAnswer.trim()}
                            >
                              {language === 'en' ? 'Check Answer' : 'تحقق من الإجابة'}
                            </Button>
                            
                            {practiceComplete[index] && (
                              <div className="mt-2 p-2 bg-green-100 text-green-800 rounded text-center">
                                ✓ {language === 'en' ? 'Correct! Well done!' : 'صحيح! أحسنت!'}
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    ))}
                    
                    {/* Mark explanation complete when all examples practiced */}
                    {practiceComplete.length === problem.interactive_examples.length && 
                     practiceComplete.every(completed => completed) && (
                      <div className="text-center p-6 bg-green-50 rounded-lg border border-green-200">
                        <div className="text-green-600 mb-3">
                          <CheckCircle className="w-12 h-12 mx-auto mb-2" />
                          <h3 className="text-lg font-semibold">
                            {language === 'en' ? 'Explanation Complete!' : 'اكتمل الشرح!'}
                          </h3>
                          <p className="text-sm">
                            {language === 'en' 
                              ? 'You have successfully practiced all examples. Ready for the next challenge!' 
                              : 'لقد تدربت بنجاح على جميع الأمثلة. جاهز للتحدي التالي!'
                            }
                          </p>
                        </div>
                        <Button 
                          onClick={async () => {
                            // Mark stage as completed
                            await submitToBackend();
                            handleNextProblem();
                          }}
                          className="bg-gradient-to-r from-green-500 to-emerald-600"
                        >
                          {language === 'en' ? 'Continue to Practice Problems →' : 'تابع لمسائل التدريب ←'}
                        </Button>
                      </div>
                    )}
                  </div>
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
            </Card>

            {/* Answer Input - FIXED: Show for ALL stages with keyboard support */}
            <Card>
              <CardContent className="p-6">
                  <div className="space-y-4">
                    {/* Step-by-step inputs for practice problems */}
                    {problem.step_solutions ? (
                      <>
                        <h4 className="font-semibold text-lg mb-4">
                          {language === 'en' ? 'Solve Step by Step:' : 'حل خطوة بخطوة:'}
                        </h4>
                        
                        {problem.step_solutions.map((step, index) => (
                          <div key={index} className={`border rounded-lg p-4 ${
                            index <= currentStep ? 'bg-white' : 'bg-gray-50 opacity-50'
                          }`}>
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex items-center">
                                <span className={`w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold mr-3 ${
                                  stepResults[index] ? 'bg-green-500 text-white' : 
                                  index === currentStep ? 'bg-blue-500 text-white' : 
                                  'bg-gray-300 text-gray-600'
                                }`}>
                                  {stepResults[index] ? '✓' : index + 1}
                                </span>
                                <div>
                                  <div className="font-medium text-sm text-gray-600">
                                    {getStepLabel(index, step)}
                                  </div>
                                </div>
                              </div>
                            </div>
                            <div className="flex gap-2">
                              <Input
                                value={stepAnswers[index]}
                                onChange={(e) => handleStepAnswerChange(index, e.target.value)}
                                onFocus={() => {
                                  handleInputFocus(index);
                                  // Auto-scroll to keep input visible on mobile
                                  setTimeout(() => {
                                    document.querySelector(`input[data-step="${index}"]`)?.scrollIntoView({ 
                                      behavior: 'smooth', 
                                      block: 'center' 
                                    });
                                  }, 100);
                                }}
                                data-step={index}
                                placeholder={language === 'en' ? 
                                  'Show your work for this step...' : 
                                  'أظهر عملك لهذه الخطوة...'
                                }
                                className="problem-input-focused flex-1 text-lg h-12"
                                disabled={index > currentStep || stepResults[index]}
                              />
                              
                              {/* Individual Check Step Button */}
                              {index === currentStep && !stepResults[index] && (
                                <Button 
                                  onClick={() => handleCheckStep(index)}
                                  className="px-4 bg-blue-600 text-white hover:bg-blue-700"
                                  disabled={!stepAnswers[index]?.trim() || (isChecking && checkingStepIndex === index)}
                                  size="sm"
                                >
                                  {isChecking && checkingStepIndex === index ? (
                                    <div className="flex items-center">
                                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                                      {text[language].completion.checking}
                                    </div>
                                  ) : (
                                    language === 'en' ? 'Check Step' : 'تحقق'
                                  )}
                                </Button>
                              )}
                              
                              <Button 
                                variant="outline"
                                size="sm"
                                onClick={() => {
                                  setActiveInputIndex(index);
                                  setShowVoiceInput(!showVoiceInput);
                                  setShowMathKeyboard(false);
                                }}
                                className="voice-input-button px-3 border-blue-300 text-blue-600 hover:bg-blue-50"
                                disabled={index > currentStep || stepResults[index]}
                                title={language === 'ar' ? 'إدخال صوتي' : 'Voice Input'}
                              >
                                <Mic className="w-4 h-4" />
                              </Button>
                              <Button 
                                variant="outline"
                                size="sm"
                                onClick={() => {
                                  setActiveInputIndex(index);
                                  setShowMathKeyboard(!showMathKeyboard);
                                  setShowVoiceInput(false);
                                }}
                                className="px-3 border-purple-300 text-purple-600 hover:bg-purple-50"
                                disabled={index > currentStep || stepResults[index]}
                                title={language === 'ar' ? 'لوحة مفاتيح رياضية' : 'Math Keyboard'}
                              >
                                <Keyboard className="w-4 h-4" />
                              </Button>
                            </div>
                          </div>
                        ))}

                        {/* Final Answer Box (if required) */}
                        {problem.final_answer_required && allStepsComplete && (
                          <div className="border-2 border-green-200 rounded-lg p-4 bg-green-50">
                            <div className="flex items-center mb-2">
                              <span className="w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold mr-3 bg-green-500 text-white">
                                ✓
                              </span>
                              <label className="font-medium text-green-800">
                                {language === 'en' ? 'Final Answer:' : 'الإجابة النهائية:'}
                              </label>
                            </div>
                            <Input
                              value={userAnswer}
                              onChange={(e) => setUserAnswer(e.target.value)}
                              placeholder={language === 'en' ? 
                                'Enter your final answer (e.g., x = 7)' : 
                                'أدخل إجابتك النهائية (مثال: س = ٧)'
                              }
                              className="text-lg h-12 bg-white"
                            />
                          </div>
                        )}
                      </>
                    ) : (
                      // Single answer input for non-step problems
                      <div>
                        <label className="block text-sm font-medium mb-2">
                          {text[language].yourAnswer}
                        </label>
                        <div className="flex gap-2">
                          <Input
                            value={stepAnswers[0]}
                            onChange={(e) => handleStepAnswerChange(0, e.target.value)}
                            onFocus={() => handleInputFocus(0)}
                            placeholder={language === 'en' ? 'Enter your answer (e.g., x > 5)' : 'أدخل إجابتك (مثل: س > ٥)'}
                            className="flex-1 text-lg h-12"
                            disabled={isCompleted && !isSubmitted}
                          />
                          <Button 
                            variant="outline"
                            size="sm"
                            onClick={() => {
                              setActiveInputIndex(0);
                              setShowVoiceInput(!showVoiceInput);
                              setShowMathKeyboard(false);
                            }}
                            className="voice-input-button px-3 border-blue-300 text-blue-600 hover:bg-blue-50"
                            disabled={isCompleted && !isSubmitted}
                            title={language === 'ar' ? 'إدخال صوتي' : 'Voice Input'}
                          >
                            <Mic className="w-4 h-4" />
                          </Button>
                          <Button 
                            variant="outline"
                            size="sm"
                            onClick={() => {
                              setActiveInputIndex(0);
                              setShowMathKeyboard(!showMathKeyboard);
                              setShowVoiceInput(false);
                            }}
                            className="px-3 border-purple-300 text-purple-600 hover:bg-purple-50"
                            disabled={isCompleted && !isSubmitted}
                            title={language === 'ar' ? 'لوحة مفاتيح رياضية' : 'Math Keyboard'}
                          >
                            <Keyboard className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                    )}

                    {/* Voice Input Component */}
                    {showVoiceInput && (
                      <div className="mt-4">
                        <VoiceInput
                          onResult={handleVoiceResult}
                          onError={handleVoiceError}
                          disabled={false}
                        />
                      </div>
                    )}

                    {/* Math Keyboard Component */}
                    {showMathKeyboard && (
                      <div className="mt-4">
                        <MathKeyboard
                          onSymbolSelect={handleSymbolSelect}
                          onNumberSelect={handleNumberSelect}
                          onOperatorSelect={handleOperatorSelect}
                          onAction={handleKeyboardAction}
                        />
                      </div>
                    )}

                    {/* Encouragement Message */}
                    {showEncouragement && (
                      <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                        <p className="text-yellow-800 text-center font-medium">
                          {showEncouragement}
                        </p>
                      </div>
                    )}

                    {/* Action Buttons - Mobile Optimized with Sticky Container */}
                    <div className="continue-button-container flex gap-2">
                      {!isCorrect && !isSubmitted ? (
                        <>
                          {/* Main Submit Button - FIXED: Show for preparation stage and final answers */}
                          {((!problem.step_solutions || problem.step_solutions.length === 0) || (problem.final_answer_required && allStepsComplete)) && (
                            <Button 
                              onClick={handleSubmit}
                              className="flex-1 h-12 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700"
                              disabled={
                                isChecking || (
                                  problem.final_answer_required && allStepsComplete ? 
                                    (!userAnswer?.trim()) :
                                    (!stepAnswers[0]?.trim())
                                )
                              }
                            >
                              {isChecking ? (
                                <div className="flex items-center">
                                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                                  {text[language].completion.checking}
                                </div>
                              ) : (
                                problem.final_answer_required && allStepsComplete ?
                                  (language === 'en' ? 'Submit Final Answer' : 'إرسال الإجابة النهائية') :
                                  (language === 'en' ? 'Submit Answer' : 'إرسال الإجابة')
                              )}
                            </Button>
                          )}
                        </>
                      ) : (
                        <>
                          <Button 
                            onClick={handleTryAgain}
                            className="flex-1 h-12"
                            variant="outline"
                          >
                            <RotateCcw className="w-4 h-4 mr-2" />
                            {text[language].tryAgain}
                          </Button>
                          
                          {(allStepsComplete || isCorrect) && (
                            <Button 
                              onClick={handleNextProblem}
                              className="flex-1 h-12 bg-gradient-to-r from-green-500 to-emerald-600"
                            >
                              <Trophy className="w-4 h-4 mr-2" />
                              {language === 'en' ? 'Continue to Next Stage →' : 'انتقل للمرحلة التالية ←'}
                            </Button>
                          )}
                        </>
                      )}
                    </div>

                    {/* Result Display */}
                    {(isSubmitted || allStepsComplete) && (
                      <div className={`p-4 rounded-lg border ${
                        (isCorrect || allStepsComplete)
                          ? 'bg-green-50 border-green-200 text-green-800' 
                          : 'bg-red-50 border-red-200 text-red-800'
                      }`}>
                        <div className="flex items-center">
                          {(isCorrect || allStepsComplete) ? (
                            <CheckCircle className="w-5 h-5 mr-2" />
                          ) : (
                            <XCircle className="w-5 h-5 mr-2" />
                          )}
                          <span className="font-medium">
                            {(isCorrect || allStepsComplete) ? text[language].correct : text[language].incorrect}
                          </span>
                        </div>
                        
                        {/* Show correct answer only for non-assessment problems */}
                        {!isCorrect && !allStepsComplete && !problem.hide_answer && (
                          <div className="mt-2 text-sm">
                            {language === 'en' ? 'Correct answer: ' : 'الإجابة الصحيحة: '}
                            <span className="font-mono">{problem.answer}</span>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
          </div>

          {/* Right Column - Hints (Hidden by Default) */}
          {(problem.hints_en?.length > 0 || problem.hints_ar?.length > 0) && !problem.show_full_solution && (
            <div>
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Lightbulb className="w-5 h-5 mr-2 text-yellow-500" />
                    {language === 'en' ? 'Hints' : 'الإرشادات'}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {/* Hint Usage Tracker */}
                    <div>
                      <div className="flex justify-between text-sm text-gray-500 mb-2">
                        <span>{language === 'en' ? 'Hints Used' : 'الإرشادات المستخدمة'}</span>
                        <span>{hintsUsed}/{(language === 'en' ? problem.hints_en : problem.hints_ar)?.length || 0}</span>
                      </div>
                      <Progress value={(hintsUsed / ((language === 'en' ? problem.hints_en : problem.hints_ar)?.length || 1)) * 100} />
                    </div>

                    {/* Operator Instructions */}
                    <div className="text-xs text-gray-600 bg-gray-50 p-2 rounded">
                      {language === 'en' 
                        ? 'Accepted operators: +, -, *, /, ×, ÷, <, >, ≤, ≥'
                        : 'العمليات المقبولة: +, -, *, /, ×, ÷, <, >, ≤, ≥'
                      }
                    </div>

                    {/* Step-based Hints */}
                    {problem.step_solutions ? (
                      problem.step_solutions.map((step, index) => (
                        <div key={index} className={`border rounded-lg p-3 ${
                          index <= currentStep ? 'bg-white' : 'bg-gray-50 opacity-50'
                        }`}>
                          <div className="flex justify-between items-center mb-2">
                            <span className="text-sm font-medium">
                              {language === 'en' ? `Step ${index + 1} Hint` : `إرشاد الخطوة ${index + 1}`}
                            </span>
                            <Button 
                              onClick={() => handleStepHintToggle(index)}
                              variant="outline" 
                              size="sm"
                              disabled={index > currentStep}
                            >
                              <Lightbulb className="w-3 h-3 mr-1" />
                              {showHints[index] ? 
                                (language === 'en' ? 'Hide' : 'إخفاء') : 
                                (language === 'en' ? 'Show' : 'إظهار')
                              }
                            </Button>
                          </div>
                          
                          {showHints[index] && (
                            <div className="bg-yellow-50 p-3 rounded border border-yellow-200">
                              <p className="text-yellow-800 text-sm">
                                {language === 'en' ? problem.hints_en[index] : problem.hints_ar[index]}
                              </p>
                            </div>
                          )}
                        </div>
                      ))
                    ) : (
                      /* Single problem hints */
                      <div className="space-y-3">
                        {(language === 'en' ? problem.hints_en : problem.hints_ar)?.map((hint, index) => (
                          <div key={index} className="border rounded-lg p-3">
                            <div className="flex justify-between items-center mb-2">
                              <span className="text-sm font-medium">
                                {language === 'en' ? `Hint ${index + 1}` : `إرشاد ${index + 1}`}
                              </span>
                              <Button 
                                onClick={() => {
                                  const newShowHints = [...showHints];
                                  newShowHints[index] = !newShowHints[index];
                                  setShowHints(newShowHints);
                                  if (newShowHints[index]) {
                                    setHintsUsed(hintsUsed + 1);
                                  }
                                }}
                                variant="outline" 
                                size="sm"
                              >
                                <Lightbulb className="w-3 h-3 mr-1" />
                                {showHints[index] ? 
                                  (language === 'en' ? 'Hide' : 'إخفاء') : 
                                  (language === 'en' ? 'Show' : 'إظهار')
                                }
                              </Button>
                            </div>
                            
                            {showHints[index] && (
                              <div className="bg-yellow-50 p-3 rounded border border-yellow-200">
                                <p className="text-yellow-800 text-sm">{hint}</p>
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Hints Impact Notice */}
                    {hintsUsed > 0 && (
                      <div className="text-xs text-orange-600 text-center">
                        {language === 'en' 
                          ? `Using hints may affect your score (-${hintsUsed * 10} points)`
                          : `استخدام الإرشادات قد يؤثر على نتيجتك (-${hintsUsed * 10} نقطة)`
                        }
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProblemView;