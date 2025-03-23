const API_BASE_URL = 'http://localhost:8000/api';

export interface Insight {
  insight: string;
  source_title: string;
  source_link: string;
}

export interface SearchRequest {
  search_term: string;
  num_results?: number;
}

export const getInsights = async (searchTerm: string, numResults: number = 5): Promise<Insight[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/insights`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        search_term: searchTerm,
        num_results: numResults,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch insights');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching insights:', error);
    throw error;
  }
}; 