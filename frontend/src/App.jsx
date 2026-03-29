import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import api from './api.jsx';
import LandingPage from './components/LandingPage';
import Register from './components/Register';
import Login from './components/Login';
import AdminDashboard from './components/AdminDashboard';
import UserDashboard from './components/UserDashboard';
import CourseManager from './components/CourseManager';
import EnrollmentManager from './components/EnrollmentManager';
import UserList from './components/UserList';
import CourseList from './components/CourseList';
import MyEnrollments from './components/MyEnrollments';

function App() {
  const [auth, setAuth] = useState(() => {
    const token = localStorage.getItem('access_token');
    const role = localStorage.getItem('role');
    const user_id = localStorage.getItem('user_id');
    if (token && role) {
      return { access_token: token, role, user_id };
    }
    return null;
  });

  const userId = auth?.user_id ? String(auth.user_id) : '';

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('role');
    localStorage.removeItem('user_id');
    setAuth(null);
  };

  const enroll = async (courseId) => {
    const payload = {
      student_id: String(userId),
      course_id: String(courseId),
    };

    if (!payload.student_id || !payload.course_id) {
      console.error('Invalid enroll payload:', payload);
      return;
    }

    try {
      await api.post('/enrollments/', payload);
    } catch (err) {
      console.error('Enroll failed:', err?.response?.data || err.message);
    }
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login setAuth={setAuth} />} />

        <Route
          path="/admin/*"
          element={auth?.role === 'admin' ? <AdminDashboard logout={logout} /> : <Navigate to="/login" />}
        >
          <Route path="courses" element={<CourseManager />} />
          <Route path="enrollments" element={<EnrollmentManager />} />
          <Route path="users" element={<UserList />} />
        </Route>

        <Route
          path="/user/*"
          element={auth?.role === 'student' ? <UserDashboard logout={logout} /> : <Navigate to="/login" />}
        >
          <Route path="courses" element={<CourseList enroll={enroll} userId={userId} />} />
          <Route path="my-courses" element={<MyEnrollments userId={userId} />} />
        </Route>

        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;