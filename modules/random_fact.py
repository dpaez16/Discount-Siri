import praw
from random import shuffle


CLIENT_ID = "i-2D8j2hde0q1A"
CLIENT_SECRET = "sX6N6vk8Kl8lsazPvA_eqZM5vA8"
USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0"


def get_random_fact():
    r = praw.Reddit(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    user_agent=USER_AGENT)

    page = r.subreddit('todayilearned')
    top_posts = page.hot(limit=50)
    
    meme_urls = list(map(lambda p: p.title, top_posts))[2:]
    shuffle(meme_urls)

    return meme_urls[0]
