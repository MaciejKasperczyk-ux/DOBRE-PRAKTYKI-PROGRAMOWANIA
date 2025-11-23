import csv

from db import SessionLocal, engine
from models import Movie, Link, Rating, Tag
from db import Base

# (opcjonalne) utworzenie tabel - jeśli nie robisz tego w main.py
Base.metadata.create_all(bind=engine)


def load_movies():
    db = SessionLocal()
    try:
        with open("database/movies.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                movie = Movie(
                    movieId=int(row["movieId"]),
                    title=row["title"],
                    genres=row["genres"]
                )
                db.add(movie)
        db.commit()
    finally:
        db.close()


def load_links():
    db = SessionLocal()
    try:
        with open("database/links.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                link = Link(
                    movieId=int(row["movieId"]),
                    imdbId=row["imdbId"],
                    tmdbId=row["tmdbId"]
                )
                db.add(link)
        db.commit()
    finally:
        db.close()


def load_ratings():
    db = SessionLocal()
    try:
        with open("database/ratings.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                rating = Rating(
                    userId=int(row["userId"]),
                    movieId=int(row["movieId"]),
                    rating=float(row["rating"]),
                    timestamp=int(row["timestamp"])
                )
                db.add(rating)
        db.commit()
    finally:
        db.close()


def load_tags():
    db = SessionLocal()
    try:
        with open("database/tags.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                tag = Tag(
                    userId=int(row["userId"]),
                    movieId=int(row["movieId"]),
                    tag=row["tag"],
                    timestamp=int(row["timestamp"])
                )
                db.add(tag)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    load_movies()
    load_links()
    load_ratings()
    load_tags()
    print("Dane załadowane do SQLite.")
