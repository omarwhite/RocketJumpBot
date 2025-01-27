from pymongo import *
import os

link = os.getenv('MongoLink')

client = MongoClient(link)
db = client['TikTokBotDB']
post_collection = db['AskRedditThreads']
vid_collection = db['JumpVideos']

def getRandomPost():
    random_post = post_collection.aggregate([{ '$sample': { 'size': 1 } }]).next()
    return random_post

def getRandomVid():
    random_vid = vid_collection.aggregate([{ '$sample': { 'size': 1 } }]).next()
    return random_vid