import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, useLanguage } from '../App';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Globe, Calculator, Trophy, Star } from 'lucide-react';

const StudentLogin = () => {
  const [username, setUsername] = useState('');
  const [className, setClassName] = useState('GR9-A');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const { language, toggleLanguage } = useLanguage();
  const navigate = useNavigate();

  const text = {
    en: {
      title: "Math Inequalities Tutor",
      subtitle: "Master Grade 9 Inequalities with Interactive Learning",
      username: "Enter your username",
      placeholder: "Your username...",
      login: "Start Learning",
      teacher: "Teacher Access",
      features: [
        "30 carefully designed problems",
        "Progressive hint system",
        "Track your progress",
        "Earn badges and points"
      ]
    },
    ar: {
      title: "مدرس المتباينات الرياضية",
      subtitle: "أتقن متباينات الصف التاسع مع التعلم التفاعلي",
      username: "أدخل اسم المستخدم",
      placeholder: "اسم المستخدم...",
      login: "ابدأ التعلم",
      teacher: "دخول المعلم",
      features: [
        "٣٠ مسألة مصممة بعناية",
        "نظام إرشادات تدريجي",
        "تتبع تقدمك",
        "اكسب الشارات والنقاط"
      ]
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username.trim()) return;

    setIsLoading(true);
    
    try {
      // Call backend API for student login
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/auth/student-login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username.trim() }),
      });

      if (response.ok) {
        const student = await response.json();
        login(student.username, 'student');
        navigate('/dashboard');
      } else {
        console.error('Login failed');
      }
    } catch (error) {
      console.error('Login error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-10 left-10 text-6xl">≤</div>
        <div className="absolute top-32 right-20 text-4xl">≥</div>
        <div className="absolute bottom-20 left-32 text-5xl">&lt;</div>
        <div className="absolute bottom-40 right-10 text-3xl">&gt;</div>
        <div className="absolute top-1/2 left-1/4 text-7xl opacity-5">x</div>
        <div className="absolute top-1/3 right-1/4 text-6xl opacity-5">س</div>
      </div>

      {/* Language Toggle */}
      <Button
        onClick={toggleLanguage}
        variant="outline"
        size="sm"
        className="absolute top-4 right-4 z-10"
      >
        <Globe className="w-4 h-4 mr-2" />
        {language === 'en' ? 'العربية' : 'English'}
      </Button>

      <div className="w-full max-w-md relative z-10">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="p-4 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-full shadow-lg">
              <Calculator className="w-12 h-12 text-white" />
            </div>
          </div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            {text[language].title}
          </h1>
          <p className="text-gray-600">
            {text[language].subtitle}
          </p>
        </div>

        {/* Login Card */}
        <Card className="shadow-xl border-0 bg-white/80 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="text-center text-gray-700">
              {text[language].username}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder={text[language].placeholder}
                className="h-12 text-lg"
                required
              />
              <Button
                type="submit"
                className="w-full h-12 text-lg bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 shadow-lg"
                disabled={isLoading || !username.trim()}
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    {language === 'en' ? 'Loading...' : 'جاري التحميل...'}
                  </div>
                ) : (
                  text[language].login
                )}
              </Button>
            </form>

            <div className="mt-6 pt-4 border-t">
              <Button
                onClick={() => navigate('/teacher')}
                variant="outline"
                className="w-full"
              >
                {text[language].teacher}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Features */}
        <div className="mt-8 grid grid-cols-2 gap-4">
          {text[language].features.map((feature, index) => (
            <div key={index} className="flex items-center bg-white/60 p-3 rounded-lg backdrop-blur-sm">
              {index === 0 && <Trophy className="w-5 h-5 text-emerald-600 mr-2 flex-shrink-0" />}
              {index === 1 && <Star className="w-5 h-5 text-teal-600 mr-2 flex-shrink-0" />}
              {index === 2 && <Calculator className="w-5 h-5 text-cyan-600 mr-2 flex-shrink-0" />}
              {index === 3 && <Globe className="w-5 h-5 text-emerald-600 mr-2 flex-shrink-0" />}
              <span className="text-sm text-gray-700">{feature}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default StudentLogin;