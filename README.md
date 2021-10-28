#  FastAPI scraper
## Explanation of services


The goal of this application is to scrape posts and comments of a public facebook page.
The tools used to achieve that goal are :

- Selenium 
- MongoDB
- Docker

## The input of scraper() service

- "total_scrolls" : the number of scrolls for a page to scrape.
- "page_name" : a name of the page to specify for the posts and comments.
- "Url" : url of the page to scrape. `PS: Url should be in that form `
- ```{page_url}/posts``` 

## the mongoDB services 

You could use those services to select the data of a specific facebook page 
or to look for all of the data. Two collections are created, one for posts an the other for 
comments.