from flask_restful import Resource, abort

from src.aggregation import get_report
from src.responses import TimeSeriesResponse
from src.timeseries import get_time_series
from src.utils import ServiceKey, NotAServiceKeyException, FetchFromServiceException


class Ping(Resource):
    def get(self):
        return 200


class Ready(Resource):
    def get(self):
        return 200


class Report(Resource):
    def get(self, content_type):
        try:
            result = get_report(ServiceKey.get_key(content_type)).json()
            return result
        except NotAServiceKeyException:
            abort(400)
        except FetchFromServiceException as err:
            abort(500, reason=err.reason)
        except KeyError:
            abort(501, reason=f"reports for {content_type} is not avaiable")


class TimeSeries(Resource):
    def get(self, content_type):
        try:
            result: TimeSeriesResponse = get_time_series(ServiceKey.get_key(content_type))
            return result.json()
        except NotAServiceKeyException:
            abort(400)
        except FetchFromServiceException as err:
            abort(500, reason=err.reason)
        except KeyError:
            abort(501)
