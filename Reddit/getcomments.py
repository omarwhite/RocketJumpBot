import os
import praw

NUM_COMMENTS = 10

# Getting the Reddit API key from Environment Variables
secret = os.getenv('redditToken')

# Accessing the Reddit API
reddit = praw.Reddit(
    client_id="N7wAzy6ETjA4YaY_VIDOYA",
    client_secret=secret,
    user_agent="Rocket Jump Bot"
)

# Function to get the top 10 comments of a post
def getTop10Comments(url):
    # Loading the post
    post = reddit.submission(url=url)

    # Loading post comments
    post.comments.replace_more(limit=0)  # Load all comments without truncating

    # Filter for top-level comments only (comments whose parent is the post itself)
    top_level_comments = [
        comment for comment in post.comments 
        if comment.parent_id == post.name and comment.body not in ["[deleted]", "[removed]"]
    ]

    # Return the top 10 top-level comments
    return top_level_comments[:NUM_COMMENTS]
