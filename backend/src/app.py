import shutil
import os
import tempfile
import uuid

from fastapi import FastAPI,HTTPException,File,Form,UploadFile,Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager
import imagekitio

from src.schemas import PostFormat,UserRead,UserCreate,UserUpdate
from src.db import Post,create_db_and_tables,get_async_session,User
from src.images import imagekit
from src.users import auth_backend,current_active_user,fastapi_users
#!from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions >>deprecated


@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield #wtf is yield?

app=FastAPI(lifespan=lifespan)

origins=[
    "http://localhost:8501"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(fastapi_users.get_auth_router(auth_backend),prefix="/auth/jwt",tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead,UserCreate),prefix="/auth",tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(),prefix="/auth",tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead),prefix="/auth",tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead,UserUpdate),prefix="/users",tags=["users"])

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


@app.get("/")
async def greeting():
    return {"success":True,"message":"I Do Wish We Could Chat Longer, But I'm Having An Old Friend For Dinner"}


@app.get("/feed")
async def get_posts(
    session:AsyncSession=Depends(get_async_session),
    user:User=Depends(current_active_user),
):
    results=await session.execute(select(Post).order_by(Post.created_at.desc()))

    posts=[row[0] for row in results.all()] #?why do we access row[0]
    posts_data=[]

    user_data=await session.execute(select(User))
    users=[row[0] for row in user_data.all()]
    user_dict={user.id:user.email for user in users}

    for post in posts:
        posts_data.append({
            "id":str(post.id),
            "user":str(post.user_id),
            "caption":post.caption,
            "url":post.url,
            "file_type":post.file_type,
            "file_name":post.file_name,
            "created_at":post.created_at.isoformat(),
            "is_owner":post.user_id==user.id,
            "email":user_dict.get(post.user_id,"Unknown User")
        })

    return {"posts":posts_data}



@app.post("/upload")
async def upload_file(
    file:UploadFile=File(...),
    caption:str=Form(""),
    user:User=Depends(current_active_user),
    session:AsyncSession=Depends(get_async_session)
):
    temp_file_path=None

    try:
        with tempfile.NamedTemporaryFile(delete=False,suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path=temp_file.name
            shutil.copyfileobj(file.file,temp_file)

        with open(temp_file_path,"rb") as uploaded_file:
            upload_result=imagekit.files.upload(
                file=uploaded_file,
                file_name=file.filename,
                use_unique_file_name=True,
                tags=["backend-upload"]
            )


        post=Post(
            user_id=user.id,
            caption=caption,
            url=upload_result.url,
            file_type="video" if file.content_type.startswith("video/") else "image",
            file_name=upload_result.name
        )

        session.add(post)
        await session.commit()
        await session.refresh(post) #make sure default values [id,created_at] are created
        return post

    except Exception as err:
        raise HTTPException(status_code=500,detail=str(err))
    except imagekitio.APIConnectionError as err:
        raise HTTPException(status_code=500,detail=str(err)) 
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close() #?is it await file.close()
    

@app.delete("/posts/{post_id}")
async def delete_post(
    post_id:str,
    user:User=Depends(current_active_user),
    session:AsyncSession=Depends(get_async_session)
    ):
    try:

        post_uuid=uuid.UUID(post_id)

        result=await session.execute(select(Post).where(Post.id==post_uuid))
        post=result.scalars().first()

        if not post:
            raise HTTPException(status_code=404,detail="post not found")
        
        if post.user_id!=user.id:
            raise HTTPException(status_code=403,detail="you don't have permission to delete this post")
        
        await session.delete(post)
        await session.commit()

        return {"success":True,"message":"deletion successful"}
    except Exception as err:
        raise HTTPException(status_code=500,detail=str(err))



    