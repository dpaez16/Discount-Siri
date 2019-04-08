import praw
from random import shuffle


CLIENT_ID = "i-2D8j2hde0q1A"
CLIENT_SECRET = "sX6N6vk8Kl8lsazPvA_eqZM5vA8"
USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0"


def url_filter(url):
    url_lower = url.lower()
    if ".jpg" in url_lower:
        return url
    elif ".png" in url_lower:
        return url
    elif ".jpeg" in url_lower:
        return url
    elif ".gif" in url_lower:
        return url
    elif ".gifv" in url_lower:
        return url
    else:
        return None


def get_front_page_preview():
    r = praw.Reddit(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    user_agent=USER_AGENT)

    page = r.subreddit('all')
    top_posts = page.hot(limit=20)
    
    front_page_preview = []

    for post in top_posts:
        processed_post = {
            'subreddit': "r/{}".format(post.subreddit),
            'title': post.title,
            'preview_url': url_filter(post.url),
            'post_link': "reddit.com" + post.permalink,
            'upvotes': post.ups
        }

        front_page_preview.append(processed_post)
    
    return front_page_preview