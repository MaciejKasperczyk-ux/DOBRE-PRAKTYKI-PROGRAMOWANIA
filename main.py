import json
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db import SessionLocal, Base, engine
from models import Movie, Link, Rating, Tag

app = FastAPI()

# tworzymy tabele przy starcie (jeśli jeszcze nie ma)
Base.metadata.create_all(bind=engine)


# dependency do sesji DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/movies")
def read_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    result = []
    for m in movies:
        result.append({
            "movieId": m.movieId,
            "title": m.title,
            "genres": m.genres
        })
    return result


@app.get("/links")
def read_links(db: Session = Depends(get_db)):
    links = db.query(Link).all()
    result = []
    for l in links:
        result.append({
            "movieId": l.movieId,
            "imdbId": l.imdbId,
            "tmdbId": l.tmdbId
        })
    return result


@app.get("/ratings")
def read_ratings(db: Session = Depends(get_db)):
    ratings = db.query(Rating).all()
    result = []
    for r in ratings:
        result.append({
            "userId": r.userId,
            "movieId": r.movieId,
            "rating": r.rating,
            "timestamp": r.timestamp
        })
    return result


@app.get("/tags")
def read_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    result = []
    for t in tags:
        result.append({
            "userId": t.userId,
            "movieId": t.movieId,
            "tag": t.tag,
            "timestamp": t.timestamp
        })
    return result
