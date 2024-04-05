from flask import Blueprint, jsonify, request

from src.data.check_in_handler import CheckInHandler
from src.errors.error_handler import handle_error
from src.http_types.http_request import HttpRequest
from src.http_types.http_response import HttpResponse

check_in_route_bp = Blueprint("check_in", __name__)


@check_in_route_bp.route("/attendees/<attendee_id>/check-in", methods=["POST"])
def create_attendees(attendee_id):
    try:
        http_request = HttpRequest(param={"attendee_id": attendee_id})

        check_in_handler = CheckInHandler()
        http_response: HttpResponse = check_in_handler.registry(
            http_request=http_request
        )
        return jsonify(http_response.body), http_response.status_code

    except Exception as exc:
        http_response = handle_error(exc)
        return jsonify(http_response.body), http_response.status_code
