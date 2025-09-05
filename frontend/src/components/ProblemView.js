import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth, useLanguage } from '../App';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Globe, ArrowLeft, Lightbulb, CheckCircle, XCircle, RotateCcw, Trophy } from 'lucide-react';
import { useToast } from '../hooks/use-toast';

const ProblemView = () => {
  const { problemId } = useParams();
  const { user } = useAuth();
  const { language, toggleLanguage } = useLanguage();
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const [stepAnswers, setStepAnswers] = useState(['', '', '']); // For 3-step solving
  const [currentStep, setCurrentStep] = useState(0);
  const [currentHint, setCurrentHint] = useState(0);
  const [showHints, setShowHints] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [stepResults, setStepResults] = useState([false, false, false]); // Track each step result
  const [attempts, setAttempts] = useState(0);
  const [showEncouragement, setShowEncouragement] = useState(false);
  const [userProgress, setUserProgress] = useState(null);
  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [allStepsComplete, setAllStepsComplete] = useState(false);
  const [userAnswer, setUserAnswer] = useState('');

  // Helper function to normalize answer
  const normalizeAnswer = (answer) => {
    // Convert Arabic numerals to Western and س to x
    const arabicToWestern = {'٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'};
    return answer.toLowerCase()
      .replace(/س/g, 'x')
      .replace(/[٠-٩]/g, (digit) => arabicToWestern[digit])
      .trim();
  };

  useEffect(() => {
    if (!user || !problemId) {
      navigate('/dashboard');
      return;
    }

    fetchData();
  }, [user, problemId, navigate]);

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
      placeholder: "Enter your answer (e.g., x > 5 or س > ٥)",
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
      backToDashboard: "Back to Dashboard"
    },
    ar: {
      back: "العودة للوحة التحكم",
      submit: "إرسال الإجابة",
      tryAgain: "حاول مرة أخرى",
      showHint: "إظهار الإرشاد",
      nextHint: "الإرشاد التالي",
      noMoreHints: "لا توجد إرشادات أخرى متاحة",
      yourAnswer: "إجابتك",
      placeholder: "أدخل إجابتك (مثل: س > ٥ أو x > 5)",
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
      backToDashboard: "العودة للوحة التحكم"
    }
  };

  const handleSubmit = async () => {
    if (!stepAnswers[currentStep].trim() && !allStepsComplete) return;

    try {
      // For step-by-step problems, validate current step
      if (problem.step_solutions && !allStepsComplete) {
        const currentStepSolution = problem.step_solutions[currentStep];
        const normalizedAnswer = normalizeAnswer(stepAnswers[currentStep]);
        const normalizedCorrect = normalizeAnswer(language === 'en' ? currentStepSolution.answer_en : currentStepSolution.answer_ar);
        
        if (normalizedAnswer === normalizedCorrect) {
          // Step is correct
          const newStepResults = [...stepResults];
          newStepResults[currentStep] = true;
          setStepResults(newStepResults);
          
          if (currentStep < problem.step_solutions.length - 1) {
            // Move to next step
            setCurrentStep(currentStep + 1);
            setCurrentHint(currentStep + 1); // Show hint for next step
          } else {
            // All steps complete
            setAllStepsComplete(true);
            setIsCorrect(true);
            
            // Submit final answer to backend
            const response = await fetch(
              `${process.env.REACT_APP_BACKEND_URL}/api/students/${user.username}/attempt`,
              {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  problem_id: problemId,
                  answer: problem.answer,
                  hints_used: currentHint
                }),
              }
            );
            
            if (response.ok) {
              const result = await response.json();
              setAttempts(result.attempts);
              toast({
                title: text[language].correct,
                description: `${text[language].points}: ${result.score}`,
              });
              fetchData();
            }
          }
        } else {
          // Step is incorrect
          setShowEncouragement(text[language].encouragement[Math.floor(Math.random() * text[language].encouragement.length)]);
          setTimeout(() => setShowEncouragement(''), 3000);
        }
      } else {
        // Single answer submission (for non-step problems)
        const response = await fetch(
          `${process.env.REACT_APP_BACKEND_URL}/api/students/${user.username}/attempt`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              problem_id: problemId,
              answer: stepAnswers[0].trim(),
              hints_used: currentHint
            }),
          }
        );

        if (response.ok) {
          const result = await response.json();
          setIsSubmitted(true);
          setIsCorrect(result.correct);
          setAttempts(result.attempts);

          if (result.correct) {
            toast({
              title: text[language].correct,
              description: `${text[language].points}: ${result.score}`,
            });
          } else {
            const encouragementIndex = Math.floor(Math.random() * text[language].encouragement.length);
            setShowEncouragement(text[language].encouragement[encouragementIndex]);
            setTimeout(() => setShowEncouragement(''), 3000);
          }
          fetchData();
        }
      }
    } catch (error) {
      console.error('Error submitting answer:', error);
    }
  };

  const handleTryAgain = () => {
    setStepAnswers(['', '', '']);
    setCurrentStep(0);
    setCurrentHint(0);
    setIsSubmitted(false);
    setIsCorrect(false);
    setStepResults([false, false, false]);
    setAllStepsComplete(false);
    setShowHints(false);
    setUserAnswer('');
  };

  const handleNextProblem = () => {
    // Get next problem in sequence
    const problemOrder = ['prep1', 'explanation1', 'practice1', 'practice2', 'assessment1', 'examprep1'];
    const currentIndex = problemOrder.indexOf(problemId);
    if (currentIndex < problemOrder.length - 1) {
      const nextProblemId = problemOrder[currentIndex + 1];
      navigate(`/problem/${nextProblemId}`);
    } else {
      navigate('/dashboard');
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
                
                {/* Show explanation for preparation and explanation problems */}
                {problem.show_full_solution && (problem.explanation_en || problem.explanation_ar) && (
                  <div className="mt-6 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                    <h4 className="font-semibold mb-2 text-blue-800">
                      {text[language].explanation}
                    </h4>
                    <pre className="whitespace-pre-wrap text-sm text-blue-700">
                      {language === 'en' ? problem.explanation_en : problem.explanation_ar}
                    </pre>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Answer Input - Only for non-explanation problems */}
            {!problem.show_full_solution && (
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
                            <div className="flex items-center mb-2">
                              <span className={`w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold mr-3 ${
                                stepResults[index] ? 'bg-green-500 text-white' : 
                                index === currentStep ? 'bg-blue-500 text-white' : 
                                'bg-gray-300 text-gray-600'
                              }`}>
                                {stepResults[index] ? '✓' : index + 1}
                              </span>
                              <label className="font-medium">
                                {language === 'en' ? step.step_en : step.step_ar}
                              </label>
                            </div>
                            <Input
                              value={stepAnswers[index]}
                              onChange={(e) => handleStepAnswerChange(index, e.target.value)}
                              placeholder={language === 'en' ? 'Enter your answer for this step...' : 'أدخل إجابتك لهذه الخطوة...'}
                              className="text-lg h-12"
                              disabled={index > currentStep || stepResults[index]}
                            />
                          </div>
                        ))}
                      </>
                    ) : (
                      // Single answer input for non-step problems
                      <div>
                        <label className="block text-sm font-medium mb-2">
                          {text[language].yourAnswer}
                        </label>
                        <Input
                          value={stepAnswers[0]}
                          onChange={(e) => handleStepAnswerChange(0, e.target.value)}
                          placeholder={language === 'en' ? 'Enter your answer (e.g., x > 5)' : 'أدخل إجابتك (مثل: س > ٥)'}
                          className="text-lg h-12"
                          disabled={isCompleted && !isSubmitted}
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

                    {/* Submit/Try Again/Next Problem Buttons */}
                    <div className="flex gap-2">
                      {!allStepsComplete && !isSubmitted ? (
                        <Button 
                          onClick={handleSubmit}
                          className="flex-1 h-12 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700"
                          disabled={!stepAnswers[currentStep]?.trim() && !problem.step_solutions}
                        >
                          {problem.step_solutions && currentStep < (problem.step_solutions?.length - 1) ? 
                            (language === 'en' ? 'Next Step →' : 'الخطوة التالية ←') :
                            text[language].submit
                          }
                        </Button>
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
                              {language === 'en' ? 'Next Problem →' : 'المسألة التالية ←'}
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
            )}
          </div>

          {/* Right Column - Hints */}
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
                    {/* Hint Progress */}
                    <div>
                      <div className="flex justify-between text-sm text-gray-500 mb-2">
                        <span>{language === 'en' ? 'Hints Used' : 'الإرشادات المستخدمة'}</span>
                        <span>{showHints ? currentHint + 1 : 0}/{(language === 'en' ? problem.hints_en : problem.hints_ar)?.length || 0}</span>
                      </div>
                      <Progress value={(showHints ? currentHint + 1 : 0) / ((language === 'en' ? problem.hints_en : problem.hints_ar)?.length || 1) * 100} />
                    </div>

                    {/* Show Hints Button */}
                    {!showHints && (
                      <Button 
                        onClick={() => setShowHints(true)}
                        variant="outline"
                        className="w-full"
                      >
                        <Lightbulb className="w-4 h-4 mr-2" />
                        {text[language].showHint}
                      </Button>
                    )}

                    {/* Display Current Hint */}
                    {showHints && (
                      <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                        <p className="text-yellow-800">
                          {language === 'en' ? problem.hints_en[currentHint] : problem.hints_ar[currentHint]}
                        </p>
                      </div>
                    )}

                    {/* Next Hint Button */}
                    {showHints && currentHint < ((language === 'en' ? problem.hints_en : problem.hints_ar)?.length || 0) - 1 && (
                      <Button 
                        onClick={handleNextHint}
                        variant="outline"
                        className="w-full"
                      >
                        {text[language].nextHint}
                      </Button>
                    )}

                    {/* No More Hints Message */}
                    {showHints && currentHint === ((language === 'en' ? problem.hints_en : problem.hints_ar)?.length || 0) - 1 && (
                      <p className="text-center text-gray-500 text-sm">
                        {problem.hide_answer ? text[language].noMoreHints : 
                         language === 'en' ? 'All hints used' : 'تم استخدام جميع الإرشادات'}
                      </p>
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