import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, useLanguage } from '../App';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Globe, LogOut, Users, TrendingUp, Award, BarChart3 } from 'lucide-react';
import { mockProblems } from '../mock';

const TeacherDashboard = () => {
  const { user, logout, isTeacher } = useAuth();
  const { language, toggleLanguage } = useLanguage();
  const navigate = useNavigate();
  const [students, setStudents] = useState([]);
  const [stats, setStats] = useState({
    totalStudents: 0,
    averageProgress: 0,
    completedProblems: 0,
    averageScore: 0
  });

  useEffect(() => {
    if (!user || !isTeacher) {
      navigate('/');
      return;
    }

    // Load all student data from localStorage
    const studentData = [];
    const keys = Object.keys(localStorage);
    
    keys.forEach(key => {
      if (key.startsWith('mathapp_progress_')) {
        const username = key.replace('mathapp_progress_', '');
        const progress = JSON.parse(localStorage.getItem(key));
        
        // Calculate student stats
        const section1Progress = progress.section1;
        const completedProblems = Object.values(section1Progress).filter(p => p.completed).length;
        const totalProblems = Object.keys(section1Progress).length;
        const progressPercentage = (completedProblems / totalProblems) * 100;
        
        // Calculate weighted score
        let totalScore = 0;
        let totalWeight = 0;
        Object.keys(section1Progress).forEach(problemId => {
          const problemProgress = section1Progress[problemId];
          const problem = mockProblems.section1.problems.find(p => p.id === problemId);
          if (problem && problemProgress.completed) {
            totalScore += (problemProgress.score * problem.weight) / 100;
            totalWeight += problem.weight;
          }
        });
        const weightedScore = totalWeight > 0 ? (totalScore / totalWeight) * 100 : 0;
        
        studentData.push({
          username,
          progress: progressPercentage,
          completedProblems,
          totalProblems,
          weightedScore: Math.round(weightedScore),
          totalAttempts: Object.values(section1Progress).reduce((sum, p) => sum + p.attempts, 0),
          lastActivity: new Date().toLocaleDateString(), // Mock data
          problemsStatus: section1Progress
        });
      }
    });

    setStudents(studentData);

    // Calculate overall stats
    if (studentData.length > 0) {
      const totalStudents = studentData.length;
      const averageProgress = studentData.reduce((sum, s) => sum + s.progress, 0) / totalStudents;
      const completedProblems = studentData.reduce((sum, s) => sum + s.completedProblems, 0);
      const averageScore = studentData.reduce((sum, s) => sum + s.weightedScore, 0) / totalStudents;

      setStats({
        totalStudents,
        averageProgress: Math.round(averageProgress),
        completedProblems,
        averageScore: Math.round(averageScore)
      });
    }
  }, [user, isTeacher, navigate]);

  const text = {
    en: {
      title: "Teacher Dashboard",
      subtitle: "Monitor student progress and performance",
      totalStudents: "Total Students",
      averageProgress: "Average Progress",
      completedProblems: "Completed Problems",
      averageScore: "Average Score",
      studentName: "Student Name",
      progress: "Progress",
      score: "Weighted Score",
      attempts: "Total Attempts",
      lastActivity: "Last Activity",
      details: "Problem Details",
      preparation: "Prep",
      explanation: "Expl",
      practice: "Prac",
      assessment: "Assess",
      examprep: "Exam",
      completed: "✓",
      notStarted: "-",
      inProgress: "...",
      noStudents: "No student data available yet",
      logout: "Logout"
    },
    ar: {
      title: "لوحة المعلم",
      subtitle: "راقب تقدم الطلاب وأداءهم",
      totalStudents: "إجمالي الطلاب",
      averageProgress: "متوسط التقدم",
      completedProblems: "المسائل المكتملة",
      averageScore: "متوسط النتيجة",
      studentName: "اسم الطالب",
      progress: "التقدم",
      score: "النتيجة المرجحة",
      attempts: "إجمالي المحاولات",
      lastActivity: "آخر نشاط",
      details: "تفاصيل المسائل",
      preparation: "تحضير",
      explanation: "شرح",
      practice: "تدريب",
      assessment: "تقييم",
      examprep: "امتحان",
      completed: "✓",
      notStarted: "-",
      inProgress: "...",
      noStudents: "لا توجد بيانات طلاب متاحة بعد",
      logout: "خروج"
    }
  };

  const getProblemStatusSymbol = (problemProgress) => {
    if (problemProgress.completed) return text[language].completed;
    if (problemProgress.attempts > 0) return text[language].inProgress;
    return text[language].notStarted;
  };

  const getProblemTypeLabel = (problemType) => {
    const labels = {
      preparation: text[language].preparation,
      explanation: text[language].explanation,
      practice: text[language].practice,
      assessment: text[language].assessment,
      examprep: text[language].examprep
    };
    return labels[problemType] || problemType;
  };

  return (
    <div className="min-h-screen p-4">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">
            {text[language].title}
          </h1>
          <p className="text-gray-600">{text[language].subtitle}</p>
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
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <Card className="bg-gradient-to-br from-blue-500 to-indigo-600 text-white">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-blue-100">{text[language].totalStudents}</p>
                <p className="text-3xl font-bold">{stats.totalStudents}</p>
              </div>
              <Users className="w-10 h-10 text-blue-200" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-green-500 to-emerald-600 text-white">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-green-100">{text[language].averageProgress}</p>
                <p className="text-3xl font-bold">{stats.averageProgress}%</p>
              </div>
              <TrendingUp className="w-10 h-10 text-green-200" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-orange-500 to-red-600 text-white">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-orange-100">{text[language].completedProblems}</p>
                <p className="text-3xl font-bold">{stats.completedProblems}</p>
              </div>
              <BarChart3 className="w-10 h-10 text-orange-200" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-500 to-pink-600 text-white">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-100">{text[language].averageScore}</p>
                <p className="text-3xl font-bold">{stats.averageScore}%</p>
              </div>
              <Award className="w-10 h-10 text-purple-200" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Students Table */}
      <Card>
        <CardHeader>
          <CardTitle>{text[language].details}</CardTitle>
        </CardHeader>
        <CardContent>
          {students.length === 0 ? (
            <div className="text-center py-12">
              <Users className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500 text-lg">{text[language].noStudents}</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{text[language].studentName}</TableHead>
                    <TableHead>{text[language].progress}</TableHead>
                    <TableHead>{text[language].score}</TableHead>
                    <TableHead>{text[language].attempts}</TableHead>
                    <TableHead className="text-center" colSpan={6}>
                      {text[language].details}
                    </TableHead>
                  </TableRow>
                  <TableRow className="border-b">
                    <TableHead></TableHead>
                    <TableHead></TableHead>
                    <TableHead></TableHead>
                    <TableHead></TableHead>
                    {mockProblems.section1.problems.map((problem) => (
                      <TableHead key={problem.id} className="text-center text-xs">
                        {getProblemTypeLabel(problem.type)}
                      </TableHead>
                    ))}
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {students.map((student) => (
                    <TableRow key={student.username}>
                      <TableCell className="font-medium">
                        {student.username}
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <Progress value={student.progress} className="w-20" />
                          <span className="text-sm text-gray-500">
                            {Math.round(student.progress)}%
                          </span>
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant={
                          student.weightedScore >= 80 ? 'default' :
                          student.weightedScore >= 60 ? 'secondary' : 'destructive'
                        }>
                          {student.weightedScore}%
                        </Badge>
                      </TableCell>
                      <TableCell className="text-center">
                        {student.totalAttempts}
                      </TableCell>
                      {mockProblems.section1.problems.map((problem) => (
                        <TableCell key={problem.id} className="text-center">
                          <span className={`text-sm ${
                            student.problemsStatus[problem.id].completed 
                              ? 'text-green-600 font-bold' 
                              : student.problemsStatus[problem.id].attempts > 0
                              ? 'text-orange-600'
                              : 'text-gray-400'
                          }`}>
                            {getProblemStatusSymbol(student.problemsStatus[problem.id])}
                          </span>
                          {student.problemsStatus[problem.id].completed && (
                            <div className="text-xs text-gray-500">
                              {student.problemsStatus[problem.id].score}%
                            </div>
                          )}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default TeacherDashboard;