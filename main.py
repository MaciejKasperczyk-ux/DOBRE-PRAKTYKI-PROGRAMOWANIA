import csv
from fastapi import FastAPI

from models import Movie, Link, Rating, Tag
app = FastAPI()


@app.get("/movies")
def read_movies():
    movies = []
    with open(r"C:\Users\Makas\Downloads\database\movies.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            movie = Movie(row["movieId"], row["title"], row["genres"])
            movies.append(movie.__dict__)
    return movies


@app.get("/links")
def read_links():
    links = []
    with open(r"C:\Users\Makas\Downloads\database\links.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            link = Link(row["movieId"], row["imdbId"], row["tmdbId"])
            links.append(link.__dict__)
    return links


@app.get("/ratings")
def read_ratings():
    ratings = []
    with open(r"C:\Users\Makas\Downloads\database\ratings.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rating = Rating(row["userId"], row["movieId"], row["rating"], row["timestamp"])
            ratings.append(rating.__dict__)
    return ratings


@app.get("/tags")
def read_tags():
    tags = []
    with open(r"C:\Users\Makas\Downloads\database\tags.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tag = Tag(row["userId"], row["movieId"], row["tag"], row["timestamp"])
            tags.append(tag.__dict__)
    return tags
