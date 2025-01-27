from Database.mongodbconn import *

# Declaring a test post and video
test_post = getRandomPost()
test_vid = getRandomVid()

# Testing the ability to grab a random post from the database
print(test_post)

# Formatting for readability
print("///////////////////////////////////////////////////")

# Testing the ability to grab a random video from the database
print(test_vid)

print("///////////////////////////////////////////////////")

# Printing out the information that will be used from the data
print(test_post["title"], test_post["url"])
print(test_vid["snippet"]["title"], 
      test_vid["snippet"]["videoOwnerChannelTitle"],
      test_vid["snippet"]["resourceId"]["videoId"])

def grabTestPost():
    return test_post

def grabTestVid():
    return test_vid