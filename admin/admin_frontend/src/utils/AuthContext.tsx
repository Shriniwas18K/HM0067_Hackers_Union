import React, { createContext, useContext, useState, ReactNode, useMemo } from 'react';

// Define the shape of the Auth context
interface AuthContextType {
  authToken: string;
  setAuthToken: (token: string) => void;
  isAuthenticated: () => boolean;
}

// Create a context for the Auth token
const AuthContext = createContext<AuthContextType | null>(null);

// Create a provider component
export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [authToken, setAuthToken] = useState<string>(() => {
    // Initialize state from local storage
    return localStorage.getItem('authToken') || '';
  });

  const updateAuthToken = (token: string) => {
    setAuthToken(token);
    if (token) {
      localStorage.setItem('authToken', token);
    } else {
      localStorage.removeItem('authToken');
    }
  };

  const value = useMemo(() => ({
    authToken,
    setAuthToken: updateAuthToken,
    isAuthenticated: () => authToken !== null && authToken !== '',
  }), [authToken]);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Create a custom hook to use the Auth context
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
