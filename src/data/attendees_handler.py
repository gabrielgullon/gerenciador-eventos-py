from uuid import uuid4

from src.errors.error_types.http_conflict import HttpConflictError
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.http_types.http_request import HttpRequest
from src.http_types.http_response import HttpResponse
from src.models.repository.events_repository import EventsRepository
from src.models.repository.attendees_repository import AttendeesRepository


class AttendeesHandler:
    def __init__(self) -> None:
        self.__attendees_repo = AttendeesRepository()
        self.__events_repository = EventsRepository()

    def registry(self, http_request: HttpRequest) -> HttpResponse:
        body = http_request.body
        event_id = http_request.param["event_id"]

        events_attendees_count = self.__events_repository.count_event_attendees(
            event_id
        )

        if (
            events_attendees_count["attendeesCount"]
            and events_attendees_count["attendeesCount"]
            >= events_attendees_count["maximumAttendees"]
        ):
            raise HttpConflictError("Evento Lotado")

        body["uuid"] = str(uuid4())
        body["event_id"] = event_id
        self.__attendees_repo.insert_attendee(body)

        return HttpResponse(body=None, status_code=201)

    def find_attendee(self, http_request: HttpRequest) -> HttpResponse:
        attendee_id = http_request.param["attendee_id"]
        badge = self.__attendees_repo.get_attendee_by_id(attendee_id=attendee_id)

        if not badge:
            raise HttpNotFoundError("Participante não cadastrado")

        return HttpResponse(
            body={"name": badge.name, "email": badge.email}, status_code=200
        )

    def find_attendees_at_event(self, http_request: HttpRequest) -> HttpResponse:
        event_id = http_request.param["event_id"]
        attendees = self.__attendees_repo.get_attendees_by_event_id(event_id=event_id)
        if not attendees:
            raise HttpNotFoundError("Evento vazio")

        formatted_attendees = []

        for a in attendees:
            formatted_attendees.append(
                {
                    "id": a.id,
                    "name": a.name,
                    "email": a.email,
                    "check_in": a.check_in_at,
                }
            )

        return HttpResponse(body={"attendees": formatted_attendees}, status_code=200)
