import React, { useEffect, useState } from 'react';
import { Table, Button } from 'react-bootstrap';
import api from '../api.jsx';

const MyEnrollments = ({ userId }) => {
  const [enrollments, setEnrollments] = useState([]);
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const [enr, crs] = await Promise.all([
        api.get('/enrollments/'),
        api.get('/courses/')
      ]);
      setEnrollments(enr.data.filter(e => e.student_id === userId));
      setCourses(crs.data);
    };
    fetchData();
  }, [userId]);

  const getCourse = (id) => courses.find(c => c.id === id) || {};

  const handleRemove = async (id) => {
    await api.delete(`/enrollments/${id}`);
    setEnrollments(enrollments.filter(e => e.id !== id));
  };

  return (
    <div>
      <h4>My Enrollments</h4>
      <Table bordered hover>
        <thead>
          <tr><th>Course</th><th>Description</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {enrollments.map(e => {
            const course = getCourse(e.course_id);
            return (
              <tr key={e.id}>
                <td>{course.title || e.course_id}</td>
                <td>{course.description || '-'}</td>
                <td>
                  <Button size="sm" variant="danger" onClick={() => handleRemove(e.id)}>Remove</Button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </Table>
    </div>
  );
};

export default MyEnrollments;
