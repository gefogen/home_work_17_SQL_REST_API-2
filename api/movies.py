from flask_restx import Api, Namespace, Resource, fields
from flask import request
from create_data import Movie, MovieSchema
from setup_db import db

api = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@api.route("/")
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get("director_id", type=int)
        genre_id = request.args.get("genre_id", type=int)

        if director_id:
            movies = Movie.query.filter(Movie.director_id == director_id)
            return movies_schema.dump(movies), 200

        if genre_id:
            genres = Movie.query.filter(Movie.genre_id == genre_id)
            return movies_schema.dump(genres), 200

        movies = Movie.query.all()
        return movies_schema.dump(movies), 200

    def post(self):
        movie = request.json
        new_movie = Movie(**movie)

        db.session.add(new_movie)
        db.session.commit()
        return "", 201


@api.route("/<int:pk>")
class MovieView(Resource):
    def get(self, pk):
        movie = Movie.query.get(pk)
        return movie_schema.dump(movie), 200

    def delete(self, pk):
        movie = Movie.query.get(pk)
        db.session.delete(movie)
        db.session.commit()
        return "", 200

    def put(self, pk):
        movie = Movie.query.get(pk)
        update_movie = request.json

        movie.title = update_movie.get('title')
        movie.description = update_movie.get('description')
        movie.trailer = update_movie.get('trailer')
        movie.year = update_movie.get('year')
        movie.rating = update_movie.get('rating')
        movie.genre_id = update_movie.get('genre_id')
        movie.director_id = update_movie.get('director_id')

        db.session.add(movie)
        db.session.commit()
