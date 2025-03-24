// Create a custom event system for authentication
const AUTH_LOGIN_EVENT = 'auth:login';
const AUTH_LOGOUT_EVENT = 'auth:logout';

export const authEvents = {
  // Notify the app that user logged in
  emitLogin: () => {
    window.dispatchEvent(new Event(AUTH_LOGIN_EVENT));
  },

  // Notify the app that user logged out
  emitLogout: () => {
    window.dispatchEvent(new Event(AUTH_LOGOUT_EVENT));
  },

  // Listen for login events
  onLogin: (callback: () => void) => {
    window.addEventListener(AUTH_LOGIN_EVENT, callback);
    return () => window.removeEventListener(AUTH_LOGIN_EVENT, callback);
  },

  // Listen for logout events
  onLogout: (callback: () => void) => {
    window.addEventListener(AUTH_LOGOUT_EVENT, callback);
    return () => window.removeEventListener(AUTH_LOGOUT_EVENT, callback);
  }
};