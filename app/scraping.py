import getpass
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from bson.objectid import ObjectId
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


import sys
import time
import urllib.request
import os
import motor.motor_asyncio



driver = None
client1 = motor.motor_asyncio.AsyncIOMotorClient(os.environ["DB_URL"])
database = client1["facebook_data"]
postsCollection = database['posts_collection']
commentsCollection = database['comments_collection']

current_scrolls = 0
old_height = 0


post = { "_id" : None, "page_url" : None, "page_name" : None, "post" : None, "dateTime" : None, "NumLikes" : None, "ImagesLinks" : None }
comment = { "_id" : None, "page_url" : None, "page_name" : None , "comment" : None }


def driveCreation():
    try:
        global driver
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument('--window-size=1420,1080')

        try:
            driver = webdriver.Remote(command_executor="http://selenium:4444/wd/hub",desired_capabilities=DesiredCapabilities.FIREFOX)
            return True
        except:
            return False
            exit()
    except Exception as e:
        print(sys.exc_info()[0])
        exit() 


#Scroll over all the page given a specific number of scrolls
def scroll(total_scrolls):
    global old_height
    current_scrolls = 0

    while (True):
        try:
            if current_scrolls == total_scrolls:
                return
            old_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            current_scrolls += 1            
        except TimeoutException:
            break

    return

#scrape posts and comments of the given page url
def scrape(total_scrolls,page_name,url):
    try:
        
        PostsToreturn=[]
        commentsToreturn=[]
        res=driveCreation()
        time.sleep(5)
        driver.get(url)
        scroll(total_scrolls)
        time.sleep(3)
        posts=driver.find_elements_by_class_name('_427x')
        try:
            for idx,x in enumerate(posts):
                try:
                    text =x.find_element_by_class_name('_3576').text
                except:
                    text=""
                    pass
                try:
                    dateElement =x.find_element_by_class_name('timestampContent').text
                except:
                    dateElement=""
                    pass   
                try:
                    num_likes =x.find_element_by_class_name('_81hb').text
                except:
                    num_likes=""
                    pass 
                try:
                    links_For_Imgs= []
                    elems= x.find_elements_by_tag_name('img')
                    for ele in elems:
                        #clean , delete first element 
                        links_For_Imgs.append(ele.get_attribute("src"))
                except:
                    links_For_Imgs= []
                    pass
                try:
                    Comment=x.find_element_by_class_name('_3l3x').text
                except:
                    Comment=""
                    pass
                links_For_Imgs = links_For_Imgs[1:] if (len(links_For_Imgs)>0) else 0
                post["_id"] = ObjectId()
                post["page_name"] =  page_name
                post["page_url"] = url
                post["post"] = text
                post["dateTime"] = dateElement
                post["NumLikes"] = num_likes
                post["ImagesLinks"] = links_For_Imgs
                insertPost = postsCollection.insert_one(post)

                comment["_id"] = ObjectId()
                comment["comment"] = Comment
                comment["page_name"] = page_name
                comment["page_url"] = url
                post1 = { "_id" : idx, "page_url" : url, "page_name" : page_name, "post" : text, "dateTime" : dateElement, "NumLikes" : num_likes, "ImagesLinks" : links_For_Imgs }
                comment1 = { "_id" : idx, "page_url" : url, "page_name" : page_name , "comment" : Comment }
                PostsToreturn.append(post1)
                commentsToreturn.append(comment1)
                insertComm = commentsCollection.insert_one(comment)

            return {"Posts":PostsToreturn, "Comments":commentsToreturn}
        except WebDriverException:
            return 'error occured'
            print(sys.exc_info()[0])
            pass
    except Exception as e :
        return e 




#scrape()
