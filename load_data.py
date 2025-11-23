# main.py
import json
from typing import Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import Base, engine, SessionLocal
from models import Movie, Link, Rating, Tag

app = FastAPI()

# Tworzymy tabele w bazie, jeśli jeszcze nie istnieją
Base.metadata.create_all(bind=engine)


# ------------ DB SESSION DEPENDENCY ------------

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------ HELPERY DO SERIALIZACJI ------------

def movie_to_dict(m: Movie) -> dict:
    return {
        "id": m.id,
        "movieId": m.movieId,
        "title": m.title,
        "genres": m.genres,
    }


def link_to_dict(l: Link) -> dict:
    return {
        "id": l.id,
        "movieId": l.movieId,
        "imdbId": l.imdbId,
        "tmdbId": l.tmdbId,
    }


def rating_to_dict(r: Rating) -> dict:
    return {
        "id": r.id,
        "userId": r.userId,
        "movieId": r.movieId,
        "rating": r.rating,
        "timestamp": r.timestamp,
    }


def tag_to_dict(t: Tag) -> dict:
    return {
        "id": t.id,
        "userId": t.userId,
        "movieId": t.movieId,
        "tag": t.tag,
        "timestamp": t.timestamp,
    }


# ------------ ROOT ------------

@app.get("/")
def read_root():
    return {"Hello": "World"}


# =================================================
#                    MOVIES
# =================================================

# READ – lista
@app.get("/movies")
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    return [movie_to_dict(m) for m in movies]


# CREATE – POST
@app.post("/movies", status_code=201)
def create_movie(movie: dict, db: Session = Depends(get_db)):
    new_movie = Movie(
        movieId=movie["movieId"],
        title=movie["title"],
        genres=movie["genres"],
    )
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return movie_to_dict(new_movie)


# READ – pojedynczy
@app.get("/movies/{movie_id}")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie_to_dict(movie)


# UPDATE – PUT
@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie_data: dict, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie.title = movie_data.get("title", movie.title)
    movie.genres = movie_data.get("genres", movie.genres)

    db.commit()
    db.refresh(movie)
    return movie_to_dict(movie)


# DELETE
@app.delete("/movies/{movie_id}", status_code=204)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(movie)
    db.commit()
    return


# =================================================
#                    LINKS
# =================================================

# READ – lista
@app.get("/links")
def get_links(db: Session = Depends(get_db)):
    links = db.query(Link).all()
    return [link_to_dict(l) for l in links]


# CREATE – POST
@app.post("/links", status_code=201)
def create_link(link: dict, db: Session = Depends(get_db)):
    new_link = Link(
        movieId=link["movieId"],
        imdbId=link["imdbId"],
        tmdbId=link["tmdbId"],
    )
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return link_to_dict(new_link)


# READ – pojedynczy (po PRIMARY KEY id)
@app.get("/links/{link_id}")
def get_link(link_id: int, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link_to_dict(link)


# UPDATE – PUT
@app.put("/links/{link_id}")
def update_link(link_id: int, link_data: dict, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    link.movieId = link_data.get("movieId", link.movieId)
    link.imdbId = link_data.get("imdbId", link.imdbId)
    link.tmdbId = link_data.get("tmdbId", link.tmdbId)

    db.commit()
    db.refresh(link)
    return link_to_dict(link)


# DELETE
@app.delete("/links/{link_id}", status_code=204)
def delete_link(link_id: int, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    db.delete(link)
    db.commit()
    return


# =================================================
#                    RATINGS
# =================================================

# READ – lista
@app.get("/ratings")
def get_ratings(db: Session = Depends(get_db)):
    ratings = db.query(Rating).all()
    return [rating_to_dict(r) for r in ratings]


# CREATE – POST
@app.post("/ratings", status_code=201)
def create_rating(rating: dict, db: Session = Depends(get_db)):
    new_rating = Rating(
        userId=rating["userId"],
        movieId=rating["movieId"],
        rating=rating["rating"],
        timestamp=rating["timestamp"],
    )
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return rating_to_dict(new_rating)


# READ – pojedynczy
@app.get("/ratings/{rating_id}")
def get_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating_to_dict(rating)


# UPDATE – PUT
@app.put("/ratings/{rating_id}")
def update_rating(rating_id: int, rating_data: dict, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    rating.userId = rating_data.get("userId", rating.userId)
    rating.movieId = rating_data.get("movieId", rating.movieId)
    rating.rating = rating_data.get("rating", rating.rating)
    rating.timestamp = rating_data.get("timestamp", rating.timestamp)

    db.commit()
    db.refresh(rating)
    return rating_to_dict(rating)


# DELETE
@app.delete("/ratings/{rating_id}", status_code=204)
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    db.delete(rating)
    db.commit()
    return


# =================================================
#                      TAGS
# =================================================

# READ – lista
@app.get("/tags")
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    return [tag_to_dict(t) for t in tags]


# CREATE – POST
@app.post("/tags", status_code=201)
def create_tag(tag: dict, db: Session = Depends(get_db)):
    new_tag = Tag(
        userId=tag["userId"],
        movieId=tag["movieId"],
        tag=tag["tag"],
        timestamp=tag["timestamp"],
    )
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return tag_to_dict(new_tag)


# READ – pojedynczy
@app.get("/tags/{tag_id}")
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag_to_dict(tag)


# UPDATE – PUT
@app.put("/tags/{tag_id}")
def update_tag(tag_id: int, tag_data: dict, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag.userId = tag_data.get("userId", tag.userId)
    tag.movieId = tag_data.get("movieId", tag.movieId)
    tag.tag = tag_data.get("tag", tag.tag)
    tag.timestamp = tag_data.get("timestamp", tag.timestamp)

    db.commit()
    db.refresh(tag)
    return tag_to_dict(tag)


# DELETE
@app.delete("/tags/{tag_id}", status_code=204)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.delete(tag)
    db.commit()
    return
