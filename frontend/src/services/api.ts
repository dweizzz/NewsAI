// src/services/api.ts

// Backend API base URL
const API_BASE_URL = 'http://localhost:8000';

export interface Insight {
  insight: string;
  source_title: string;
  source_link: string;
}

export const getInsights = async (searchTerm: string): Promise<Insight[]> => {
  try {
    // Call the insights endpoint with the search term
    const token = localStorage.getItem('token');

    const response = await fetch(`${API_BASE_URL}/api/insights?query=${encodeURIComponent(searchTerm)}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Error fetching insights: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching insights:', error);
    throw error;
  }
};