import React, { useEffect, useState } from 'react';
import { Table, Button } from 'react-bootstrap';
import api from '../api.jsx';

const EnrollmentManager = () => {
  const [enrollments, setEnrollments] = useState([]);
  const [courses, setCourses] = useState([]);
  const [students, setStudents] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [enr, crs, std] = await Promise.all([
          api.get('/enrollments/'),
          api.get('/courses/'),
          api.get('/students/'),
        ]);
        setEnrollments(enr.data || []);
        setCourses(crs.data || []);
        setStudents(std.data || []);
      } catch (err) {
        console.error('Failed to load enrollments', err);
      }
    };
    fetchData();
  }, []);

  const getCourse = (id) => courses.find((c) => String(c.id) === String(id));
  const getStudent = (id) => students.find((s) => String(s.id) === String(id));

  const handleRemove = async (id) => {
    try {
      await api.delete(`/enrollments/${id}`);
      setEnrollments((prev) => prev.filter((e) => e.id !== id));
    } catch (err) {
      console.error('Failed to remove enrollment', err);
    }
  };

  return (
    <div>
      <h4>View Enrollments</h4>
      <Table bordered hover>
        <thead>
          <tr>
            <th>Student</th>
            <th>Course</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {enrollments.map((e) => (
            <tr key={e.id}>
              <td>{getStudent(e.student_id)?.name || e.student_id}</td>
              <td>{getCourse(e.course_id)?.title || e.course_id}</td>
              <td>
                <Button size="sm" variant="danger" onClick={() => handleRemove(e.id)}>
                  Remove
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default EnrollmentManager;