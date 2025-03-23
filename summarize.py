import os
from dotenv import load_dotenv
import openai
from typing import List, Dict, Any
from fetch_google_results import fetch_google_search_results

# Load environment variables
load_dotenv()

def summarize_with_openai(articles: List[Dict[str, Any]], search_term: str) -> str:
    """
    Use OpenAI to summarize the articles.
    
    Args:
        articles (List[Dict[str, Any]]): List of articles with title, link, snippet, and date
        search_term (str): The search term used to find the articles
    
    Returns:
        str: A bullet-point summary of the articles
    """
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    if not openai.api_key:
        raise ValueError("OpenAI API key not found in environment variables")
    
    # Prepare the content for summarization
    content = f"Here are recent news articles about '{search_term}':\n\n"
    for article in articles:
        content += f"Title: {article['title']}\n"
        content += f"Summary: {article['snippet']}\n"
        if article.get('date'):
            content += f"Date: {article['date']}\n"
        content += "\n"
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates concise bullet-point summaries of news articles. Focus on the most important information and recent developments."},
                {"role": "user", "content": f"Please provide a bullet-point summary of the following news articles about {search_term}:\n\n{content}"}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Error generating summary"

def get_news_summary(search_term: str, num_results: int = 5) -> str:
    """
    Main function to fetch news and generate a summary.
    
    Args:
        search_term (str): The search term to find news about
        num_results (int): Number of articles to fetch and summarize
    
    Returns:
        str: A bullet-point summary of the news articles
    """
    # Fetch search results
    results = fetch_google_search_results(search_term, num_results)
    
    if not results:
        return f"No recent news found for '{search_term}'"
    
    # Generate summary using OpenAI
    summary = summarize_with_openai(results, search_term)
    return summary

# Example usage
if __name__ == "__main__":
    search_term = "artificial intelligence"
    print(f"\nGenerating news summary for: {search_term}\n")
    summary = get_news_summary(search_term, 5)
    print(summary) 