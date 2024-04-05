from typing import Dict
from src.errors.error_types.http_conflict import HttpConflictError
from src.models.entities.attendees import Attendees
from src.models.entities.events import Events
from src.models.settings.connections import db_connection_handler
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


class EventsRepository:
    def insert_event(self, eventsInfo: Dict) -> Dict:
        with db_connection_handler as db:
            try:
                event = Events(
                    id=eventsInfo.get("uuid"),
                    title=eventsInfo.get("title"),
                    details=eventsInfo.get("details"),
                    slug=eventsInfo.get("slug"),
                    maximum_attendees=eventsInfo.get("maximum_attendees"),
                )

                db.session.add(event)
                db.session.commit()

                return eventsInfo

            except IntegrityError:
                raise HttpConflictError("Evento já cadastrado")

            except Exception as exc:
                db.session.rollback()
                raise exc

    def get_event_by_id(self, event_id: str) -> Events:
        with db_connection_handler as db:
            try:
                event = db.session.query(Events).filter(Events.id == event_id).one()

                return event

            except NoResultFound:
                return None

    def count_event_attendees(self, event_id: str) -> Dict:
        with db_connection_handler as db:
            event_count = (
                db.session.query(Events)
                .join(Attendees, Events.id == Attendees.event_id)
                .filter(Events.id == event_id)
                .with_entities(Events.maximum_attendees, Attendees.id)
                .all()
            )

            if not len(event_count):
                return {"maximumAttendees": 0, "attendeesCount": 0}

            return {
                "maximumAttendees": event_count[0].maximum_attendees,
                "attendeesCount": len(event_count),
            }
