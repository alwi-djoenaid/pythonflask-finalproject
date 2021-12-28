"""
This is the movie module and supports all the REST actions for the
Movies data
"""

from flask import make_response, abort
from config import db
from models import Movie, Director, MovieSchema
from marshmallow import EXCLUDE


def read_all():
    """
    This function responds to a request for /api/movie
    with the complete list of movies
    :return:   json list of all movies
    """
    
    movies = Movie.query.order_by(Movie.id).limit(20)

    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movies)
    return data

def read_top_five_popularity():
    """
    This function responds to a request for /api/movie/top5movies
    with the complete list of movies
    :return:   json list of 5 most popular movies
    """

    movies = Movie.query.order_by(db.desc(Movie.popularity)).limit(5)

    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movies)
    return data

def read_five_most_revenue():
    """
    This function responds to a request for /api/movie/top5revenue
    with the complete list of movies
    :return:   json list of 5 most revenue movies
    """

    movies = Movie.query.order_by(db.desc(Movie.revenue)).limit(5)

    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movies)
    return data

def read_one_by_id(movie_id, director_id):
    """
    This function responds to a request for /api/directors/{id}
    with single movie record
    :param director_id:      ID of the director the movie is related to
    :param movie_id:         ID of the movie
    :return:  JSON list of a movie
    """

    movie = (
        Movie.query.join(Director, Director.id == Movie.director_id)
        .filter(Director.id == director_id)
        .filter(Movie.id == movie_id)
        .one_or_none()
    )

    if movie is not None:
        movieSchema = MovieSchema()
        data = movieSchema.dump(movie)
        return data
    
    else:
        abort(404, f"Movie not found for ID: {movie_id}")

def read_movie_by_name(movie_name):
    """
    This function responds to a request for /api/movies/movie_name
    with a record of movies filtered by their name
    :param movie_name:  movie name to be filtered
    :return: json of a movie records
    """

    search = "%{}%".format(movie_name)

    movies = Movie.query.filter(Movie.original_title.like(search)).all()

    if movies is not None:
        movieSchema = MovieSchema(many=True)
        data = movieSchema.dump(movies)
        return data
    
    else:
        abort(404, f"Movie not found for name: {movie_name}")

def create(movie, director_id):
    """
    This function creates a new movie related to the passed in director ID.
    :param director_id:      Id of the director the movie is related to
    :param movie:            The JSON containing the movie data
    :return:                201 on success
    """

    director = Director.query.filter(Director.id == director_id).one_or_none()

    if director is None:
        abort(404, f"Director not found for ID: {director_id}")

    movieSchema = MovieSchema()
    newMovie = movieSchema.load(movie, session=db.session)

    director.movies.append(newMovie)
    db.session.commit()

    data = movieSchema.dump(newMovie)

    return data, 201

def update(movie, director_id, movie_id):
    """
    This function updates an existing movie related to the passed in
    director ID.
    :param director_id:       Id of the director the movie is related to
    :param movie_id:         Id of the movie to update
    :param movie:            The JSON containing the movie data
    :return:                200 on success
    """

    print('######################')
    print(director_id)

    targetMovie = (
        Movie.query.filter(Director.id == director_id)
        .filter(Movie.id == movie_id)
        .one_or_none()
    )

    if targetMovie is not None:
        movieSchema = MovieSchema()
        updatedMovie = movieSchema.load(movie, session=db.session, unknown=EXCLUDE)

        updatedMovie.director_id = targetMovie.director_id
        updatedMovie.id = targetMovie.id

        db.session.merge(updatedMovie)
        db.session.commit()

        data = movieSchema.dump(targetMovie)

        return data, 200

    else:
        abort(404, f"Movie not found for ID: {movie_id}")

def delete(movie_id, director_id):
    """
    This function deletes a movie from the movie structure
    :param director_id:   Id of the director the movie is related to
    :param movie_id:     Id of the movie to delete
    :return:            200 on successful delete, 404 if not found
    """

    movie = (
        Movie.query.filter(Director.id == director_id)
        .filter(Movie.id == movie_id)
        .one_or_none()
    )

    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response("Movie {movie_id} deleted successfully".format(movie_id = movie_id), 200)

    else:
        abort(404, f"Movie not found for ID: {movie_id}")