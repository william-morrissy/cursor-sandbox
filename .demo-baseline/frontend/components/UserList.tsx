import React, { useState, useEffect } from 'react';

// Missing: TypeScript interfaces, error handling, loading states

export const UserList = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    // TODO: Replace with actual API call
    fetch('/api/users')
      .then(res => res.json())
      .then(data => setUsers(data));
  }, []);

  return (
    <div className="user-list">
      <h2>Users</h2>
      {users.map(user => (
        <div key={user.id} className="user-card">
          <h3>{user.name}</h3>
          <p>{user.email}</p>
          <span>{user.role}</span>
        </div>
      ))}
    </div>
  );
};

