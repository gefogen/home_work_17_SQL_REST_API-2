from flask_restx import Api, Namespace, Resource, fields
from flask import request
from models import Director, DirectorSchema
from setup_db import db

api = Namespace('genres')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

@api.route("/")
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get("director_id", type=int)
        genre_id = request.args.get("genre_id", type=int)

        if director_id:
            movies = Director.query.filter(Director.director_id == director_id)
            return directors_schema.dump(movies), 200

        if genre_id:
            genres = Director.query.filter(Director.genre_id == genre_id)
            return directors_schema.dump(genres), 200

        movies = Director.query.all()
        return directors_schema.dump(movies), 200

    def post(self):
        movie = request.json
        new_movie = Director(**movie)

        db.session.add(new_movie)
        db.session.commit()
        return "", 201


@api.route("/<int:pk>")
class MovieView(Resource):
    def get(self, pk):
        movie = Director.query.get(pk)
        return director_schema.dump(movie), 200

    def delete(self, pk):
        movie = Director.query.get(pk)
        db.session.delete(movie)
        db.session.commit()
        return "", 200

    def put(self, pk):
        movie = Director.query.get(pk)
        update_movie = request.json

        movie.name = update_movie.get('name')

        db.session.add(movie)
        db.session.commit()