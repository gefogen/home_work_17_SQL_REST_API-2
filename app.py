# app.py
import json

from flask import Flask, request
from flask_restx import Api, Resource, Namespace
from setup_db import db
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False}

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

api = Api(app)
movies_api = api.namespace('movies')

db.init_app(app)


@movies_api.route("/")
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


@movies_api.route("/<int:pk>")
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


if __name__ == '__main__':
    app.run(debug=True)