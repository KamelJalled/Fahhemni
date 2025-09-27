import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, useLanguage } from '../App';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Globe, LogOut, Trophy, Star, Medal, Crown, Play, Lock, CheckCircle, XCircle, ChevronRight, RotateCcw, BookOpen, HelpCircle } from 'lucide-react';
import RulesModal from './RulesModal';

const Dashboard = () => { // <--- Component starts HERE

  // --- 1. ALL STATE AND VARIABLES ---
  const { user, logout } = useAuth();
  const { language, toggleLanguage } = useLanguage();
  const navigate = useNavigate();
  const [userProgress, setUserProgress] = useState(null);
  const [userStats, setUserStats] = useState({ totalPoints: 0, badges: [] });
  const [sections, setSections] = useState([]);
  const [selectedSection, setSelectedSection] = useState('section1');
  const [loading, setLoading] = useState(true);
  const [showRulesModal, setShowRulesModal] = useState(false);

  const sections_info = [
    { id: 'section1', title_en: 'Section 1: Solving Inequalities by Addition or Subtraction', title_ar: 'القسم الأول: حل المتباينات بالجمع أو بالطرح' },
    { id: 'section2', title_en: 'Section 2: Solving Inequalities by Multiplication or Division', title_ar: 'القسم الثاني: حل المتباينات بالضرب أو بالقسمة' },
    { id: 'section3', title_en: 'Section 3: Solving Multi-Step Inequalities', title_ar: 'القسم الثالث: حل المتباينات المتعددة الخطوات' },
    { id: 'section4', title_en: 'Section 4: Solving Compound Inequalities', title_ar: 'القسم الرابع: حل المتباينات المركبة' },
    { id: 'section5', title_en: 'Section 5: Solving Inequalities Involving Absolute Value', title_ar: 'القسم الخامس: حل المتباينات التي تتضمن القيمة المطلقة' }
  ];

  const badges = [
    { id: "first_steps", name: { en: "First Steps", ar: "الخطوات الأولى" }, description: { en: "Complete your first problem", ar: "أكمل مسألتك الأولى" }, icon: "trophy" },
    { id: "practice_master", name: { en: "Practice Master", ar: "أستاذ التمرين" }, description: { en: "Complete all practice problems", ar: "أكمل جميع مسائل التدريب" }, icon: "star" },
    { id: "assessment_ace", name: { en: "Assessment Ace", ar: "بطل التقييم" }, description: { en: "Score 80+ on assessment", ar: "احصل على ٨٠+ في التقييم" }, icon: "medal" },
    { id: "inequality_expert", name: { en: "Inequality Expert", ar: "خبير المتباينات" }, description: { en: "Complete entire section", ar: "أكمل القسم بالكامل" }, icon: "crown" }
  ];

  const text = {
    en: {
      welcome: "Welcome back",
      progress: "Your Progress",
      points: "Total Points",
      badges: "Badges Earned",
      sections: "Sections",
      problems: "Problems",
      start: "Start",
      continue: "Continue",
      completed: "Completed",
      locked: "Locked",
      attempts: "attempts",
      logout: "Logout",
      preparation: "Preparation",
      explanation: "Explanation",
      practice: "Practice",
      assessment: "Assessment",
      examprep: "Exam Prep"
    },
    ar: {
      welcome: "مرحباً بك مرة أخرى",
      progress: "تقدمك",
      points: "إجمالي النقاط",
      badges: "الشارات المكتسبة",
      sections: "الأقسام",
      problems: "المسائل",
      start: "ابدأ",
      continue: "تابع",
      completed: "مكتمل",
      locked: "مقفل",
      attempts: "محاولات",
      logout: "خروج",
      preparation: "التحضير",
      explanation: "الشرح",
      practice: "التدريب",
      assessment: "التقييم",
      examprep: "الإعداد للاختبار"
    }
  };

  // --- 2. HELPER FUNCTIONS ---
  const fetchData = async () => {
    try {
      setLoading(true);

      const progressResponse = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/students/${user.username}/progress`
      );
      
      if (progressResponse.ok) {
        const progressData = await progressResponse.json();
        setUserProgress(progressData.progress);
        setUserStats({
          totalPoints: progressData.total_points,
          badges: progressData.badges
        });
      }

      const sectionsWithProblems = [];
      for (const section of sections_info) {
        try {
          const problemsResponse = await fetch(
            `${process.env.REACT_APP_BACKEND_URL}/api/problems/section/${section.id}`
          );
          
          if (problemsResponse.ok) {
            const problemsData = await problemsResponse.json();
            sectionsWithProblems.push({
              ...section,
              problems: problemsData
            });
          } else {
            sectionsWithProblems.push({
              ...section,
              problems: []
            });
          }
        } catch (sectionError) {
          console.error(`Error fetching ${section.id}:`, sectionError);
          sectionsWithProblems.push({
            ...section,
            problems: []
          });
        }
      }
      
      setSections(sectionsWithProblems);

    } catch (error) {
      console.error('Error fetching data:', error);
      setSections(sections_info.map(s => ({ ...s, problems: [] })));
    } finally {
      setLoading(false);
    }
  };

  const calculateOverallProgress = () => {
    let totalCompleted = 0;
    let totalProblems = 0;
    
    sections.forEach(section => {
      if (userProgress && userProgress[section.id]) {
        const sectionCompleted = Object.values(userProgress[section.id]).filter(p => p.completed).length;
        const sectionTotal = Object.keys(userProgress[section.id]).length;
        totalCompleted += sectionCompleted;
        totalProblems += sectionTotal;
      }
    });
    
    return totalProblems > 0 ? (totalCompleted / totalProblems) * 100 : 0;
  };

  const calculateSectionProgress = (sectionId) => {
    if (!userProgress || !userProgress[sectionId]) return 0;
    const sectionCompleted = Object.values(userProgress[sectionId]).filter(p => p.completed).length;
    const sectionTotal = Object.keys(userProgress[sectionId]).length;
    return sectionTotal > 0 ? (sectionCompleted / sectionTotal) * 100 : 0;
  };

  const getProblemType = (problemId) => {
    if (problemId.includes('prep') && !problemId.includes('examprep')) return 'preparation';
    if (problemId.includes('explanation')) return 'explanation';
    if (problemId.includes('practice')) return 'practice';
    if (problemId.includes('assessment')) return 'assessment';
    if (problemId.includes('examprep')) return 'examprep';
    return 'unknown';
  };

  const checkStageAccess = (sectionId, problemId, userProgress) => {
    if (!problemId || !sectionId || !userProgress || !userProgress[sectionId]) {
      return { access: true };
    }
    
    const sectionProgress = userProgress[sectionId];
    const problemType = getProblemType(problemId);
    
    if (problemType === 'assessment' || problemType === 'examprep') {
      const practiceProblems = Object.keys(sectionProgress).filter(id => 
        id.includes('practice')
      );
      
      if (practiceProblems.length > 0) {
        const allPracticeComplete = practiceProblems.every(practiceId => 
          sectionProgress[practiceId]?.completed === true
        );
        
        if (!allPracticeComplete) {
          const incompletePractice = practiceProblems.filter(practiceId => 
            !sectionProgress[practiceId]?.completed
          );
          
          return {
            access: false,
            message: language === 'en' 
              ? `You must complete all practice stages first. Incomplete: ${incompletePractice.join(', ')}`
              : `يجب إكمال جميع مراحل التدريب أولاً. غير مكتمل: ${incompletePractice.join(', ')}`,
            showLockedIcon: true,
            lockedReason: 'practice_incomplete'
          };
        }
      }
    }
    
    if (problemType === 'examprep') {
      const assessmentId = `assessment${sectionId.slice(-1)}`;
      const assessmentComplete = sectionProgress[assessmentId]?.completed === true;
      
      if (!assessmentComplete) {
        return {
          access: false,
          message: language === 'en' 
            ? 'You must complete the Assessment stage first'
            : 'يجب إكمال مرحلة التقييم أولاً',
          showLockedIcon: true,
          lockedReason: 'assessment_incomplete'
        };
      }
    }
    
    return { access: true };
  };

  const getProblemStatus = (problemId, sectionId, progress) => {
    if (!progress || !progress[sectionId] || !progress[sectionId][problemId]) {
      return 'available';
    }
    
    const problem = progress[sectionId][problemId];
    if (problem.completed) return 'completed';
    if (problem.attempts > 0) return 'in-progress';
    
    const assessmentId = `assessment${sectionId.slice(-1)}`;
    const examPrepId = `examprep${sectionId.slice(-1)}`;
    
    if (problemId === assessmentId) {
      const practiceProblems = Object.keys(progress[sectionId]).filter(id => id.includes('practice'));
      const hasPracticeComplete = practiceProblems.some(practiceId => progress[sectionId][practiceId]?.completed);
      return hasPracticeComplete ? 'available' : 'locked';
    }
    if (problemId === examPrepId) {
      return progress[sectionId][assessmentId]?.completed ? 'available' : 'locked';
    }
    
    return 'available';
  };

  const getBadgeIcon = (badgeId) => {
    const iconMap = {
      trophy: Trophy,
      star: Star,
      medal: Medal,
      crown: Crown
    };
    const badge = badges.find(b => b.id === badgeId);
    const IconComponent = iconMap[badge?.icon] || Trophy;
    return <IconComponent className="w-5 h-5" />;
  };

  const handleProblemClick = (problemId, sectionId) => {
    const accessControl = checkStageAccess(sectionId, problemId, userProgress);
    
    if (!accessControl.access) {
      alert(`🔒 ${accessControl.message}`);
      return;
    }
    
    localStorage.setItem('lastSection', sectionId);
    localStorage.setItem('lastProblem', problemId);
    
    window.location.href = `/section/${sectionId}/problem/${problemId}`;
  };

  // --- 3. useEffect HOOKS ---
  useEffect(() => {
    if (!user) {
      navigate('/');
      return;
    }
    fetchData();
  }, [user, navigate]);

  useEffect(() => {
    const lastSection = localStorage.getItem('lastSection');
    if (lastSection) {
      setSelectedSection(lastSection);
      localStorage.removeItem('lastSection');
      localStorage.removeItem('lastProblem');
    }
  }, []);

  // --- 4. RENDER LOGIC ---
  if (!userProgress || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-emerald-500"></div>
      </div>
    );
  }

  const overallProgressPercentage = calculateOverallProgress();
  const selectedSectionData = sections.find(s => s.id === selectedSection);
  const selectedSectionProgress = calculateSectionProgress(selectedSection);

  return (
    <div className="min-h-screen p-4 overflow-x-hidden">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
        <div className="flex-1 min-w-0">
          <h1 className="text-xl sm:text-2xl font-bold text-gray-800 truncate">
            {text[language].welcome}, {user.username}!
          </h1>
          <p className="text-gray-600 text-sm sm:text-base">{text[language].progress}</p>
        </div>
        
        <div className="flex gap-2">
          <Button onClick={() => setShowRulesModal(true)} variant="outline" size="sm">
            <BookOpen className="w-4 h-4 mr-2" />
            {language === 'en' ? 'Rules' : 'قواعد'}
          </Button>
          <Button onClick={toggleLanguage} variant="outline" size="sm">
            <Globe className="w-4 h-4 mr-2" />
            {language === 'en' ? 'العربية' : 'English'}
          </Button>
          <Button onClick={logout} variant="outline" size="sm">
            <LogOut className="w-4 h-4 mr-2" />
            {text[language].logout}
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Card className="bg-gradient-to-br from-emerald-500 to-teal-600 text-white">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-emerald-100">{text[language].points}</p>
                <p className="text-3xl font-bold">{userStats.totalPoints}</p>
              </div>
              <Trophy className="w-10 h-10 text-emerald-200" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-orange-500 to-red-600 text-white">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-orange-100">{text[language].badges}</p>
                <p className="text-3xl font-bold">{userStats.badges.length}/4</p>
              </div>
              <Star className="w-10 h-10 text-orange-200" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-500 to-pink-600 text-white">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-100">{text[language].progress}</p>
                <p className="text-3xl font-bold">{Math.round(overallProgressPercentage)}%</p>
              </div>
              <CheckCircle className="w-10 h-10 text-purple-200" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Sections Navigation */}
      <Card className="mb-6">
        <CardContent className="p-6">
          <h3 className="font-semibold mb-4 text-center">{text[language].sections}</h3>
           {/* Mobile: Simple Dropdown Menu */}
           <div className="block md:hidden mb-4">
             <select
               value={selectedSection}
               onChange={(e) => updateSelectedSection(e.target.value)}
               className="w-full p-3 border border-gray-300 rounded-lg bg-white shadow-sm text-sm"
             >
              {sections.map((section) => {
               const sectionInfo = sections_info.find(s => s.id === section.id);
               return (
                <option key={section.id} value={section.id}>
                {sectionInfo ? (language === 'en' ? sectionInfo.title_en : sectionInfo.title_ar) : section.id}
                </option>
              );
           })}
             </select>
           </div>
          <div className="grid grid-cols-5 gap-2">
            {sections.map((section) => {
              const sectionProgress = calculateSectionProgress(section.id);
              const isSelected = selectedSection === section.id;
              const hasProblems = section.problems && section.problems.length > 0;
              
              return (
                <Button
                  key={section.id}
                  variant={isSelected ? "default" : "outline"}
                  className={`${!hasProblems ? 'opacity-50' : ''}`}
                  onClick={() => setSelectedSection(section.id)}
                  disabled={!hasProblems}
                >
                  <div className="text-center">
                    <div className="text-xs">
                      {language === 'en' ? section.title_en : section.title_ar}
                    </div>
                    <div className="text-xs opacity-75 mt-1">
                      {Math.round(sectionProgress)}% {text[language].completed}
                    </div>
                  </div>
                </Button>
              );
            })}
          </div>
          
          {selectedSectionData && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="flex justify-between items-center mb-2">
                <h4 className="font-semibold text-gray-700">
                  {language === 'en' ? 'Current Section Progress' : 'تقدم القسم الحالي'}
                </h4>
                <span className="text-sm font-medium text-blue-600">{Math.round(selectedSectionProgress)}%</span>
              </div>
              <Progress value={selectedSectionProgress} className="h-2" />
            </div>
          )}
        </CardContent>
      </Card>

      {/* Problems Grid */}
      {selectedSectionData && selectedSectionData.problems && selectedSectionData.problems.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
          {selectedSectionData.problems.map((problem) => {
            const accessControl = checkStageAccess(selectedSection, problem.id, userProgress);
            const status = getProblemStatus(problem.id, selectedSection, userProgress);
            const problemProgress = userProgress[selectedSection]?.[problem.id] || { completed: false, score: 0, attempts: 0 };
            const effectiveStatus = !accessControl.access ? 'locked' : status;
            const isAccessDenied = !accessControl.access;
            
            return (
              <Card 
                key={`${selectedSection}-${problem.id}`} 
                className={`cursor-pointer transition-all hover:shadow-lg ${
                  effectiveStatus === 'locked' || isAccessDenied ? 'opacity-50 cursor-not-allowed bg-gray-100' : 'hover:scale-105'
                }`}
                onClick={() => handleProblemClick(problem.id, selectedSection)}
              >
                  <Button
                    onClick={() => {
                     if (window.confirm(language === 'en' ?
                      'Are you sure you want to start over? This will reset all your progress.' :
                      'هل أنت متأكد من أنك تريد البدء من جديد؟ سيؤدي هذا إلى إعادة تعيين كل تقدمك.'
                      )) {
                        localStorage.removeItem('mathapp_progress');
                        window.location.href = '/dashboard';
                       }
                    }}
                    variant="outline"
                    size="sm"
                    className="text-orange-600 border-orange-300 hover:bg-orange-50"
                  >
                  <RotateCcw className="w-4 h-4 mr-2" />
                  {language === 'en' ? 'Start Over' : 'ابدأ من جديد'}
                  </Button>
                
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center">
                      {effectiveStatus === 'completed' && <CheckCircle className="w-5 h-5 text-green-500 mr-2" />}
                      {effectiveStatus === 'in-progress' && <Play className="w-5 h-5 text-orange-500 mr-2" />}
                      {(effectiveStatus === 'locked' || isAccessDenied) && <Lock className="w-5 h-5 text-red-500 mr-2" />}
                      {effectiveStatus === 'available' && !isAccessDenied && <Play className="w-5 h-5 text-emerald-500 mr-2" />}
                      <Badge variant={
                        problem.type === 'preparation' ? 'secondary' :
                        problem.type === 'explanation' ? 'outline' :
                        problem.type === 'practice' ? 'default' :
                        problem.type === 'assessment' ? 'destructive' : 
                        'secondary'
                      }>
                        {text[language][problem.type] || problem.type}
                        {isAccessDenied && ' 🔒'}
                      </Badge>
                    </div>
                    {problemProgress.score > 0 && !isAccessDenied && (
                      <span className="text-sm font-medium text-emerald-600">
                        {problemProgress.score}%
                      </span>
                    )}
                  </div>
                  
                  <div className="text-center mb-4">
                    <div className={`text-2xl font-mono p-3 rounded-lg border ${
                      isAccessDenied ? 'bg-gray-200 text-gray-500' : 'bg-gray-50'
                    }`}>
                      {isAccessDenied ? '🔒 Locked' : (language === 'en' ? problem.question_en : problem.question_ar)}
                    </div>
                  </div>
                  
                  {isAccessDenied && (
                    <div className="mb-3 p-2 bg-red-50 border border-red-200 rounded text-sm text-red-700 text-center">
                      {accessControl.message}
                    </div>
                  )}
                  
                  <div className="flex justify-between items-center text-sm text-gray-500">
                    <span>
                      {effectiveStatus === 'completed' ? text[language].completed :
                       effectiveStatus === 'in-progress' ? text[language].continue :
                       effectiveStatus === 'locked' || isAccessDenied ? text[language].locked :
                       text[language].start}
                    </span>
                    {problemProgress.attempts > 0 && !isAccessDenied && (
                      <span>{problemProgress.attempts} {text[language].attempts}</span>
                    )}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      ) : (
        <Card className="mb-6">
          <CardContent className="p-6 text-center">
            <p className="text-gray-500">
              {language === 'en' 
                ? `No problems available for ${selectedSectionData?.title_en || selectedSection} yet.` 
                : `لا توجد مسائل متاحة لـ ${selectedSectionData?.title_ar || selectedSection} بعد.`}
            </p>
          </CardContent>
        </Card>
      )}

      {/* Badges Section */}
      {userStats.badges.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>{text[language].badges}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {userStats.badges.map((badgeId) => {
                const badge = badges.find(b => b.id === badgeId);
                if (!badge) return null;
                return (
                  <div key={badgeId} className="text-center p-4 bg-gradient-to-br from-yellow-100 to-orange-100 rounded-lg">
                    <div className="flex justify-center mb-2 text-yellow-600">
                      {getBadgeIcon(badgeId)}
                    </div>
                    <h4 className="font-semibold text-sm">{badge.name[language]}</h4>
                    <p className="text-xs text-gray-600 mt-1">{badge.description[language]}</p>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}

      <RulesModal 
        isOpen={showRulesModal} 
        onClose={() => setShowRulesModal(false)} 
      />
    </div>
  );
}; // <--- Component ends HERE

export default Dashboard;