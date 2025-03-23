import os
from dotenv import load_dotenv
import openai
from typing import List, Dict, Any
from fetch_google_results import fetch_google_search_results
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
                {"role": "system", "content": """You are a precise data extraction assistant. Your task is to:
1. Extract individual, distinct insights from the provided news articles
2. For each insight:
   - Write a clear, concise statement of one specific fact or development
   - Include the source article's title and link
   - Ensure each insight is self-contained and specific
3. Format your response as a JSON array of objects, where each object has:
   - 'insight': The specific fact or development
   - 'source_title': The title of the source article
   - 'source_link': The URL of the source article
4. Focus on recent developments and specific facts rather than general information
5. Ensure each insight is unique and not repeated across articles"""},
                {"role": "user", "content": f"Please extract individual insights from these news articles about {search_term}:\n\n{content}"}
            ],
            max_tokens=1000,
            temperature=0.3  # Lower temperature for more consistent, factual output
        )
        
        # Parse the JSON response
        insights = json.loads(response.choices[0].message.content)
        return insights
    except Exception as e:
        print(f"Error generating insights: {e}")
        return []

def save_insights(insights: List[Dict[str, Any]], search_term: str):
    """
    Save insights to both JSON and CSV files.
    """
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
    
    # Save insights to files
    save_insights(insights, search_term)
    
    return insights

# Example usage
if __name__ == "__main__":
    search_term = "artificial intelligence"
    print(f"\nGenerating insights for: {search_term}\n")
    insights = get_news_insights(search_term, 5)
    
    # Print insights to console
    print("\nGenerated Insights:")
    for i, insight in enumerate(insights, 1):
        print(f"\n{i}. {insight['insight']}")
        print(f"   Source: {insight['source_title']}")
        print(f"   Link: {insight['source_link']}") 