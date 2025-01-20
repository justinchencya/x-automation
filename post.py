import tweepy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables
api_key = os.getenv('X_API_KEY')
api_key_secret = os.getenv('X_API_KEY_SECRET')
access_token = os.getenv('X_ACCESS_TOKEN')
access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')

# Create client with OAuth2 access token
client = tweepy.Client(consumer_key=api_key, consumer_secret=api_key_secret, access_token=access_token, access_token_secret=access_token_secret)

# Create tweet
def create_tweet(text):
    client.create_tweet(text=text)

if __name__ == "__main__":
    text = input("Enter the text to tweet: ")
    create_tweet(text)