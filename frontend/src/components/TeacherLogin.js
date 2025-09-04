import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, useLanguage } from '../App';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Globe, GraduationCap, ArrowLeft } from 'lucide-react';

const TeacherLogin = () => {
  const [accessCode, setAccessCode] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const { language, toggleLanguage } = useLanguage();
  const navigate = useNavigate();

  const text = {
    en: {
      title: "Teacher Dashboard Access",
      subtitle: "Monitor student progress and performance",
      accessCode: "Access Code",
      placeholder: "Enter access code...",
      login: "Access Dashboard",
      back: "Back to Student Login",
      error: "Invalid access code. Please try again."
    },
    ar: {
      title: "دخول لوحة المعلم",
      subtitle: "راقب تقدم الطلاب وأداءهم",
      accessCode: "رمز الدخول",
      placeholder: "أدخل رمز الدخول...",
      login: "دخول اللوحة",
      back: "العودة لدخول الطالب",
      error: "رمز دخول غير صحيح. حاول مرة أخرى."
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!accessCode.trim()) return;

    setIsLoading(true);
    setError('');

    // Simulate API call
    setTimeout(() => {
      if (accessCode.trim() === 'teacher2024') {
        login('Teacher', 'teacher');
        navigate('/teacher-dashboard');
      } else {
        setError(text[language].error);
      }
      setIsLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-10 left-10 text-6xl">≤</div>
        <div className="absolute top-32 right-20 text-4xl">≥</div>
        <div className="absolute bottom-20 left-32 text-5xl">&lt;</div>
        <div className="absolute bottom-40 right-10 text-3xl">&gt;</div>
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

      {/* Back Button */}
      <Button
        onClick={() => navigate('/')}
        variant="outline"
        size="sm"
        className="absolute top-4 left-4 z-10"
      >
        <ArrowLeft className="w-4 h-4 mr-2" />
        {text[language].back}
      </Button>

      <div className="w-full max-w-md relative z-10">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="p-4 bg-gradient-to-br from-orange-500 to-red-600 rounded-full shadow-lg">
              <GraduationCap className="w-12 h-12 text-white" />
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
              {text[language].accessCode}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                type="password"
                value={accessCode}
                onChange={(e) => {
                  setAccessCode(e.target.value);
                  setError('');
                }}
                placeholder={text[language].placeholder}
                className="h-12 text-lg"
                required
              />
              {error && (
                <p className="text-red-500 text-sm text-center">{error}</p>
              )}
              <Button
                type="submit"
                className="w-full h-12 text-lg bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 shadow-lg"
                disabled={isLoading || !accessCode.trim()}
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
          </CardContent>
        </Card>

        {/* Access Code Hint */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-500">
            {language === 'en' 
              ? 'Contact your administrator for the access code' 
              : 'اتصل بالمسؤول للحصول على رمز الدخول'
            }
          </p>
        </div>
      </div>
    </div>
  );
};

export default TeacherLogin;