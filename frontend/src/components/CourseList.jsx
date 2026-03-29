import React, { useEffect, useState } from 'react';
import { Table, Button, Alert } from 'react-bootstrap';
import api from '../api.jsx';

const CourseList = ({ enroll, userId }) => {
  const [courses, setCourses] = useState([]);
  const [enrolledIds, setEnrolledIds] = useState([]);
  const [error, setError] = useState('');

  // Fetch courses
  useEffect(() => {
    api.get('/courses/').then(res => setCourses(res.data));
  }, []);

  // Fetch enrollments for this user
  useEffect(() => {
    api.get('/enrollments/').then(res => {
      setEnrolledIds(res.data.filter(e => e.student_id === userId).map(e => e.course_id));
    });
  }, [userId]);

  const handleEnroll = async (courseId) => {
    try {
      await enroll(courseId);
      setEnrolledIds([...enrolledIds, courseId]);
    } catch (err) {
      setError('Failed to enroll');
    }
  };

  return (
    <div>
      <h4>Available Courses</h4>
      {error && <Alert variant="danger">{error}</Alert>}
      <Table bordered hover>
        <thead>
          <tr><th>Name</th><th>Description</th><th>Action</th></tr>
        </thead>
        <tbody>
          {courses.map(course => (
            <tr key={course.id}>
              <td>{course.title}</td>
              <td>{course.description}</td>
              <td>
                {enrolledIds.includes(course.id) ? (
                  <Button size="sm" disabled>Enrolled</Button>
                ) : (
                  <Button size="sm" onClick={() => handleEnroll(course.id)}>
                    Enroll
                  </Button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default CourseList;
