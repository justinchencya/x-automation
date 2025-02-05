from weibo_api.client import WeiboClient
from openai import OpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import List
# OpenAI API key
load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

# OpenAI client
openai_client = OpenAI(api_key=openai_api_key)

# Weibo client
weibo_client = WeiboClient()

def get_user_info(user_id):
    p = weibo_client.people(user_id)
    print(type(p.name))
    print(u"Username: {}".format(p.name))
    print(u"Description: {}".format(p.description))
    print(u"Number of people they follow: {}".format(p.follow_count))
    print(u"Number of followers: {}".format(p.followers_count))

def get_user_posts(user_id, pages=1):
    p = weibo_client.people(user_id)

    posts = []

    for post in p.statuses.page(pages):    
        posts.append(post)

    return posts

class PostTranslation(BaseModel):
  post_id: str
  original: str
  translated: str
  embedded_url: str

class PostsSummary(BaseModel):
  posts: List[PostTranslation]

def summarize_posts(posts, query):
    posts_str = ("=" * 50 + "\n").join([f"ID: {post.id} \n {post.text} \n" for post in posts])

    # print(posts_str)

    prompt = f"""
    Here are the posts:
    {posts_str}
    Here is the query:
    {query}
    """

    completion = openai_client.beta.chat.completions.parse(
        model='gpt-4o',
        messages=[
            {"role": "system", "content": "You are a helpful assistant that filters and summarizesposts based on a query."},
            {"role": "user", "content": prompt}
        ], 
        response_format=PostsSummary
    )

    return completion.choices[0].message.parsed

if __name__ == "__main__":
    # E.g. 6444741184
    user_id = input("User ID: ")

    get_user_info(user_id)

    posts = get_user_posts(user_id)

    # E.g. Find posts sharing AI tools and knowdge and are NOT announcement made by the poster himself. Translate into English to form a Twitter post. Extract and keep embedded URLs to the shared resources if exist.
    query = input("Query for summarizing posts: ")

    posts_summary = summarize_posts(posts, query)

    for post_translation in posts_summary.posts:
        print("=" * 50)
        print(f"ID: \n {post_translation.post_id}")
        print(f"Original: \n {post_translation.original}")
        print(f"Translated: \n {post_translation.translated}")
        print(f"Embedded URL: \n {post_translation.embedded_url}")