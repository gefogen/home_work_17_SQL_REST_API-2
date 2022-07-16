from flask_restx import Api, Namespace, Resource, fields
from flask import request
from create_data import Genre, GenreSchema
from setup_db import db

api = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

@api.route("/")
class GenresView(Resource):
    def get(self):
        movies = Genre.query.all()
        return genres_schema.dump(movies), 200

    def post(self):
        movie = request.json
        new_movie = Genre(**movie)

        db.session.add(new_movie)
        db.session.commit()
        return "", 201


@api.route("/<int:pk>")
class GenreView(Resource):
    def get(self, pk):
        movie = Genre.query.get(pk)
        return genre_schema.dump(movie), 200

    def delete(self, pk):
        movie = Genre.query.get(pk)
        db.session.delete(movie)
        db.session.commit()
        return "", 200

    def put(self, pk):
        movie = Genre.query.get(pk)
        update_movie = request.json

        movie.name = update_movie.get('name')

        db.session.add(movie)
        db.session.commit()
