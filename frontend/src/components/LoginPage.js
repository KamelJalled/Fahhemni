import React, { useState } from 'react';
import StudentLogin from './StudentLogin';
import TeacherLogin from './TeacherLogin';

function LoginPage({ onLogin }) {
  const [loginType, setLoginType] = useState('student');

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold">Math Inequalities Tutor</h2>
        </div>
        
        <div className="bg-white shadow-md rounded px-8 pt-6 pb-8">
          <div className="flex justify-center mb-6">
            <button 
              onClick={() => setLoginType('student')}
              className={`px-4 py-2 mr-2 rounded ${
                loginType === 'student' 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              Student Login
            </button>
            <button 
              onClick={() => setLoginType('teacher')}
              className={`px-4 py-2 rounded ${
                loginType === 'teacher' 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-200 text-gray-700'
              }`}
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
      </div>
    </div>
  );
}

export default LoginPage;