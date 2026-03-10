from fastapi import FastAPI,HTTPException

app=FastAPI()

posts={
    1:{
        "title":"Billy Costigan infiltrates the criminal organization of Frank Costello",
        "year":2006
    },
    2:{
        "title":"330,000 French, British, Belgian and Dutch soldiers were safely evacuated from dunkirk",
        "year":2017
    }
}


@app.get("/posts")
def get_posts():
    return posts

@app.get("/posts/{id}")
def get_post_by_id(id:int):
    if not posts.get(id):
        raise HTTPException(status_code=404,detail=f"Post with {id} not found")
    return posts.get(id)