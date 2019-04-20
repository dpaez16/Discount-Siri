import praw
from random import shuffle


CLIENT_ID = "i-2D8j2hde0q1A"
CLIENT_SECRET = "sX6N6vk8Kl8lsazPvA_eqZM5vA8"
USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0"


def url_filter(url):
    url_lower = url.lower()
    if ".jpg" in url_lower:
        return True
    elif ".png" in url_lower:
        return True
    elif ".jpeg" in url_lower:
        return True
    elif ".gif" in url_lower:
        return True
    elif ".gifv" in url_lower:
        return True
    else:
        return False


def get_random_memes():
    r = praw.Reddit(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    user_agent=USER_AGENT)

    page = r.subreddit('dankmemes')
    top_posts = page.hot(limit=50)
    
    meme_urls = list(map(lambda p: p.url, top_posts))
    meme_urls = list(filter(lambda u: url_filter(u), meme_urls))
    shuffle(meme_urls)

    return meme_urls, ""
