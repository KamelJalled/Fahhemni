import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth, useLanguage } from '../App';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Globe, ArrowLeft, Lightbulb, CheckCircle, XCircle, RotateCcw, Trophy } from 'lucide-react';
import { mockProblems, normalizeAnswer } from '../mock';
import { useToast } from '../hooks/use-toast';

const ProblemView = () => {
  const { problemId } = useParams();
  const { user } = useAuth();
  const { language, toggleLanguage } = useLanguage();
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const [userAnswer, setUserAnswer] = useState('');
  const [currentHint, setCurrentHint] = useState(0);
  const [showHints, setShowHints] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [attempts, setAttempts] = useState(0);
  const [showEncouragement, setShowEncouragement] = useState(false);
  const [userProgress, setUserProgress] = useState(null);

  const problem = mockProblems.section1.problems.find(p => p.id === problemId);

  useEffect(() => {
    if (!user || !problem) {
      navigate('/dashboard');
      return;
    }

    // Load user progress
    const savedProgress = localStorage.getItem(`mathapp_progress_${user.username}`);
    if (savedProgress) {
      const progress = JSON.parse(savedProgress);
      setUserProgress(progress);
      setAttempts(progress.section1[problemId]?.attempts || 0);
    }
  }, [user, problem, problemId, navigate]);

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

  const handleSubmit = () => {
    if (!userAnswer.trim()) return;

    const normalizedUserAnswer = normalizeAnswer(userAnswer);
    const normalizedCorrectAnswer = normalizeAnswer(problem.answer);
    const newAttempts = attempts + 1;
    
    setAttempts(newAttempts);
    setIsSubmitted(true);

    const correct = normalizedUserAnswer === normalizedCorrectAnswer;
    setIsCorrect(correct);

    // Calculate score based on attempts and hints used
    let score = 0;
    if (correct) {
      score = Math.max(40, 100 - (newAttempts - 1) * 20 - currentHint * 10);
    }

    // Update progress in localStorage
    if (userProgress) {
      const updatedProgress = { ...userProgress };
      updatedProgress.section1[problemId] = {
        completed: correct,
        score: correct ? score : Math.max(updatedProgress.section1[problemId]?.score || 0, score),
        attempts: newAttempts
      };
      
      setUserProgress(updatedProgress);
      localStorage.setItem(`mathapp_progress_${user.username}`, JSON.stringify(updatedProgress));
    }

    // Show toast notification
    if (correct) {
      toast({
        title: text[language].correct,
        description: `${text[language].points}: ${score}`,
        variant: "success"
      });
    } else {
      // Show random encouragement
      const encouragementIndex = Math.floor(Math.random() * text[language].encouragement.length);
      setShowEncouragement(text[language].encouragement[encouragementIndex]);
      setTimeout(() => setShowEncouragement(''), 3000);
    }
  };

  const handleTryAgain = () => {
    setUserAnswer('');
    setIsSubmitted(false);
    setIsCorrect(false);
  };

  const handleNextHint = () => {
    if (currentHint < (problem.hints?.length || 0) - 1) {
      setCurrentHint(currentHint + 1);
    }
    setShowHints(true);
  };

  const renderMathExpression = (expression) => {
    return (
      <div className="text-3xl font-mono bg-gray-50 p-6 rounded-lg border text-center">
        {expression}
      </div>
    );
  };

  if (!problem) {
    return <div>Problem not found</div>;
  }

  const problemProgress = userProgress?.section1[problemId];
  const isCompleted = problemProgress?.completed || false;
  const earnedScore = problemProgress?.score || 0;

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
                {renderMathExpression(problem.question[language])}
                
                {/* Show explanation for preparation and explanation problems */}
                {problem.showFullSolution && problem.explanation && (
                  <div className="mt-6 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                    <h4 className="font-semibold mb-2 text-blue-800">
                      {text[language].explanation}
                    </h4>
                    <pre className="whitespace-pre-wrap text-sm text-blue-700">
                      {problem.explanation[language]}
                    </pre>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Answer Input - Only for non-explanation problems */}
            {!problem.showFullSolution && (
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium mb-2">
                        {text[language].yourAnswer}
                      </label>
                      <Input
                        value={userAnswer}
                        onChange={(e) => setUserAnswer(e.target.value)}
                        placeholder={text[language].placeholder}
                        className="text-lg h-12"
                        disabled={isCompleted && !isSubmitted}
                      />
                    </div>

                    {/* Encouragement Message */}
                    {showEncouragement && (
                      <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                        <p className="text-yellow-800 text-center font-medium">
                          {showEncouragement}
                        </p>
                      </div>
                    )}

                    {/* Submit/Try Again Button */}
                    <div className="flex gap-2">
                      {!isSubmitted ? (
                        <Button 
                          onClick={handleSubmit}
                          className="flex-1 h-12 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700"
                          disabled={!userAnswer.trim()}
                        >
                          {text[language].submit}
                        </Button>
                      ) : (
                        <>
                          {!isCorrect && (
                            <Button 
                              onClick={handleTryAgain}
                              className="flex-1 h-12"
                              variant="outline"
                            >
                              <RotateCcw className="w-4 h-4 mr-2" />
                              {text[language].tryAgain}
                            </Button>
                          )}
                          {isCorrect && (
                            <Button 
                              onClick={() => navigate('/dashboard')}
                              className="flex-1 h-12 bg-gradient-to-r from-green-500 to-emerald-600"
                            >
                              <Trophy className="w-4 h-4 mr-2" />
                              {text[language].backToDashboard}
                            </Button>
                          )}
                        </>
                      )}
                    </div>

                    {/* Result Display */}
                    {isSubmitted && (
                      <div className={`p-4 rounded-lg border ${
                        isCorrect 
                          ? 'bg-green-50 border-green-200 text-green-800' 
                          : 'bg-red-50 border-red-200 text-red-800'
                      }`}>
                        <div className="flex items-center">
                          {isCorrect ? (
                            <CheckCircle className="w-5 h-5 mr-2" />
                          ) : (
                            <XCircle className="w-5 h-5 mr-2" />
                          )}
                          <span className="font-medium">
                            {isCorrect ? text[language].correct : text[language].incorrect}
                          </span>
                        </div>
                        
                        {/* Show correct answer only for non-assessment problems */}
                        {!isCorrect && !problem.hideAnswer && (
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
          {problem.hints && !problem.showFullSolution && (
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
                        <span>{showHints ? currentHint + 1 : 0}/{problem.hints.length}</span>
                      </div>
                      <Progress value={(showHints ? currentHint + 1 : 0) / problem.hints.length * 100} />
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
                          {problem.hints[currentHint][language]}
                        </p>
                      </div>
                    )}

                    {/* Next Hint Button */}
                    {showHints && currentHint < problem.hints.length - 1 && (
                      <Button 
                        onClick={handleNextHint}
                        variant="outline"
                        className="w-full"
                      >
                        {text[language].nextHint}
                      </Button>
                    )}

                    {/* No More Hints Message */}
                    {showHints && currentHint === problem.hints.length - 1 && (
                      <p className="text-center text-gray-500 text-sm">
                        {problem.hideAnswer ? text[language].noMoreHints : 
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