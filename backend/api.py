from flask_restful import Api, Resource, reqparse

from backend.database import get_sats_db, get_passes_db
from backend.tracker import compute_next_pass, compute_latlon

api = Api()


class Satellites(Resource):
    def get(self):
        sats_db = get_sats_db()
        sats = [sats_db[id] for id in list(sats_db.keys())]
        return sats, 200

    def post(self):
        # REVIEW: getting deprecated
        parser = reqparse.RequestParser()

        parser.add_argument("id", required=True)
        parser.add_argument("name", required=True)
        parser.add_argument("pipeline", required=True)

        args = parser.parse_args()

        sats_db = get_sats_db()
        sats_db[args['id']] = args

        next_pass = compute_next_pass(args['id'])

        passes_db = get_passes_db()
        passes_db[args['id']] = next_pass

        return sats_db[args['id']], 201


class Satellite(Resource):
    def get(self, sat_id):
        db = get_sats_db()

        if sat_id not in db.keys():
            return {"error": "Satellite not found"}, 404

        return db[sat_id], 200

    def delete(self, sat_id):
        sats_db = get_sats_db()
        passes_db = get_passes_db()

        if sat_id not in sats_db.keys():
            return {"error": "Satellite not found"}, 404

        del sats_db[sat_id]

        if sat_id in passes_db.keys():
            del passes_db[sat_id]

        return {}, 204


class Passes(Resource):
    def get(self, sat_id):
        db = get_passes_db()

        if sat_id not in db.keys():
            return {"error": "Satellite not found"}, 404

        return db[sat_id], 200


class LatLon(Resource):
    def get(self, sat_id):
        db = get_sats_db()

        if sat_id not in db.keys():
            return {"error": "Satellite not found"}, 404

        data = compute_latlon(sat_id)
        return data, 200


api.add_resource(Satellites, "/satellites")
api.add_resource(Satellite, "/satellites/<sat_id>")
api.add_resource(Passes, "/satellites/<sat_id>/passes")
api.add_resource(LatLon, "/satellites/<sat_id>/latlon")
