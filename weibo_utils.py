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

class originalPostReview(BaseModel):
    post_id: str
    is_reply_or_forward: bool
    ai_related: bool
    nonpersonal_knowledge_sharing_content: bool
    for_chinese_audience_only: bool
    contains_link: bool
    full_post: bool

def review_original_post(post):
    prompt = f"""
    Please review the following post in reference to the following questions.

    Criteria:
    ---
    - Is the post a reply or forward?
    - Is the post about AI (e.g., news, reviews, tools)?
    - Is the post a knowledge sharing post rather than an announcement or subjective opinion made by the poster about themselves or their own accounts?
    - Is the post for a Chinese audience (i.e. sharing tools or resources that only Chinese people use, such as Baidu, Weibo, Feishu, BiliBili, etc.)?
    - Does the post contain any links to external resources?
    - Is the post a full post (not expandable)?
    ---

    Post:
    ID: {post.id}
    Text: {post.text}
    ---
    """

    completion = openai_client.beta.chat.completions.parse(
        model='gpt-4o',
        messages=[
            {"role": "system", "content": "You are a helpful assistant that helps review social media posts as instructed."},
            {"role": "user", "content": prompt}
        ], 
        response_format=originalPostReview
    )   

    return completion.choices[0].message.parsed

class ProcessedPost(BaseModel):
  post_id: str
  original: str
  translated: str
  embedded_url: str

def process_post(post):
    prompt = f"""
    Please help me process the following weibo post in the following steps:
    - Translate the post into English.
    - Identify and extract embedded URLs to the shared resources if exist, chopping off any prefixes like https://weibo.cn/sinaurl.
    - Remove any hashtags from the post.

    Post:
    ---
    Post ID: {post.id}
    Post Text: {post.text}
    ---
    """

    completion = openai_client.beta.chat.completions.parse(
        model='gpt-4o',
        messages=[
            {"role": "system", "content": "You are a helpful assistant that helps process social media posts as instructed."},
            {"role": "user", "content": prompt}
        ], 
        response_format=ProcessedPost
    )

    processed_post = completion.choices[0].message.parsed

    return processed_post

class ReviewedProcessedPost(BaseModel):
  post_id: str
  original: str
  processed: str
  refined_with_url: str

def review_processed_post(processed_post):
    prompt = f"""
    Please review the following post in reference to the criteria listed below. Please fix any issues if necessary.

    Criteria:
    ---
    - The post is all in English.
    - The post doesn't contain any markdown formatting, especially for links. In otherwords, there should be nothing like [Web Link]; if there is a link, the link should just be attached directly.
    - The post doesn't have any formatting issues, such as extra spaces or newlines.
    ---

    Post ID: 
    ---
    {processed_post.post_id}
    ---

    Original Post:
    {processed_post.original}

    Processed Post:
    {processed_post.translated}
    {processed_post.embedded_url}
    ---

    Just return the refined post, with URL if exists, without any other text.
    """

    completion = openai_client.beta.chat.completions.parse(
        model='gpt-4o',
        messages=[
            {"role": "system", "content": "You are a helpful assistant that helps review social media posts as instructed."},
            {"role": "user", "content": prompt}
        ],
        response_format=ReviewedProcessedPost
    )

    reviewed_processed_post = completion.choices[0].message.parsed

    return reviewed_processed_post

if __name__ == "__main__":
    user_id = "6444741184"
    posts = get_user_posts(user_id)

    for post in posts:
        review = review_original_post(post)

        if not review.is_reply_or_forward and review.ai_related and review.nonpersonal_knowledge_sharing_content and not review.for_chinese_audience_only and review.full_post:
            # print("=" * 50)
            # print("Original Post:")
            # print(post.text)

            # print('\n')
            processed_post = process_post(post)
            # print("Processed Post:") 
            # print(processed_post.translated)
            # print(processed_post.embedded_url)

            print('\n')
            reviewed_processed_post = review_processed_post(processed_post)
            print("Original Post:")
            print(reviewed_processed_post.original)
            print("Processed Post:")
            print(reviewed_processed_post.processed)
            print("Reviewed Post with URL:")
            print(reviewed_processed_post.refined_with_url)