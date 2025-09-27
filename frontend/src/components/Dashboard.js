import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, useLanguage } from '../App';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Globe, LogOut, Trophy, Star, Medal, Crown, Play, Lock, CheckCircle, XCircle, ChevronRight, RotateCcw, BookOpen, HelpCircle } from 'lucide-react';
import RulesModal from './RulesModal';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const { language, toggleLanguage } = useLanguage();
  const navigate = useNavigate();
  const [userProgress, setUserProgress] = useState(null);
  const [userStats, setUserStats] = useState({ totalPoints: 0, badges: [] });
  const [sections, setSections] = useState([]);
  const [selectedSection, setSelectedSection] = useState(() => {
    // NAVIGATION CONTEXT FIX: Preserve current section from localStorage or URL
    const savedContext = localStorage.getItem('mathapp_navigation_context');
    if (savedContext) {
      try {
        const context = JSON.parse(savedContext);
        // Only use saved context if it's recent (within 1 hour)
        if (Date.now() - context.timestamp < 3600000) {
          return context.section || 'section1';
        }
      } catch (e) {
        console.log('Error parsing navigation context:', e);
      }
    }
    return 'section1'; // Default
  });
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

  // NAVIGATION CONTEXT FIX: Helper to save navigation context
  const saveNavigationContext = (section, stage = null) => {
    const context = {
      section: section,
      stage: stage,
      timestamp: Date.now()
    };
    localStorage.setItem('mathapp_navigation_context', JSON.stringify(context));
  };

  // Update selected section and save context
  const updateSelectedSection = (sectionId) => {
    setSelectedSection(sectionId);
    saveNavigationContext(sectionId);
  };

  useEffect(() => {
    if (!user) {
      navigate('/');
      return;
    }

    fetchData();
  }, [user, navigate]);

  const fetchData = async () => {
    try {
      setLoading(true);

      // Fetch student progress
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

      // Fetch problems for all sections
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
            // Section doesn't exist, add empty problems
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
      // Fallback to empty data for all sections
      setUserProgress({
        section1: {
          prep1: { completed: false, score: 0, attempts: 0 },
          explanation1: { completed: false, score: 0, attempts: 0 },
          practice1_1: { completed: false, score: 0, attempts: 0 },
          practice1_2: { completed: false, score: 0, attempts: 0 },
          assessment1: { completed: false, score: 0, attempts: 0 },
          examprep1: { completed: false, score: 0, attempts: 0 }
        }
      });
      setSections(sections_info.map(s => ({ ...s, problems: [] })));
    } finally {
      setLoading(false);
    }
  };

  // Add this to Dashboard.js after the state declarations:

useEffect(() => {
    // Check if we're returning from a problem view
    const lastSection = localStorage.getItem('lastSection');
    const lastProblem = localStorage.getItem('lastProblem');
    
    if (lastSection) {
        // Set the current section to the last visited
        setCurrentSection(lastSection);
        
        // Clear the stored values
        localStorage.removeItem('lastSection');
        localStorage.removeItem('lastProblem');
    }
}, []);

// Fix the handleProblemClick function:
const handleProblemClick = (problemId) => {
    // Store current context
    localStorage.setItem('currentSection', currentSection);
    localStorage.setItem('currentProblem', problemId);
    
    // Navigate with full URL
    window.location.href = `/section/${currentSection}/problem/${problemId}`;
};

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
      // Problem type labels
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
      // Problem type labels - FIXED LOCALIZATION
      preparation: "التحضير",
      explanation: "الشرح",
      practice: "التدريب",
      assessment: "التقييم",
      examprep: "الإعداد للاختبار"
    }
  };

  // CRITICAL: Stage access control to prevent cheating
  const checkStageAccess = (sectionId, problemId, userProgress) => {
    if (!problemId || !sectionId || !userProgress || !userProgress[sectionId]) {
      return { access: true }; // Allow if no progress data
    }
    
    const sectionProgress = userProgress[sectionId];
    const problemType = getProblemType(problemId);
    
    // SECURITY: Lock Assessment and Exam Prep stages until ALL practice stages are completed
    if (problemType === 'assessment' || problemType === 'examprep') {
      // Get all practice problems for this section
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
    
    // SECURITY: Lock Exam Prep until Assessment is completed
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

  // Helper function to determine problem type from ID
  const getProblemType = (problemId) => {
    if (problemId.includes('prep') && !problemId.includes('examprep')) return 'preparation';
    if (problemId.includes('explanation')) return 'explanation';
    if (problemId.includes('practice')) return 'practice';
    if (problemId.includes('assessment')) return 'assessment';
    if (problemId.includes('examprep')) return 'examprep';
    return 'unknown';
  };

  const getProblemStatus = (problemId, sectionId, progress) => {
    if (!progress || !progress[sectionId] || !progress[sectionId][problemId]) {
      return 'available';
    }
    
    const problem = progress[sectionId][problemId];
    if (problem.completed) return 'completed';
    if (problem.attempts > 0) return 'in-progress';
    
    // Check if locked based on flexible prerequisites
    const assessmentId = `assessment${sectionId.slice(-1)}`;
    const examPrepId = `examprep${sectionId.slice(-1)}`;
    
    if (problemId === assessmentId) {
      // Allow assessment after completing at least one practice problem
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

     const status = getProblemStatus(problemId, sectionId, userProgress);
    
    // Show warning for assessment if not all practice completed (redundant check for safety)
    const assessmentId = `assessment${sectionId.slice(-1)}`;
    if (problemId === assessmentId && status === 'available') {
      const practiceProblems = Object.keys(userProgress[sectionId] || {}).filter(id => id.includes('practice'));
      const allPracticeComplete = practiceProblems.every(practiceId => userProgress[sectionId][practiceId]?.completed);
      
      if (!allPracticeComplete) {
        const proceed = window.confirm(
          language === 'en' 
            ? "⚠️ Recommended to complete all practice problems first. Continue anyway?"
            : "⚠️ يُنصح بإكمال جميع مسائل التدريب أولاً. هل تريد المتابعة؟"
        );
        if (!proceed) return;
      }
    }
    
    // Only navigate if access is allowed
    if (status !== 'locked') {
      const targetUrl = `/problem/${problemId}`;
      console.log(`🚀 DASHBOARD NAVIGATION: Navigating to ${targetUrl}`);
      
      // Try React Router navigate first
      try {
        navigate(targetUrl);
        
        // Force navigation if React Router doesn't work
        setTimeout(() => {
          if (window.location.pathname !== targetUrl) {
            console.log(`🔄 React Router navigation failed, forcing with window.location`);
            window.location.href = targetUrl;
          }
        }, 100);
        
      } catch (error) {
        console.error('Dashboard navigation error:', error);
        // Fallback: Force navigation with window.location
        window.location.href = targetUrl;
      }
    }
  };

  if (!userProgress || loading) {
      return <div className="min-h-screen flex items-center justify-center">
      <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-emerald-500"></div>
      </div>;
  }

  // Calculate overall progress across all sections
  const calculateOverallProgress = () => {
    let totalCompleted = 0;
    let totalProblems = 0;
    
    sections.forEach(section => {
      if (userProgress[section.id]) {
        const sectionCompleted = Object.values(userProgress[section.id]).filter(p => p.completed).length;
        const sectionTotal = Object.keys(userProgress[section.id]).length;
        totalCompleted += sectionCompleted;
        totalProblems += sectionTotal;
      }
    });
    
    return totalProblems > 0 ? (totalCompleted / totalProblems) * 100 : 0;
  };

  const calculateSectionProgress = (sectionId) => {
    if (!userProgress[sectionId]) return 0;
    const sectionCompleted = Object.values(userProgress[sectionId]).filter(p => p.completed).length;
    const sectionTotal = Object.keys(userProgress[sectionId]).length;
    return sectionTotal > 0 ? (sectionCompleted / sectionTotal) * 100 : 0;
  };

  const overallProgressPercentage = calculateOverallProgress();
  const selectedSectionData = sections.find(s => s.id === selectedSection);
  const selectedSectionProgress = calculateSectionProgress(selectedSection);
  
  // Debug section switching
  console.log(`Dashboard rendering - selectedSection: ${selectedSection}, selectedSectionData:`, selectedSectionData?.id, selectedSectionData?.problems?.length);

  return (
    <div className="min-h-screen p-4 overflow-x-hidden">
      {/* Header - Mobile Responsive */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
        <div className="flex-1 min-w-0">
          <h1 className="text-xl sm:text-2xl font-bold text-gray-800 truncate">
            {text[language].welcome}, {user.username}!
          </h1>
          <p className="text-gray-600 text-sm sm:text-base">{text[language].progress}</p>
        </div>
        
        {/* Mobile: Stacked buttons */}
        <div className="flex flex-col sm:hidden gap-2 w-full">
          <div className="flex gap-2">
            <Button 
              onClick={() => setShowRulesModal(true)}
              variant="outline" 
              size="sm"
              className="text-blue-600 border-blue-300 hover:bg-blue-50 flex-1"
            >
              <BookOpen className="w-4 h-4 mr-1" />
              <span className="text-xs">{language === 'en' ? 'Rules' : 'قواعد'}</span>
            </Button>
            <Button 
              onClick={() => {
                // Reset to beginning - clear progress and refresh
                if (window.confirm(language === 'en' ? 
                  'Start over? This will reset all progress.' : 
                  'البدء من جديد؟ سيتم حذف كل التقدم.'
                )) {
                  localStorage.removeItem('mathapp_progress');
                  window.location.href = '/dashboard';
                }
              }} 
              variant="outline" 
              size="sm"
              className="text-orange-600 border-orange-300 hover:bg-orange-50 flex-1"
            >
              <RotateCcw className="w-4 h-4 mr-1" />
              <span className="text-xs">{language === 'en' ? 'Reset' : 'إعادة'}</span>
            </Button>
          </div>
          <div className="flex gap-2">
            <Button onClick={toggleLanguage} variant="outline" size="sm" className="flex-1">
              <Globe className="w-4 h-4 mr-1" />
              <span className="text-xs">{language === 'en' ? 'العربية' : 'English'}</span>
            </Button>
            <Button onClick={logout} variant="outline" size="sm" className="flex-1">
              <LogOut className="w-4 h-4 mr-1" />
              <span className="text-xs">{text[language].logout}</span>
            </Button>
          </div>
        </div>
        
        {/* Desktop: Horizontal buttons */}
        <div className="hidden sm:flex gap-2 flex-shrink-0">
          <Button 
            onClick={() => setShowRulesModal(true)}
            variant="outline" 
            size="sm"
            className="text-blue-600 border-blue-300 hover:bg-blue-50"
          >
            <BookOpen className="w-4 h-4 mr-2" />
            {language === 'en' ? 'Solving Rules' : 'قواعد الحل'}
          </Button>
          <Button 
            onClick={() => {
              // Reset to beginning - clear progress and refresh
              if (window.confirm(language === 'en' ? 
                'Are you sure you want to start over? This will reset all your progress.' : 
                'هل أنت متأكد من أنك تريد البدء من جديد؟ سيؤدي هذا إلى إعادة تعيين كل تقدمك.'
              )) {
                // Clear progress but keep user logged in
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

      {/* Sections Navigation - Mobile Optimized */}
      <Card className="mb-6">
        <CardContent className="p-6">
          <h3 className="font-semibold mb-4 text-center">{text[language].sections}</h3>
          
          {/* Mobile: Simple Dropdown Menu */}
          <div className="block md:hidden mb-4">
            <select 
              value={selectedSection} 
              onChange={(e) => {
                console.log(`Mobile dropdown: Switching to section: ${e.target.value}`);
                updateSelectedSection(e.target.value);
              }}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white shadow-sm text-sm"
            >
              {sections.map((section) => {
                const sectionInfo = sections_info.find(s => s.id === section.id);
                const hasProblems = section.problems && section.problems.length > 0;
                return (
                  <option 
                    key={section.id} 
                    value={section.id}
                    disabled={!hasProblems}
                  >
                    {sectionInfo ? (language === 'en' ? sectionInfo.title_en : sectionInfo.title_ar) : section.id}
                  </option>
                );
              })}
            </select>
          </div>
          
          {/* Desktop: Horizontal Tabs */}
          <div className="hidden md:block">
            <div className="grid grid-cols-5 gap-2">
              {sections.map((section) => {
                const sectionProgress = calculateSectionProgress(section.id);
                const isSelected = selectedSection === section.id;
                const hasProblems = section.problems && section.problems.length > 0;
                
                return (
                  <Button
                    key={section.id}
                    variant={isSelected ? "default" : "outline"}
                    className={`section-tab-button ${
                      !hasProblems ? 'opacity-50' : ''
                    } ${isSelected ? 'bg-blue-600 text-white shadow-lg' : 'hover:bg-gray-50'}`}
                    onClick={() => {
                      console.log(`Desktop tabs: Switching to section: ${section.id}`);
                      updateSelectedSection(section.id);
                    }}
                    disabled={!hasProblems}
                    style={{
                      height: '100px',
                      padding: '8px',
                      whiteSpace: 'normal',
                      wordWrap: 'break-word',
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'center',
                      alignItems: 'center',
                      textAlign: 'center'
                    }}
                  >
                    <div style={{ width: '100%', textAlign: 'center' }}>
                      <div 
                        className={`${language === 'ar' ? 'arabic-section-title' : 'english-section-title'}`}
                        style={{
                          fontWeight: '500',
                          marginBottom: '4px',
                          lineHeight: language === 'ar' ? '1.4' : '1.2',
                          maxHeight: language === 'ar' ? '65px' : '55px',
                          overflow: 'hidden',
                          wordBreak: 'break-word',
                          overflowWrap: 'break-word',
                          hyphens: 'auto',
                          display: '-webkit-box',
                          WebkitLineClamp: 4,
                          WebkitBoxOrient: 'vertical',
                          textOverflow: 'ellipsis'
                        }}
                      >
                        {language === 'en' ? section.title_en : section.title_ar}
                      </div>
                      <div className="text-xs opacity-75">
                        {Math.round(sectionProgress)}% {text[language].completed}
                      </div>
                      {isSelected && (
                        <div className="w-full h-0.5 bg-white mt-1 rounded"></div>
                      )}
                    </div>
                  </Button>
                );
              })}
            </div>
          </div>
          
          {/* Selected Section Info - Integrated without duplication */}
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

      {/* Problems Grid - Enhanced Section Isolation */}
      {selectedSectionData && selectedSectionData.problems && selectedSectionData.problems.length > 0 ? (
        <div key={`section-problems-${selectedSection}`} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6 transition-all duration-300">
          {selectedSectionData.problems
            .filter(problem => problem && problem.id) // Ensure valid problems
            .map((problem) => {
            // CRITICAL: Check access control for each problem
            const accessControl = checkStageAccess(selectedSection, problem.id, userProgress);
            const status = getProblemStatus(problem.id, selectedSection, userProgress);
            const problemProgress = userProgress[selectedSection]?.[problem.id] || { completed: false, score: 0, attempts: 0 };
            
            // Override status if access is denied
            const effectiveStatus = !accessControl.access ? 'locked' : status;
            const isAccessDenied = !accessControl.access;
            
            console.log(`Rendering problem ${problem.id} from section ${selectedSection}, access: ${accessControl.access}`);
            
            return (
              <Card 
                key={`${selectedSection}-${problem.id}-${problem.type || 'problem'}`} 
                className={`cursor-pointer transition-all hover:shadow-lg ${
                  effectiveStatus === 'locked' || isAccessDenied ? 'opacity-50 cursor-not-allowed bg-gray-100' : 'hover:scale-105'
                } ${isAccessDenied ? 'border-2 border-red-200' : ''}`}
                onClick={() => handleProblemClick(problem.id, selectedSection)}
              >
                <CardContent className="p-6 problem-text">
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
                        problem.type === 'assessment' ? (isAccessDenied ? 'destructive' : 'destructive') : 
                        problem.type === 'examprep' ? (isAccessDenied ? 'destructive' : 'secondary') : 'secondary'
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
                  
                  {/* SECURITY: Show access denied reason */}
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
        <Card key={`empty-${selectedSection}`} className="mb-6">
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

      {/* Rules Modal */}
      <RulesModal 
        isOpen={showRulesModal} 
        onClose={() => setShowRulesModal(false)} 
      />
    </div>
  );
};

export default Dashboard;