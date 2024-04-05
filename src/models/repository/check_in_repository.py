from src.errors.error_types.http_conflict import HttpConflictError
from src.models.entities.check_in import CheckIn
from src.models.settings.connections import db_connection_handler
from sqlalchemy.exc import IntegrityError, NoResultFound

db_connection_handler.connect_to_db()


class CheckInRepository:
    def insert_check_in(self, attendee_id: str):
        with db_connection_handler as db:
            try:
                check_in = CheckIn(attendeeId=attendee_id)
                db.session.add(check_in)
                db.session.commit()

                return attendee_id

            except IntegrityError:
                raise HttpConflictError("Check In já feito")

            except Exception as exc:
                db.session.rollback()
                raise exc
