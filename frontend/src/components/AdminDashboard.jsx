import React from 'react';
import { Container, Nav, Button } from 'react-bootstrap';
import { Link, Outlet, useNavigate } from 'react-router-dom';

const AdminDashboard = ({ logout }) => {
  const navigate = useNavigate();
  const handleLogout = () => {
    logout();
    navigate('/');
  };
  return (
    <Container className="mt-4">
      <h2>Admin Dashboard</h2>
      <Nav className="mb-3">
        <Nav.Item><Link to="/admin/courses" className="nav-link">Manage Courses</Link></Nav.Item>
        <Nav.Item><Link to="/admin/enrollments" className="nav-link">View Enrollments</Link></Nav.Item>
        <Nav.Item><Link to="/admin/users" className="nav-link">View Users</Link></Nav.Item>
        <Button variant="outline-danger" className="ms-auto" onClick={handleLogout}>Logout</Button>
      </Nav>
      <Outlet />
    </Container>
  );
};

export default AdminDashboard;
