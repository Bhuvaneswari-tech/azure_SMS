import React, { useState } from 'react';
import { Alert, Button, Card, Container, Form } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import api from '../api.jsx';

const Login = ({ setAuth }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await api.post('/login', { email, password });
      const data = res.data;

      localStorage.setItem('access_token', data.access_token || '');
      localStorage.setItem('role', data.role || '');
      localStorage.setItem('user_id', data.user_id || '');

      setAuth({
        access_token: data.access_token,
        role: data.role,
        user_id: data.user_id || '',
      });

      if (data.role === 'admin') {
        navigate('/admin/courses');
      } else {
        navigate('/user/courses');
      }
    } catch (err) {
      setError(err?.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="mt-5" style={{ maxWidth: 420 }}>
      <Card body>
        <h4 className="mb-3">Login</h4>

        {error ? <Alert variant="danger">{error}</Alert> : null}

        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Email</Form.Label>
            <Form.Control
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter email"
              required
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />
          </Form.Group>

          <Button type="submit" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </Button>
        </Form>
      </Card>
    </Container>
  );
};

export default Login;