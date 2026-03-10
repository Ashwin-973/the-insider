from fastapi import FastAPI,HTTPException
from src.schemas import PostFormat

app=FastAPI()

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

@app.get("/posts")
def get_posts(limit:int=None):  #query param is optional as a default value exists
    if limit:
        return list(posts.values())[:limit]
    return posts

@app.get("/posts/{id}")
def get_post_by_id(id:int)->PostFormat:
    if not posts.get(id):
        raise HTTPException(status_code=404,detail=f"Post with id:{id} not found")
    return posts.get(id)



@app.post("/posts")
def add_post(post:PostFormat)->PostFormat: #since we use a pydantic model as the fn argument , python automatically assumes it as the req body
    new_post={
         "title":post.title,
         "content":post.content
         }
    posts[max(posts)+1]=new_post
    return new_post


    