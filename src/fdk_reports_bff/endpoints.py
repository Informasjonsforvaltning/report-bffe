from flask import request
from flask_restful import Resource, abort

from fdk_reports_bff.aggregation import get_report
from fdk_reports_bff.elasticsearch import get_all_update_entries
from fdk_reports_bff.elasticsearch.scheduler import Update
from fdk_reports_bff.responses import TimeSeriesResponse
from fdk_reports_bff.timeseries import get_time_series
from fdk_reports_bff.utils import (
    FetchFromServiceException,
    NotAServiceKeyException,
    ServiceKey,
)


class Ping(Resource):
    def get(self):
        return 200


class Updates(Resource):
    def get(self):
        return get_all_update_entries()

    def post(self):
        try:
            should_ignore = request.args["ignore_previous"]
        except KeyError:
            should_ignore = False
        Update.start_update(ignore_previous_updates=should_ignore)
        return 200


class Ready(Resource):
    def get(self):
        return 200


class Report(Resource):
    def get(self, content_type):
        try:
            result = get_report(
                content_type=ServiceKey.get_key(content_type), args=request.args
            ).json()
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
            result: TimeSeriesResponse = get_time_series(
                ServiceKey.get_key(content_type), args=request.args
            )
            return result.json()
        except NotAServiceKeyException:
            abort(400)
        except FetchFromServiceException as err:
            abort(500, reason=err.reason)
        except KeyError:
            abort(501)
