from weibo_api.client import WeiboClient
from openai import OpenAI
from dotenv import load_dotenv
import os

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

def summarize_posts(posts, query):
    posts_str = ("=" * 50 + "\n").join([post.text for post in posts])

    prompt = f"""
    Here are the posts:
    {posts_str}
    Here is the query:
    {query}
    """

    completion = openai_client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {"role": "system", "content": "You are a helpful assistant that filters and summarizesposts based on a query."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message

if __name__ == "__main__":
    user_id = input("User ID: ")

    get_user_info(user_id)

    posts = get_user_posts(user_id)

    query = input("Query for summarizing posts: ")

    print(summarize_posts(posts, query))