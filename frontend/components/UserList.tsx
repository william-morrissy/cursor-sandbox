import React, { useState, useEffect } from 'react';

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

interface UserListState {
  users: User[];
  loading: boolean;
  error: string | null;
}

export const UserList = () => {
  const [state, setState] = useState<UserListState>({
    users: [],
    loading: true,
    error: null,
  });

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setState(prev => ({ ...prev, loading: true, error: null }));
        
        const response = await fetch('/api/users');
        
        if (!response.ok) {
          throw new Error(`Failed to fetch users: ${response.status} ${response.statusText}`);
        }
        
        const data: User[] = await response.json();
        setState({ users: data, loading: false, error: null });
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
        setState(prev => ({ ...prev, loading: false, error: errorMessage }));
      }
    };

    fetchUsers();
  }, []);

  if (state.loading) {
    return (
      <div className="user-list">
        <h2>Users</h2>
        <p>Loading...</p>
      </div>
    );
  }

  if (state.error) {
    return (
      <div className="user-list">
        <h2>Users</h2>
        <div className="error" role="alert">
          <p>Error: {state.error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="user-list">
      <h2>Users</h2>
      {state.users.length === 0 ? (
        <p>No users found.</p>
      ) : (
        state.users.map(user => (
          <div key={user.id} className="user-card">
            <h3>{user.name}</h3>
            <p>{user.email}</p>
            <span>{user.role}</span>
          </div>
        ))
      )}
    </div>
  );
};

