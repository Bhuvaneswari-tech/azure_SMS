import React from 'react';
import { Container, Button, Row, Col } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const LandingPage = () => (
  <Container className="text-center mt-5">
    <h1>Welcome to Student Management System</h1>
    <p>Manage courses, students, and enrollments with ease.</p>
    <Row className="justify-content-center mt-4">
      <Col xs="auto">
        <Link to="/login">
          <Button variant="primary" className="mx-2">Login</Button>
        </Link>
        <Link to="/register">
          <Button variant="success" className="mx-2">Register</Button>
        </Link>
      </Col>
    </Row>
  </Container>
);

export default LandingPage;
