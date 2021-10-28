from fastapi import FastAPI
import scraping as sc 
from pydantic import BaseModel
import requestsDB as db1
import json
from bson import ObjectId

class Item(BaseModel):
    total_scrolls: int
    page_name:str
    url: str 

app=FastAPI()


#Service de scraping et d'ajout de données à la base de données Mongodb.
@app.post("/scrapingService/")
async def scrapingResults(item: Item):
    reslts =sc.scrape(item.total_scrolls,item.page_name,item.url)
    return reslts

@app.get("/allposts/")
async def allposts_():
    allPo=[]
    res= await db1.allposts()
    for post in res:
        Coment=[]
        for index,value in post.items():
            Coment.append({index:str(value)})
        allPo.append({'Comment':Coment})
    return allPo

@app.get("/allComments/")
async def allComments_():
    allCo=[]
    res= await db1.allcomments()
    for post in res:
        Coment=[]
        for index,value in post.items():
            Coment.append({index:str(value)})
        allCo.append({'Comment':Coment})
    return allCo

@app.get("/PageComments/{name}")
async def PageComments_(name):
    allCo=[]
    res=await db1.Pagecomments(name)
    for post in res:
        Coment=[]
        for index,value in post.items():
            Coment.append({index:str(value)})
        allCo.append({'Comment':Coment})
    return allCo 


@app.get("/Pageposts/{name}")
async def Pageposts_(name):
    allPo=[]
    res= await db1.Pageposts(name)
    for post in res:
        Post=[]
        for index,value in post.items():
            Post.append({index:str(value)})
        allPo.append({'Post':Post})
    return allPo 
