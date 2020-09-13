from typing import Optional, List
from petcare.models.event import Event
from petcare.models.operation import Operation
from petcare.models.operation_instance import OperationInstance
import petcare.models.db_session as db
import sqlalchemy.orm as orm


def get_event(event_id: int) -> Optional[Event]:
    return db.get_db_obj(event_id, Event)


def get_current_events(limit=10) -> List[Event]:
    session = db.create_session()
    try:
        events = session.query(Event) \
            .options(orm.joinedload(Event.pet)) \
            .order_by(Event.pet_id).limit(limit).all()
    finally:
        session.close()
    return events
