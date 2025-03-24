import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authEvents } from '../services/authEvents';
import './Login.css';

// Backend API base URL
const API_BASE_URL = 'http://localhost:8000';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email || !password) {
      setError('Please enter both email and password');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      // Create form data for OAuth2 password flow
      const formData = new FormData();
      formData.append('username', email); // FastAPI OAuth2 expects 'username' field
      formData.append('password', password);

      console.log("Attempting login with:", {
        email,
        password: "[REDACTED]" // Don't log actual password
      });

      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        body: formData,
        credentials: 'include', // Include cookies if needed
      });

      // Log response for debugging
      console.log("Login response status:", response.status);

      const data = await response.json();
      console.log("Login response data:", data);

      if (!response.ok) {
        // Handle specific error cases
        if (data.detail === "Incorrect email or password") {
          setError('Invalid email or password');
        } else {
          setError(data.detail || 'Login failed');
        }
        return;
      }

      // Store token
      localStorage.setItem('token', data.access_token);

      // Emit login event to notify App component
      authEvents.emitLogin();

      // Redirect to main page
      navigate('/');
    } catch (err) {
      console.error("Login error:", err);
      setError('An error occurred during login. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegisterClick = () => {
    navigate('/register');
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Log in to News AI</h2>
        {error && <div className="login-error">{error}</div>}

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              disabled={isLoading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              disabled={isLoading}
            />
          </div>

          <button
            type="submit"
            className="login-button"
            disabled={isLoading}
          >
            {isLoading ? 'Logging in...' : 'Log In'}
          </button>
        </form>

        <div className="login-footer">
          <p>Don't have an account?</p>
          <button
            className="register-link"
            onClick={handleRegisterClick}
            disabled={isLoading}
          >
            Register
          </button>
        </div>
      </div>
    </div>
  );
}

export default Login;