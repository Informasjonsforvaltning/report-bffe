from flask_restful import Resource


class Ping(Resource):
    def get(self):
        return 200


class Ready(Resource):
    def get(self):
        return 200
