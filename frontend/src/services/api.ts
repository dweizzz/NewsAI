// services/api.ts

const API_URL = 'http://localhost:8000';

export interface Insight {
  insight: string;
  source_title: string;
  source_link: string;
}

export interface SavedSearchTerm {
  _id: string;
  term: string;
  user_id: string;
  created_at: string;
}

// Helper function for API requests with authentication
const fetchWithAuth = async (url: string, options: RequestInit = {}) => {
  const token = localStorage.getItem('token');

  if (!token) {
    throw new Error('Authentication required');
  }

  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
    ...options.headers
  };

  const response = await fetch(url, {
    ...options,
    headers
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `API request failed with status ${response.status}`);
  }

  return response.json();
};

// Get insights for a search term
export const getInsights = async (searchTerm: string, numResults: number = 5): Promise<Insight[]> => {
  const token = localStorage.getItem('token');
  const headers: HeadersInit = {
    'Content-Type': 'application/json'
  };

  // Add auth token if available
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}/api/insights`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      search_term: searchTerm,
      num_results: numResults
    })
  });

  if (!response.ok) {
    throw new Error(`Failed to get insights: ${response.statusText}`);
  }

  return response.json();
};

// Fetch saved search terms from the API
export const fetchSavedSearches = async (): Promise<SavedSearchTerm[]> => {
  return fetchWithAuth(`${API_URL}/search-terms/`);
};

// Save a new search term
export const saveSearchTerm = async (term: string): Promise<SavedSearchTerm> => {
  return fetchWithAuth(`${API_URL}/search-terms/`, {
    method: 'POST',
    body: JSON.stringify({ term })
  });
};

// Delete a search term
export const deleteSearchTerm = async (searchTermId: string): Promise<void> => {
  await fetchWithAuth(`${API_URL}/search-terms/${searchTermId}`, {
    method: 'DELETE'
  });
};

// Authentication functions
export const loginUser = async (email: string, password: string) => {
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: formData
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Login failed');
  }

  return response.json();
};

export const registerUser = async (email: string, username: string, password: string) => {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, username, password })
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Registration failed');
  }

  return response.json();
};