from weibo_utils import *
from post import *
import json
import random

WEIBO_USER_IDs = ['1727858283', '6444741184', '2192828333', '6083767801', '3894431038']

with open('data/posts_tweeted.json', 'r') as file:
    POSTS_TWEETED = json.load(file)

def tweet_post(post_translation):
    content = f"""
    {post_translation.translated}

    {post_translation.embedded_url}
    """

    # print("Will tweet:")
    # print(content)

    create_tweet(content)

    return content

if __name__ == "__main__":
    candidates = []

    for user_id in WEIBO_USER_IDs:
        posts = get_user_posts(user_id)

        query = """
        Please help me process the given weibo posts:
        - Find posts that share AI tools and knowledge, that are full posts (i.e. no 全文 expansions), and that are NOT announcement made by the poster himself. 
        - Translate into English to form a Twitter post. DO NOT include any links in the translated post.
        - Extract and keep embedded URLs to the shared resources, but make sure it is a valid URL. Otherwise, ignore it.
        - We will not be posting any image. So if there's any reference or mention of image in the original post, ignore it.
        """

        posts_summary = summarize_posts(posts, query)

        for post_translation in posts_summary.posts:
            if post_translation.post_id not in POSTS_TWEETED:
                print("=" * 50)
                print(f"ID: \n{post_translation.post_id}")
                print(f"Original: \n{post_translation.original}")
                print(f"Translated: \n{post_translation.translated}")
                print(f"Embedded URL: \n{post_translation.embedded_url}")

                candidates.append(post_translation)
            else:
                print(f"Post {post_translation.post_id} already tweeted.")

    if len(candidates) > 0:
        selected = random.choice(candidates)

        tweet_content = tweet_post(selected)

        POSTS_TWEETED[selected.post_id] = {
            "original": selected.original,
            "translated": selected.translated,
            "embedded_url": selected.embedded_url,
            "tweet_content": tweet_content
        }

        with open("data/posts_tweeted.json", "w") as f:
            json.dump(POSTS_TWEETED, f, indent=4)        
    else:
        print(f"Nothiong to tweet.")