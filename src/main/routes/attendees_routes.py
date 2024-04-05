from flask import Blueprint, jsonify, request

from src.data.attendees_handler import AttendeesHandler
from src.data.event_handler import EventHandler
from src.errors.error_handler import handle_error
from src.http_types import http_request
from src.http_types.http_request import HttpRequest

attendees_route_bp = Blueprint("attendees_route", __name__)


@attendees_route_bp.route("/events/<event_id>/register", methods=["POST"])
def create_attendees(event_id):
    try:
        http_request = HttpRequest(param={"event_id": event_id}, body=request.json)

        attendees_handler = AttendeesHandler()
        http_response = attendees_handler.registry(http_request=http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exc:
        http_response = handle_error(exc)
        return jsonify(http_response.body), http_response.status_code


@attendees_route_bp.route("/attendees/<attendee_id>/badge", methods=["GET"])
def find_attendees(attendee_id):
    try:
        attendees_handler = AttendeesHandler()
        http_request = HttpRequest(param={"attendee_id": attendee_id})

        http_response = attendees_handler.find_attendee(http_request=http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exc:
        http_response = handle_error(exc)
        return jsonify(http_response.body), http_response.status_code


@attendees_route_bp.route("/events/<event_id>/attendees", methods=["GET"])
def get_attendees(event_id):
    try:
        http_request = HttpRequest(param={"event_id": event_id})

        attendees_handler = AttendeesHandler()
        http_response = attendees_handler.find_attendees_at_event(
            http_request=http_request
        )
        return jsonify(http_response.body), http_response.status_code
    except Exception as exc:
        http_response = handle_error(exc)
        return jsonify(http_response.body), http_response.status_code
