import os
import motor.motor_asyncio


client1 = motor.motor_asyncio.AsyncIOMotorClient(os.environ["DB_URL"])
database = client1["facebook_data"]
postsCollection = database['posts_collection']
commentsCollection = database['comments_collection']


def allposts():
    return postsCollection.find().to_list(50000)

def allcomments():
    return commentsCollection.find().to_list(50000)

def Pageposts(name):
    return postsCollection.find({"page_name":name}).to_list(50000)
    
def Pagecomments(name):
    return commentsCollection.find({"page_name":name}).to_list(50000)
