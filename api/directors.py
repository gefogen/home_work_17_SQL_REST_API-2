from flask_restx import Api, Namespace, Resource, fields
from flask import request
from create_data import Director, DirectorSchema
from setup_db import db

api = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

@api.route("/")
class DirectorsView(Resource):
    def get(self):
        movies = Director.query.all()
        return directors_schema.dump(movies), 200

    def post(self):
        movie = request.json
        new_movie = Director(**movie)

        db.session.add(new_movie)
        db.session.commit()
        return "", 201


@api.route("/<int:pk>")
class DirectorView(Resource):
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
