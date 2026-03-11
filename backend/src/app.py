from fastapi import FastAPI,HTTPException,File,Form,UploadFile,Depends
from src.schemas import PostFormat

from src.db import Post,create_db_and_tables,get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield #wtf is yield?

app=FastAPI(lifespan=lifespan)

posts : dict = {
    1: {
        "title": "Billy Costigan infiltrates the criminal organization of Frank Costello",
        "content": "An undercover state trooper has successfully embedded himself within Costello's inner circle. The streets of South Boston are reaching a boiling point."
    },
    2: {
        "title": "330,000 French, British, Belgian and Dutch soldiers were safely evacuated from Dunkirk",
        "content": "A miracle on the beaches. Thousands of civilian vessels arrived today to bring our boys home across the Channel."
    },
    3: {
        "title": "Satriale's Pork Store sees mysterious increase in 'waste management' meetings",
        "content": "Locals report Tony Soprano and his associates have been spending extra hours at the deli. The gabagool is moving fast, but the tension is higher."
    },
    4: {
        "title": "Jack Rabbit Slim's hosts world-class twist contest tonight",
        "content": "Mia Wallace and Vincent Vega just took the stage. The $5 shakes are flowing, and the dance floor is electric."
    },
    5: {
        "title": "First rule of the local underground gathering is finally leaked",
        "content": "Someone broke the silence. Rumors of a basement fight club are spreading, but remember: you do not talk about it."
    },
    6: {
        "title": "LAPD searching for 'The K' following Replicant uprising rumors",
        "content": "Blade Runners are on high alert in the neon haze of 2049. A mysterious signal was detected near the ruins of Las Vegas."
    },
    7: {
        "title": "Henry Hill confirms: 'As far back as I can remember, I always wanted to be a gangster'",
        "content": "In a shocking local update, Hill has officially climbed the ranks of the Lucchese family. He's now a 'made' man in the neighborhood."
    },
    8: {
        "title": "Patrick Bateman recommends new morning routine for 'peak performance'",
        "content": "The Wall Street executive claims a 1,000-crunch workout and a honey almond body scrub are the keys to a balanced life. Check your reservations at Dorsia."
    },
    9: {
        "title": "Blue crystal substance reported to be '99.1% pure' in Albuquerque",
        "content": "A new player named Heisenberg has reportedly taken over the local market. DEA officials are baffled by the chemical perfection of the product."
    },
    10: {
        "title": "Rick's Café Américain remains the safest neutral ground in Casablanca",
        "content": "Despite the war, the gin is cold and Sam is playing 'As Time Goes By.' Everyone comes to Rick's, but nobody leaves without a story."
    }
}
'''new_post={
         "title":"Hugh Glass gets mauled by a wild bear",
         "content":"Forest hunting goes wrong as gypsy soldier gets brutally mauled by a wild bear like a rag doll . Despite severe injuries Mr.Glass survied"
         }'''

#* GET : query param is optional as a default value exists
#* POST : since we use a pydantic model as the fn argument , python automatically assumes it as the req body

@app.get("/feed")
async def get_posts(
    session:AsyncSession=Depends(get_async_session)
):
    results=await session.execute(select(Post).order_by(Post.created_at.desc()))

    posts=[row[0] for row in results.all()] #?why do we access row[0]
    posts_data=[]
    for post in posts:
        posts_data.append({
            "id":str(post.id),
            "caption":post.caption,
            "url":post.url,
            "file_type":post.file_type,
            "file_name":post.file_name,
            "created_at":post.created_at.isoformat()
        })

    return {"posts":posts_data}



@app.post("/upload")
async def upload_file(
    file:UploadFile=File(...),
    caption:str=Form(""),
    session:AsyncSession=Depends(get_async_session)
):
    post=Post(
        caption=caption,
        url="https://www.filmcomment.com/blog/david-thomson-the-revenant-alejandro-g-inarritu/",
        file_type="Article",
        file_name="Film Comment : The Revenant"
    )

    session.add(post)
    await session.commit()
    await session.refresh(post) #make sure default values [id,created_at] are created
    return post

    