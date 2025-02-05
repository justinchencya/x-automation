from weibo_utils import *
from post import *
import json

WEIBO_USER_IDs = ['1727858283', '6444741184']

with open('data/posts_tweeted.json', 'r') as file:
    POSTS_TWEETED = json.load(file)

if __name__ == "__main__":
    for user_id in WEIBO_USER_IDs:
        posts = get_user_posts(user_id)

        query = "Find posts sharing AI tools and knowdge and are NOT announcement made by the poster himself. Translate into English to form a Twitter post. Extract and keep embedded URLs to the shared resources if exist."
        posts_summary = summarize_posts(posts, query)

        for post_translation in posts_summary.posts:
            if post_translation.post_id not in POSTS_TWEETED:
                print("=" * 50)
                print(f"ID: \n {post_translation.post_id}")
                print(f"Original: \n {post_translation.original}")
                print(f"Translated: \n {post_translation.translated}")
                print(f"Embedded URL: \n {post_translation.embedded_url}")

                POSTS_TWEETED[post_translation.post_id] = {
                    "original": post_translation.original,
                    "translated": post_translation.translated,
                    "embedded_url": post_translation.embedded_url
                }
            else:
                print(f"Post {post_translation.post_id} already tweeted.")

    with open("data/posts_tweeted.json", "w") as f:
        json.dump(POSTS_TWEETED, f, indent=4)