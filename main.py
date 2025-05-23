from weibo_utils import *
from post import *
import json
import random

WEIBO_USER_IDs = ['1727858283', '6444741184', '2192828333', '6083767801', '3894431038']

with open('data/posts_tweeted.json', 'r', encoding='utf-8') as file:
    POSTS_TWEETED = json.load(file)

def tweet_post(reviewed_processed_post):
    content = reviewed_processed_post.refined_with_url
    create_tweet(content)

    return content

if __name__ == "__main__":
    candidates = []

    for user_id in WEIBO_USER_IDs:
        print(f"Processing user {user_id}...")
        posts = get_user_posts(user_id)

        for post in posts:
            if post.id not in POSTS_TWEETED:
                review = review_original_post(post)

                if not review.is_reply_or_forward and not review.time_sensitive and review.ai_related and review.nonpersonal_knowledge_sharing_content and not review.for_chinese_audience_only and review.full_post:
                    # print("=" * 50)
                    # print("Original Post:")
                    # print(post.text)

                    # print('\n')
                    processed_post = process_post(post)
                    # print("Processed Post:") 
                    # print(processed_post.translated)
                    # print(processed_post.embedded_url)

                    if processed_post.embedded_url is not None:
                        processed_url = process_url(processed_post.embedded_url)
                    else:
                        processed_url = None

                    # print('\n')
                    reviewed_processed_post = review_processed_post(processed_post, processed_url)
                    # print("Reviewed Post:")
                    # print(reviewed_processed_post.refined_with_url)

                    print(f"Adding post {post.id} to candidates...")
                    candidates.append(reviewed_processed_post)

    if len(candidates) > 0:
        selected = random.choice(candidates)

        tweet_content = tweet_post(selected)

        print(f"Tweeting:")
        print(tweet_content)

        # print('\n')
        # print("Original Post:")
        # print(selected.original)
        # print("Processed Post:")
        # print(selected.processed)
        # print("Reviewed Post with URL:")
        # print(selected.refined_with_url)

        POSTS_TWEETED[selected.post_id] = {
            "original": selected.original,
            "processed": selected.processed,
            "refined_with_url": selected.refined_with_url
        }

        with open("data/posts_tweeted.json", "w", encoding='utf-8') as f:
            json.dump(POSTS_TWEETED, f, ensure_ascii=False, indent=4)        
    else:
        print(f"Nothiong to tweet.")