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

# Upload media
auth = tweepy.OAuth1UserHandler(
    consumer_key=api_key, consumer_secret=api_key_secret, access_token=access_token, access_token_secret=access_token_secret
)

api = tweepy.API(auth)

def upload_media(media_path):
    print(f"Uploading media: {media_path}...")
    media = api.media_upload(media_path)

    print(f"Media uploaded: {media.media_id}")
    print(f"Media expires in: {media.expires_after_secs} seconds")

    return media

def create_tweet_with_media(text, media_path):
    media = upload_media(media_path)
    client.create_tweet(text=text, media_ids=[media.media_id_string])  

if __name__ == "__main__":
    text = input("Enter the text to tweet: ")
    create_tweet(text)