import os
from typing import Any

from flask import request
from flask_restful import abort, Resource

from fdk_reports_bff.aggregation.aggregation import get_report
from fdk_reports_bff.elasticsearch import get_all_update_entries
from fdk_reports_bff.elasticsearch.scheduler import Update
from fdk_reports_bff.service.utils import (
    FetchFromServiceException,
    NotAServiceKeyException,
    ServiceKey,
)

env = {
    ServiceKey.API_KEY: os.getenv("API_KEY"),
}


class Ping(Resource):
    def get(self: Any) -> Any:
        return 200


class Updates(Resource):
    def get(self: Any) -> Any:
        api_key_expected = env.get(ServiceKey.API_KEY)
        api_key = request.headers.get("X-API-KEY")
        if not (api_key and api_key_expected and api_key_expected == api_key):
            abort(http_status_code=403, description="Forbidden")

        return get_all_update_entries()

    def post(self: Any) -> Any:
        api_key_expected = env.get(ServiceKey.API_KEY)
        api_key = request.headers.get("X-API-KEY")
        if not (api_key and api_key_expected and api_key_expected == api_key):
            abort(http_status_code=403, description="Forbidden")

        try:
            should_ignore = request.args["ignore_previous"]
        except KeyError:
            should_ignore = False
        Update.start_update(ignore_previous_updates=should_ignore)
        return 200


class Ready(Resource):
    def get(self: Any) -> Any:
        return 200


class Report(Resource):
    def get(self: Any, content_type: str) -> Any:
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
