from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)  # wewnętrzne id
    movieId = Column(Integer, index=True)               # id z CSV
    title = Column(String, index=True)
    genres = Column(String)


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    movieId = Column(Integer, index=True)
    imdbId = Column(String)
    tmdbId = Column(String)


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, index=True)
    movieId = Column(Integer, index=True)
    rating = Column(Float)
    timestamp = Column(Integer)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, index=True)
    movieId = Column(Integer, index=True)
    tag = Column(String)
    timestamp = Column(Integer)
