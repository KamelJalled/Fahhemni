import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, useLanguage } from '../App';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Globe, LogOut, Users, TrendingUp, Award, BarChart3 } from 'lucide-react';

const TeacherDashboard = () => {
  const { user, logout, isTeacher } = useAuth();
  const { language, toggleLanguage } = useLanguage();
  const navigate = useNavigate();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedClass, setSelectedClass] = useState('all');

  useEffect(() => {
    if (!user || !isTeacher) {
      navigate('/');
      return;
    }

    fetchDashboardData();
  }, [user, isTeacher, navigate]);

  const fetchDashboardData = async (classFilter = null) => {
    try {
      setLoading(true);
      const url = classFilter && classFilter !== 'all' 
        ? `${process.env.REACT_APP_BACKEND_URL}/api/teacher/students?class_filter=${classFilter}`
        : `${process.env.REACT_APP_BACKEND_URL}/api/teacher/students`;
      
      const response = await fetch(url);
      
      if (response.ok) {
        const data = await response.json();
        setDashboardData(data);
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Fallback to empty data
      setDashboardData({
        total_students: 0,
        average_progress: 0,
        completed_problems: 0,
        average_score: 0,
        students: []
      });
    } finally {
      setLoading(false);
    }
  };

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

  if (loading || !dashboardData) {
    return <div className="min-h-screen flex items-center justify-center">
      <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-emerald-500"></div>
    </div>;
  }

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
                <p className="text-3xl font-bold">{dashboardData.total_students}</p>
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
                <p className="text-3xl font-bold">{dashboardData.average_progress}%</p>
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
                <p className="text-3xl font-bold">{dashboardData.completed_problems}</p>
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
                <p className="text-3xl font-bold">{dashboardData.average_score}%</p>
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
          {dashboardData.students.length === 0 ? (
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
                    <TableHead className="text-center text-xs">{getProblemTypeLabel('preparation')}</TableHead>
                    <TableHead className="text-center text-xs">{getProblemTypeLabel('explanation')}</TableHead>
                    <TableHead className="text-center text-xs">{getProblemTypeLabel('practice')}</TableHead>
                    <TableHead className="text-center text-xs">{getProblemTypeLabel('practice')}</TableHead>
                    <TableHead className="text-center text-xs">{getProblemTypeLabel('assessment')}</TableHead>
                    <TableHead className="text-center text-xs">{getProblemTypeLabel('examprep')}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {dashboardData.students.map((student) => (
                    <TableRow key={student.username}>
                      <TableCell className="font-medium">
                        {student.username}
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <Progress value={student.progress_percentage} className="w-20" />
                          <span className="text-sm text-gray-500">
                            {Math.round(student.progress_percentage)}%
                          </span>
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant={
                          student.weighted_score >= 80 ? 'default' :
                          student.weighted_score >= 60 ? 'secondary' : 'destructive'
                        }>
                          {Math.round(student.weighted_score)}%
                        </Badge>
                      </TableCell>
                      <TableCell className="text-center">
                        {student.total_attempts}
                      </TableCell>
                      {Object.keys(student.problems_status).map((problemId) => (
                        <TableCell key={problemId} className="text-center">
                          <span className={`text-sm ${
                            student.problems_status[problemId].completed 
                              ? 'text-green-600 font-bold' 
                              : student.problems_status[problemId].attempts > 0
                              ? 'text-orange-600'
                              : 'text-gray-400'
                          }`}>
                            {getProblemStatusSymbol(student.problems_status[problemId])}
                          </span>
                          {student.problems_status[problemId].completed && (
                            <div className="text-xs text-gray-500">
                              {student.problems_status[problemId].score}%
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