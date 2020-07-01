from flask_restful import Resource, abort

from src.aggregation import get_report
from src.utils import ServiceKey, NotAServiceKeyException


class Ping(Resource):
    def get(self):
        return 200


class Ready(Resource):
    def get(self):
        return 200


class Report(Resource):
    def get(self, content_type):
        try:
            result = get_report()
            abort(501)
        except NotAServiceKeyException:
            abort(400)
