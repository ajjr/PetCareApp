from collections import defaultdict
from datetime import datetime
from typing import Optional, List

import sqlalchemy.orm as orm
from sqlalchemy import and_

import petcare.models.db_session as db
from petcare.models.event import Event
from petcare.models.operation import Operation
from petcare.models.operation_instance import OperationInstance


def get_event(event_id: int) -> Optional[Event]:
    return db.get_db_obj(event_id, Event)


def get_current_events(limit=10) -> List[Event]:
    session = db.create_session()
    try:
        events = session.query(Event) \
            .options(orm.joinedload(Event.pet)) \
            .options(orm.joinedload(Event.operation)) \
            .order_by(Event.pet_id).limit(limit).all()
    finally:
        session.close()
    return events


def get_events_between(start_date, end_date, user_id):
    session = db.create_session()
    try:
        events = session.query(Event) \
            .options(orm.joinedload(Event.pet)) \
            .options(orm.joinedload(Event.operations)) \
            .filter(and_(Event.date > start_date, Event.date < end_date)) \
            .filter(Event.user_id == user_id) \
            .order_by(Event.date).all()
        # events = session.query(Event, OperationInstance, Operation).select_from(Event) \
        #     .join(OperationInstance) \
        #     .join(Operation) \
        #     .filter(and_(Event.date > start_date, Event.date < end_date)) \
        #     .filter(Event.user_id == user_id) \
        #     .order_by(Event.date).all()

        print(events)
        event_dict = defaultdict(list)
        for event in events:
            event_dict[(event.date.month, event.date.day)].append({
                "title": event.description,
                "pet_name": event.pet.name,
                "pet_id": event.pet_id,
                "event_id": event.id
            })
            if event.operations:
                for oper in event.operations:
                    event_dict[(event.date.month, event.date.day)][-1]["oi_id"] = oper.id
                    event_dict[(event.date.month, event.date.day)][-1]["operation_name"] = oper.operation_id




    finally:
        session.close()

    return event_dict


def get_operations() -> List[Operation]:
    session = db.create_session()
    return session.query(Operation).all()


def insert_simple_event(event_date: datetime, event_desc: str, user_id, pet_id=None):
    event = Event()
    event.date = event_date
    event.description = event_desc
    event.user_id = user_id
    event.pet_id = pet_id

    session = db.create_session()
    try:
        session.add(event)
        session.commit()
    finally:
        session.close()


def insert_event(event_date: datetime, event_desc: str, user_id, pet_id: int,
                 operation_id: int, operator: str):
    event = Event()
    event.date = event_date
    event.description = event_desc
    event.user_id = user_id
    event.pet_id = pet_id

    op = OperationInstance()
    op.operator = operator
    op.operation_id = operation_id
    op.event = event

    session = db.create_session()
    try:
        session.add(event)
        session.add(op)
        session.commit()
    finally:
        session.close()



