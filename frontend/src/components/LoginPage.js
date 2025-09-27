import React, { useState } from 'react';
import StudentLogin from './StudentLogin';
import TeacherLogin from './TeacherLogin';

function LoginPage({ onLogin }) {
  const [loginType, setLoginType] = useState('student');

  return (
    <div className="login-page">
      <div className="login-tabs">
        <button 
          onClick={() => setLoginType('student')}
          className={loginType === 'student' ? 'active' : ''}
        >
          Student Login
        </button>
        <button 
          onClick={() => setLoginType('teacher')}
          className={loginType === 'teacher' ? 'active' : ''}
        >
          Teacher Login
        </button>
      </div>
      
      {loginType === 'student' ? (
        <StudentLogin onLogin={onLogin} />
      ) : (
        <TeacherLogin onLogin={onLogin} />
      )}
    </div>
  );
}

export default LoginPage;