import praw
from random import shuffle


CLIENT_ID = "i-2D8j2hde0q1A"
CLIENT_SECRET = "sX6N6vk8Kl8lsazPvA_eqZM5vA8"
USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0"


def get_random_shower_thought():
    r = praw.Reddit(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    user_agent=USER_AGENT)

    page = r.subreddit('showerthoughts')
    top_posts = page.hot(limit=50)
    
    thoughts = list(map(lambda p: p.title, top_posts))[2:]
    shuffle(thoughts)

    return thoughts[0]