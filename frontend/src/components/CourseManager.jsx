import React, { useEffect, useState } from 'react';
import { Table, Button, Modal, Form, Alert } from 'react-bootstrap';
import api from '../api.jsx';

const CourseManager = () => {
  const [courses, setCourses] = useState([]);
  const [show, setShow] = useState(false);
  const [editCourse, setEditCourse] = useState(null);
  const [form, setForm] = useState({ title: '', description: '' });
  const [error, setError] = useState('');

  const fetchCourses = async () => {
    const res = await api.get('/courses/');
    setCourses(res.data);
  };
  // eslint-disable-next-line react-hooks/set-state-in-effect
  useEffect(() => { fetchCourses(); }, []);

  const handleShow = (course = null) => {
    setEditCourse(course);
    setForm(course ? { title: course.title, description: course.description } : { title: '', description: '' });
    setShow(true);
  };
  const handleClose = () => { setShow(false); setError(''); };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editCourse) {
        await api.put(`/courses/${editCourse.id}`, form);
      } else {
        await api.post('/courses/', form);
      }
      fetchCourses();
      handleClose();
    } catch (err) {
      setError('Error saving course');
    }
  };

  const handleDelete = async (id) => {
    await api.delete(`/courses/${id}`);
    fetchCourses();
  };

  return (
    <div>
      <Button className="mb-3" onClick={() => handleShow()}>Add Course</Button>
      <Table bordered hover>
        <thead>
          <tr><th>Title</th><th>Description</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {courses.map(course => (
            <tr key={course.id}>
              <td>{course.title}</td>
              <td>{course.description}</td>
              <td>
                <Button size="sm" onClick={() => handleShow(course)}>Edit</Button>{' '}
                <Button size="sm" variant="danger" onClick={() => handleDelete(course.id)}>Delete</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>{editCourse ? 'Edit Course' : 'Add Course'}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {error && <Alert variant="danger">{error}</Alert>}
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Title</Form.Label>
              <Form.Control name="title" value={form.title} onChange={handleChange} required />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Description</Form.Label>
              <Form.Control name="description" value={form.description} onChange={handleChange} required />
            </Form.Group>
            <Button type="submit">Save</Button>
          </Form>
        </Modal.Body>
      </Modal>
    </div>
  );
};

export default CourseManager;
