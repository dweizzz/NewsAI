import os
from dotenv import load_dotenv
import openai
from typing import List, Dict, Any
from .fetch_google_results import fetch_google_search_results
import json
import csv
from datetime import datetime

# Load environment variables
load_dotenv()

def summarize_with_openai(articles: List[Dict[str, Any]], search_term: str) -> List[Dict[str, Any]]:
    """
    Use OpenAI to extract individual insights from articles.
    
    Args:
        articles (List[Dict[str, Any]]): List of articles with title, link, snippet, and date
        search_term (str): The search term used to find the articles
    
    Returns:
        List[Dict[str, Any]]: List of insights with their sources
    """
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    if not openai.api_key:
        raise ValueError("OpenAI API key not found in environment variables")
    
    # Prepare the content for analysis
    content = f"Here are recent news articles about '{search_term}':\n\n"
    for i, article in enumerate(articles):
        content += f"Article {i+1}:\n"
        content += f"Title: {article['title']}\n"
        content += f"Summary: {article['snippet']}\n"
        if article.get('date'):
            content += f"Date: {article['date']}\n"
        content += f"Link: {article['link']}\n\n"
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a precise data extraction assistant. Your task is to extract individual insights from news articles and format them as a JSON array.

IMPORTANT: Your response must be a valid JSON array containing objects. Each object must have exactly these fields:
- insight: A clear, concise statement of one specific fact or development
- source_title: The title of the source article
- source_link: The URL of the source article

Example format:
[
  {
    "insight": "OpenAI released GPT-4 with improved capabilities",
    "source_title": "OpenAI Announces GPT-4",
    "source_link": "https://example.com/article1"
  },
  {
    "insight": "Google's AI model achieved 90% accuracy in medical diagnosis",
    "source_title": "Google AI Breakthrough in Healthcare",
    "source_link": "https://example.com/article2"
  }
]

Guidelines:
1. Extract specific, factual insights
2. Include source information for each insight
3. Ensure each insight is unique
4. Focus on recent developments
5. Keep insights concise and clear"""},
                {"role": "user", "content": f"Please extract individual insights from these news articles about {search_term} and format them as a JSON array:\n\n{content}"}
            ],
            max_tokens=1000,
            temperature=0.3  # Lower temperature for more consistent, factual output
        )
        
        # Get the response content
        response_content = response.choices[0].message.content.strip()
        
        # Try to parse the JSON response
        try:
            insights = json.loads(response_content)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print("Raw response:", response_content)
            return []
            
        # Validate the structure
        if not isinstance(insights, list):
            print("Error: Response is not a JSON array")
            return []
            
        # Validate each insight has required fields
        valid_insights = []
        for insight in insights:
            if all(key in insight for key in ['insight', 'source_title', 'source_link']):
                valid_insights.append(insight)
            else:
                print(f"Warning: Skipping invalid insight structure: {insight}")
                
        return valid_insights
        
    except Exception as e:
        print(f"Error generating insights: {e}")
        return []

def save_insights(insights: List[Dict[str, Any]], search_term: str):
    """
    Save insights to both JSON and CSV files.
    """
    if not insights:
        print("No valid insights to save")
        return
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save as JSON
    json_filename = f"insights_{search_term.replace(' ', '_')}_{timestamp}.json"
    with open(json_filename, 'w') as f:
        json.dump(insights, f, indent=2)
    print(f"Saved insights to {json_filename}")
    
    # Save as CSV
    csv_filename = f"insights_{search_term.replace(' ', '_')}_{timestamp}.csv"
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['insight', 'source_title', 'source_link'])
        writer.writeheader()
        writer.writerows(insights)
    print(f"Saved insights to {csv_filename}")

def get_news_insights(search_term: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Main function to fetch news and generate structured insights.
    
    Args:
        search_term (str): The search term to find news about
        num_results (int): Number of articles to fetch and analyze
    
    Returns:
        List[Dict[str, Any]]: List of insights with their sources
    """
    # Fetch search results
    results = fetch_google_search_results(search_term, num_results)
    
    if not results:
        print(f"No recent news found for '{search_term}'")
        return []
    
    # Generate insights using OpenAI
    insights = summarize_with_openai(results, search_term)
    
    if insights:
        # Save insights to files
        save_insights(insights, search_term)
    else:
        print("No valid insights were generated")
    
    return insights

# Example usage
if __name__ == "__main__":
    search_term = "artificial intelligence"
    print(f"\nGenerating insights for: {search_term}\n")
    insights = get_news_insights(search_term, 5)
    
    # Print insights to console
    if insights:
        print("\nGenerated Insights:")
        for i, insight in enumerate(insights, 1):
            print(f"\n{i}. {insight['insight']}")
            print(f"   Source: {insight['source_title']}")
            print(f"   Link: {insight['source_link']}")
    else:
        print("No insights were generated") 