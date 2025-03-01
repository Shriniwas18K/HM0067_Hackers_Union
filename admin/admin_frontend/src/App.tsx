import React from 'react';
import { useAuth } from './utils/AuthContext';
import Registration from './pages/Registeration';

const App: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div>
      {isAuthenticated() ? <h1>DashBoard</h1>: <Registration />}
    </div>
  );
};

export default App
