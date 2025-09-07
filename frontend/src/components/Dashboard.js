import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, useLanguage } from '../App';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Globe, LogOut, Trophy, Star, Medal, Crown, Play, Lock, CheckCircle, XCircle, ChevronRight } from 'lucide-react';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const { language, toggleLanguage } = useLanguage();
  const navigate = useNavigate();
  const [userProgress, setUserProgress] = useState(null);
  const [userStats, setUserStats] = useState({ totalPoints: 0, badges: [] });
  const [sections, setSections] = useState([]);
  const [selectedSection, setSelectedSection] = useState('section1');
  const [loading, setLoading] = useState(true);

  const badges = [
    { id: "first_steps", name: { en: "First Steps", ar: "الخطوات الأولى" }, description: { en: "Complete your first problem", ar: "أكمل مسألتك الأولى" }, icon: "trophy" },
    { id: "practice_master", name: { en: "Practice Master", ar: "أستاذ التمرين" }, description: { en: "Complete all practice problems", ar: "أكمل جميع مسائل التدريب" }, icon: "star" },
    { id: "assessment_ace", name: { en: "Assessment Ace", ar: "بطل التقييم" }, description: { en: "Score 80+ on assessment", ar: "احصل على ٨٠+ في التقييم" }, icon: "medal" },
    { id: "inequality_expert", name: { en: "Inequality Expert", ar: "خبير المتباينات" }, description: { en: "Complete entire section", ar: "أكمل القسم بالكامل" }, icon: "crown" }
  ];

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

      // Fetch problems for section1
      const problemsResponse = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/problems/section/section1`
      );
      
      if (problemsResponse.ok) {
        const problemsData = await problemsResponse.json();
        setProblems(problemsData);
      }

    } catch (error) {
      console.error('Error fetching data:', error);
      // Fallback to empty data
      setUserProgress({
        section1: {
          prep1: { completed: false, score: 0, attempts: 0 },
          explanation1: { completed: false, score: 0, attempts: 0 },
          practice1: { completed: false, score: 0, attempts: 0 },
          practice2: { completed: false, score: 0, attempts: 0 },
          assessment1: { completed: false, score: 0, attempts: 0 },
          examprep1: { completed: false, score: 0, attempts: 0 }
        }
      });
      setProblems([]);
    } finally {
      setLoading(false);
    }
  };

  const text = {
    en: {
      welcome: "Welcome back",
      progress: "Your Progress",
      points: "Total Points",
      badges: "Badges Earned",
      section: "Section 1: One-Step Inequalities",
      problems: "Problems",
      start: "Start",
      continue: "Continue",
      completed: "Completed",
      locked: "Locked",
      attempts: "attempts",
      logout: "Logout"
    },
    ar: {
      welcome: "مرحباً بك مرة أخرى",
      progress: "تقدمك",
      points: "إجمالي النقاط",
      badges: "الشارات المكتسبة",
      section: "القسم الأول: المتباينات أحادية الخطوة",
      problems: "المسائل",
      start: "ابدأ",
      continue: "تابع",
      completed: "مكتمل",
      locked: "مقفل",
      attempts: "محاولات",
      logout: "خروج"
    }
  };

  const getProblemStatus = (problemId, progress) => {
    const problem = progress.section1[problemId];
    if (problem.completed) return 'completed';
    if (problem.attempts > 0) return 'in-progress';
    
    // Check if locked based on flexible prerequisites
    if (problemId === 'assessment1') {
      // Allow assessment after completing at least one practice problem
      const practice1Complete = progress.section1.practice1.completed;
      const practice2Complete = progress.section1.practice2.completed;
      return (practice1Complete || practice2Complete) ? 'available' : 'locked';
    }
    if (problemId === 'examprep1') {
      return progress.section1.assessment1.completed ? 'available' : 'locked';
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

  const handleProblemClick = (problemId) => {
    const status = getProblemStatus(problemId, userProgress);
    
    // Show warning for assessment if not all practice completed
    if (problemId === 'assessment1' && status === 'available') {
      const practice1Complete = userProgress.section1.practice1.completed;
      const practice2Complete = userProgress.section1.practice2.completed;
      
      if (!practice1Complete || !practice2Complete) {
        const proceed = window.confirm(
          language === 'en' 
            ? "⚠️ Recommended to complete all practice problems first. Continue anyway?"
            : "⚠️ يُنصح بإكمال جميع مسائل التدريب أولاً. هل تريد المتابعة؟"
        );
        if (!proceed) return;
      }
    }
    
    if (status !== 'locked') {
      navigate(`/problem/${problemId}`);
    }
  };

  if (!userProgress || loading) {
    return <div className="min-h-screen flex items-center justify-center">
      <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-emerald-500"></div>
    </div>;
  }

  const sectionProgress = Object.values(userProgress.section1).filter(p => p.completed).length;
  const totalProblems = Object.keys(userProgress.section1).length;
  const progressPercentage = (sectionProgress / totalProblems) * 100;

  return (
    <div className="min-h-screen p-4">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            {text[language].welcome}, {user.username}!
          </h1>
          <p className="text-gray-600">{text[language].progress}</p>
        </div>
        <div className="flex gap-2">
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
                <p className="text-purple-100">{text[language].problems}</p>
                <p className="text-3xl font-bold">{sectionProgress}/{totalProblems}</p>
              </div>
              <CheckCircle className="w-10 h-10 text-purple-200" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Progress Bar */}
      <Card className="mb-6">
        <CardContent className="p-6">
          <div className="flex justify-between items-center mb-2">
            <h3 className="font-semibold">{text[language].section}</h3>
            <span className="text-sm text-gray-500">{Math.round(progressPercentage)}%</span>
          </div>
          <Progress value={progressPercentage} className="mb-4" />
        </CardContent>
      </Card>

      {/* Problems Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        {problems.map((problem) => {
          const status = getProblemStatus(problem.id, userProgress);
          const problemProgress = userProgress.section1[problem.id];
          
          return (
            <Card 
              key={problem.id} 
              className={`cursor-pointer transition-all hover:shadow-lg ${
                status === 'locked' ? 'opacity-50 cursor-not-allowed' : 'hover:scale-105'
              }`}
              onClick={() => handleProblemClick(problem.id)}
            >
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center">
                    {status === 'completed' && <CheckCircle className="w-5 h-5 text-green-500 mr-2" />}
                    {status === 'in-progress' && <Play className="w-5 h-5 text-orange-500 mr-2" />}
                    {status === 'locked' && <Lock className="w-5 h-5 text-gray-400 mr-2" />}
                    {status === 'available' && <Play className="w-5 h-5 text-emerald-500 mr-2" />}
                    <Badge variant={
                      problem.type === 'preparation' ? 'secondary' :
                      problem.type === 'explanation' ? 'outline' :
                      problem.type === 'practice' ? 'default' :
                      problem.type === 'assessment' ? 'destructive' : 'secondary'
                    }>
                      {problem.type.charAt(0).toUpperCase() + problem.type.slice(1)}
                    </Badge>
                  </div>
                  {problemProgress.score > 0 && (
                    <span className="text-sm font-medium text-emerald-600">
                      {problemProgress.score}%
                    </span>
                  )}
                </div>
                
                <div className="text-center mb-4">
                  <div className="text-2xl font-mono bg-gray-50 p-3 rounded-lg border">
                    {language === 'en' ? problem.question_en : problem.question_ar}
                  </div>
                </div>
                
                <div className="flex justify-between items-center text-sm text-gray-500">
                  <span>
                    {status === 'completed' ? text[language].completed :
                     status === 'in-progress' ? text[language].continue :
                     status === 'locked' ? text[language].locked :
                     text[language].start}
                  </span>
                  {problemProgress.attempts > 0 && (
                    <span>{problemProgress.attempts} {text[language].attempts}</span>
                  )}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

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
    </div>
  );
};

export default Dashboard;