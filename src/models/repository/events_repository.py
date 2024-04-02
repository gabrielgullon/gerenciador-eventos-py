from typing import Dict
from src.models.entities.events import Events
from src.models.settings.connections import db_connection_handler


class EventsRepository:
    def insert_event(self, eventsInfo: Dict) -> Dict:
        with db_connection_handler as db:
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

    def get_event_by_id(self, event_id: str) -> Events:
        with db_connection_handler as db:
            event = db.session.query(Events).filter(Events.id == event_id).one()

            return event
