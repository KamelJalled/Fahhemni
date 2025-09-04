import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, useLanguage } from '../App';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Globe, LogOut, Trophy, Star, Medal, Crown, Play, Lock, CheckCircle, XCircle } from 'lucide-react';
import { mockProblems, mockUsers, badges } from '../mock';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const { language, toggleLanguage } = useLanguage();
  const navigate = useNavigate();
  const [userProgress, setUserProgress] = useState(null);
  const [userStats, setUserStats] = useState({ totalPoints: 0, badges: [] });

  useEffect(() => {
    if (!user) {
      navigate('/');
      return;
    }

    // Load user progress from localStorage
    const savedProgress = localStorage.getItem(`mathapp_progress_${user.username}`);
    if (savedProgress) {
      const progress = JSON.parse(savedProgress);
      setUserProgress(progress);
      calculateStats(progress);
    } else {
      // Initialize empty progress
      const initialProgress = {
        section1: {
          prep1: { completed: false, score: 0, attempts: 0 },
          explanation1: { completed: false, score: 0, attempts: 0 },
          practice1: { completed: false, score: 0, attempts: 0 },
          practice2: { completed: false, score: 0, attempts: 0 },
          assessment1: { completed: false, score: 0, attempts: 0 },
          examprep1: { completed: false, score: 0, attempts: 0 }
        }
      };
      setUserProgress(initialProgress);
      localStorage.setItem(`mathapp_progress_${user.username}`, JSON.stringify(initialProgress));
    }
  }, [user, navigate]);

  const calculateStats = (progress) => {
    let totalPoints = 0;
    let earnedBadges = [];
    const section1 = progress.section1;

    // Calculate points based on weighted scoring
    Object.keys(section1).forEach(problemId => {
      const problemProgress = section1[problemId];
      const problem = mockProblems.section1.problems.find(p => p.id === problemId);
      if (problem && problemProgress.completed) {
        totalPoints += (problemProgress.score * problem.weight) / 100;
      }
    });

    // Check badges
    if (Object.values(section1).some(p => p.completed)) {
      earnedBadges.push('first_steps');
    }
    if (section1.practice1.completed && section1.practice2.completed) {
      earnedBadges.push('practice_master');
    }
    if (section1.assessment1.completed && section1.assessment1.score >= 80) {
      earnedBadges.push('assessment_ace');
    }
    if (Object.values(section1).every(p => p.completed)) {
      earnedBadges.push('inequality_expert');
    }

    setUserStats({ totalPoints: Math.round(totalPoints), badges: earnedBadges });
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
    
    // Check if locked based on prerequisites
    if (problemId === 'assessment1') {
      const practiceComplete = progress.section1.practice1.completed && progress.section1.practice2.completed;
      return practiceComplete ? 'available' : 'locked';
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
    if (status !== 'locked') {
      navigate(`/problem/${problemId}`);
    }
  };

  if (!userProgress) {
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
        {mockProblems.section1.problems.map((problem) => {
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
                    {problem.question[language]}
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