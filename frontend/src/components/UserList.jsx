import React, { useEffect, useState } from 'react';
import { Table } from 'react-bootstrap';
import api from '../api.jsx';

const UserList = () => {
  const [users, setUsers] = useState([]);
  useEffect(() => {
    api.get('/users/').then(res => setUsers(res.data));
  }, []);
  return (
    <div>
      <h4>All Users</h4>
      <Table bordered hover>
        <thead>
          <tr><th>ID</th><th>Name</th><th>Email</th></tr>
        </thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.username}</td>
              <td>{u.email}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default UserList;