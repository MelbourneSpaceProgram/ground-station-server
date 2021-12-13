from flask_restful import Api, Resource, reqparse

from backend.database import get_db

api = Api()


class Satellites(Resource):
    def get(self):
        db = get_db()
        sats = [db[id] for id in list(db.keys())]
        return sats, 200

    def post(self):
        # REVIEW: getting deprecated
        parser = reqparse.RequestParser()

        parser.add_argument("id", required=True)
        parser.add_argument("name", required=True)
        parser.add_argument("pipeline", required=True)

        args = parser.parse_args()

        db = get_db()
        db[args['id']] = args

        return args, 201


class Satellite(Resource):
    def get(self, sat_id):
        db = get_db()

        if sat_id not in db.keys():
            return {"error": "Satellite not found"}, 404

        return db[sat_id], 200

    def delete(self, sat_id):
        db = get_db()

        if sat_id not in db.keys():
            return {"error": "Satellite not found"}, 404

        del db[sat_id]
        return {}, 204


api.add_resource(Satellites, "/satellites")
api.add_resource(Satellite, "/satellites/<sat_id>")
