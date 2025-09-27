import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import LoginPage from './components/LoginPage';
import Dashboard from './components/Dashboard';
import ProblemView from './components/ProblemView';
import TeacherDashboard from './components/TeacherDashboard';

// Create contexts
export const AuthContext = React.createContext(null);
export const LanguageContext = React.createContext(null);

function App() {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [language, setLanguage] = useState(localStorage.getItem('language') || 'en');

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch (error) {
        console.error('Error parsing saved user:', error);
        localStorage.removeItem('user');
      }
    }
    setIsLoading(false);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('user');
    localStorage.removeItem('currentSection');
    localStorage.removeItem('currentProblem');
  };

  const toggleLanguage = () => {
    const newLang = language === 'en' ? 'ar' : 'en';
    setLanguage(newLang);
    localStorage.setItem('language', newLang);
  };

  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner">Loading...</div>
      </div>
    );
  }

  return (
    <AuthContext.Provider value={{ user, logout: handleLogout }}>
      <LanguageContext.Provider value={{ language, toggleLanguage }}>
        <Router>
          <div dir={language === 'ar' ? 'rtl' : 'ltr'} className="App">
            <Routes>
              <Route 
                path="/login" 
                element={
                  user ? <Navigate to="/dashboard" replace /> : <LoginPage onLogin={handleLogin} />
                } 
              />

              <Route 
                path="/dashboard" 
                element={
                  user ? (
                    user.role === 'teacher' ? (
                      <TeacherDashboard user={user} onLogout={handleLogout} />
                    ) : (
                      <Dashboard user={user} onLogout={handleLogout} />
                    )
                  ) : (
                    <Navigate to="/login" replace />
                  )
                } 
              />

              <Route 
                path="/section/:sectionId/problem/:problemId" 
                element={
                  user ? (
                    <ProblemView user={user} onLogout={handleLogout} />
                  ) : (
                    <Navigate to="/login" replace />
                  )
                } 
              />

              <Route 
                path="/problem/:problemId" 
                element={
                  user ? (
                    <ProblemView user={user} onLogout={handleLogout} />
                  ) : (
                    <Navigate to="/login" replace />
                  )
                } 
              />

              <Route 
                path="/teacher-dashboard" 
                element={
                  user && user.role === 'teacher' ? (
                    <TeacherDashboard user={user} onLogout={handleLogout} />
                  ) : (
                    <Navigate to="/login" replace />
                  )
                } 
              />

              <Route 
                path="/" 
                element={<Navigate to={user ? "/dashboard" : "/login"} replace />} 
              />

              <Route 
                path="*" 
                element={<Navigate to={user ? "/dashboard" : "/login"} replace />} 
              />
            </Routes>
          </div>
        </Router>
      </LanguageContext.Provider>
    </AuthContext.Provider>
  );
}

// Export hooks
export const useAuth = () => {
  const context = React.useContext(AuthContext);
  if (!context) {
    return { user: null, logout: () => {} };
  }
  return context;
};

export const useLanguage = () => {
  const context = React.useContext(LanguageContext);
  if (!context) {
    return { language: 'en', toggleLanguage: () => {} };
  }
  return context;
};

export default App;