from fastapi import FastAPI
from fastapi.params import Body
from httpx import post
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()
class Post(BaseModel):
    title: str
    content: str
    published: bool = True   
    rating:Optional[int] = None

my_posts = [{"title": "post 1", "content": "content of post 1" ,"id": 1}, {"title": "post 2", "content": "content of post 2",  "id": 2},
            {"title": "post 3", "content": "content of post 3",  "id": 3}]

@app.get("/")
def get_user():
    return {"message": "Hello Rik"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/createpost")
def create_post(post: Post):
   post_dict = post.dict()
   post_dict["id"] = randrange(0, 1000000)
   my_posts.append(post_dict )
   return {"data": post_dict}




