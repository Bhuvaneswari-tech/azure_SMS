import React from 'react';
import { Container, Nav, Button } from 'react-bootstrap';
import { Link, Outlet, useNavigate } from 'react-router-dom';

const UserDashboard = ({ logout }) => {
  const navigate = useNavigate();
  const handleLogout = () => {
    logout();
    navigate('/');
  };
  return (
    <Container className="mt-4">
      <h2>User Dashboard</h2>
      <Nav className="mb-3">
        <Nav.Item><Link to="/user/courses" className="nav-link">Course List</Link></Nav.Item>
        <Nav.Item><Link to="/user/my-courses" className="nav-link">My Enrollments</Link></Nav.Item>
        <Button variant="outline-danger" className="ms-auto" onClick={handleLogout}>Logout</Button>
      </Nav>
      <Outlet />
    </Container>
  );
};

export default UserDashboard;
