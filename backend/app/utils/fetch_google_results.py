import os
from dotenv import load_dotenv
import requests
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

def fetch_google_search_results(search_term: str, num_results: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch search results from Google using the Custom Search API.
    
    Args:
        search_term (str): The search query
        num_results (int): Number of results to return (max 10 per request)
    
    Returns:
        List[Dict[str, Any]]: List of search results with title, link, and snippet
    """
    api_key = os.getenv('GOOGLE_API_KEY')
    cse_id = os.getenv('GOOGLE_CSE_ID')
    
    if not api_key or not cse_id:
        raise ValueError("API key or Custom Search Engine ID not found in environment variables")

    full_search_term = f"Recent news about {search_term}"
    
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cse_id,
        'q': full_search_term,
        'num': min(num_results, 10),  # Google API limits to 10 results per request
        'sort': 'date'  # Sort by date to get recent results
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'items' not in data:
            return []
            
        return [{
            'title': item.get('title', ''),
            'link': item.get('link', ''),
            'snippet': item.get('snippet', ''),
            'date': item.get('pagemap', {}).get('metatags', [{}])[0].get('article:published_time', '')
        } for item in data['items']]
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results: {e}")
        return [] 