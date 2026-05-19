from fastapi import FastAPI ,Response   ,status ,HTTPException
from fastapi.params import Body
from httpx import post
import psycopg2
from pydantic import BaseModel
from typing import Optional
from random import randrange
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()
class Post(BaseModel):
    title: str
    content: str
    published: bool = True   

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='RIK@123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2) 



my_posts = [{"title": "post 1", "content": "content of post 1" ,"id": 1}, {"title": "post 2", "content": "content of post 2",  "id": 2},
            {"title": "post 3", "content": "content of post 3",  "id": 3},
            {"title": "post 4", "content": "content of post 4",  "id": 4}]



def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i       

@app.get("/")
def get_user():
    return {"message": "Hello Rik"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    # print(posts)
    return {"data": posts}

@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
   cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
   new_post = cursor.fetchone()
   conn.commit()
   return {"data": new_post}



@app.get("/posts/{id}")
def get_post(id: int , response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
  
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return {"post_detail " :post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post): 
    print(post)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}


