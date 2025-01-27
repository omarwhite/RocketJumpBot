from Reddit.getcomments import *
from dbtests import grabTestPost

# Grabbing a random url
url = grabTestPost()["url"]

# Getting comments from post
commentList = getTop10Comments(url)

# Displaying comments from post
for i, comment in enumerate(commentList, start=1):
    print(f"Comment {i}: {comment.body}")