from flask_restful import Resource, abort


class Ping(Resource):
    def get(self):
        return 200


class Ready(Resource):
    def get(self):
        return 200


class Report(Resource):
    def get(self, content_type):
        abort(501)
