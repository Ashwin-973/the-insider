from fastapi import FastAPI

app=FastAPI()

@app.get("/favorite-movies")
def favorite_movies():
    return {"movie1":"Fight Club","movie2":"Leon: The Professional"}