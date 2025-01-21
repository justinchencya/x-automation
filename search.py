import tweepy
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Get environment variables
bearer_token = os.getenv('X_BEARER_TOKEN')

# Create client with OAuth2 access token
client = tweepy.Client(bearer_token=bearer_token)

# Search for tweets
def search_recent_tweets(search_window_min, query, max_results):
  """
  search_window_min: int, duration of the search window in minutes, measured backward from the current timestamp
  query: str, query to search
  max_results: int, number of results to return from search
  """

  end_time = datetime.now()
  start_time = end_time - timedelta(minutes=search_window_min)

  # Format dates in RFC3339 format (ISO 8601)
  start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
  end_time = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

  results = client.search_recent_tweets(
      start_time=start_time, 
      end_time=end_time, 
      query=query, 
      max_results=max_results, 
      tweet_fields=['author_id', 'lang', 'public_metrics'], 
      sort_order='relevancy')

  df_results = pd.DataFrame({
      'id': [d.id for d in results.data],
      'text': [d.text for d in results.data],
      'author_id': [d.author_id for d in results.data],
      'lang': [d.lang for d in results.data],
      'retweet_count': [d.public_metrics['retweet_count'] for d in results.data],
      'reply_count': [d.public_metrics['reply_count'] for d in results.data],
      'like_count': [d.public_metrics['like_count'] for d in results.data],
      'quote_count': [d.public_metrics['quote_count'] for d in results.data],
      'bookmark_count': [d.public_metrics['bookmark_count'] for d in results.data],
      'impression_count': [d.public_metrics['impression_count'] for d in results.data],
  })

  return df_results

if __name__ == "__main__":
    search_window_min = int(input("Enter the search window in minutes: "))
    query = input("Enter the query to search: ")
    max_results = int(input("Enter the maximum number of results to return: "))
    df_results = search_recent_tweets(search_window_min, query, max_results)
    print(df_results)