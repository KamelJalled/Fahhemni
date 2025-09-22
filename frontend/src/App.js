import React, { createContext, useContext, useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import StudentLogin from "./components/StudentLogin";
import TeacherLogin from "./components/TeacherLogin";
import Dashboard from "./components/Dashboard";
import ProblemView from "./components/ProblemView";
import TeacherDashboard from "./components/TeacherDashboard";

// this is a test comment.

// Language Context
const LanguageContext = createContext();

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState(() => {
    return localStorage.getItem('mathapp_language') || 'en';
  });

  useEffect(() => {
    localStorage.setItem('mathapp_language', language);
    // Update document direction for RTL
    document.dir = language === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = language;
  }, [language]);

  const toggleLanguage = () => {
    setLanguage(prev => prev === 'en' ? 'ar' : 'en');
  };

  return (
    <LanguageContext.Provider value={{ language, toggleLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
};

// Auth Context
const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem('mathapp_user');
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const [isTeacher, setIsTeacher] = useState(() => {
    return localStorage.getItem('mathapp_teacher') === 'true';
  });

  const login = (username, userType = 'student') => {
    const userData = {
      username,
      userType,
      loginTime: new Date().toISOString()
    };
    
    setUser(userData);
    setIsTeacher(userType === 'teacher');
    localStorage.setItem('mathapp_user', JSON.stringify(userData));
    localStorage.setItem('mathapp_teacher', userType === 'teacher');
  };

  const logout = async () => {
    // Clear all local state and storage first (immediate UI response)
    setUser(null);
    setIsTeacher(false);
    localStorage.removeItem('mathapp_user');
    localStorage.removeItem('mathapp_teacher');
    
    // Clear any cached data
    Object.keys(localStorage).forEach(key => {
      if (key.startsWith('mathapp_')) {
        localStorage.removeItem(key);
      }
    });
    
    // Try to call backend logout endpoint silently (don't block on errors)
    try {
      await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/auth/logout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
    } catch (error) {
      // Silently handle logout errors - user experience shouldn't be affected
      console.log('Logout request completed');
    }
    
    // Navigate to home page immediately without flash
    setTimeout(() => {
      window.location.href = '/';
    }, 100); // Small delay to ensure state is cleared
  };

  return (
    <AuthContext.Provider value={{ user, isTeacher, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

function App() {
  return (
    <div className="App min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50">
      <AuthProvider>
        <LanguageProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<StudentLogin />} />
              <Route path="/teacher" element={<TeacherLogin />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/problem/:problemId" element={<ProblemView />} />
              <Route path="/teacher-dashboard" element={<TeacherDashboard />} />
              {/* Catch-all route - redirect to home */}
              <Route path="*" element={<StudentLogin />} />
            </Routes>
          </BrowserRouter>
        </LanguageProvider>
      </AuthProvider>
    </div>
  );
}

export default App;