import calendar
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional, List

import sqlalchemy.orm as orm
from sqlalchemy import and_

import petcare.models.db_session as db
from petcare.models.event import Event
from petcare.models.event_repeat import EventRepeat
from petcare.models.event_series import EventSeries
from petcare.models.operation import Operation
from petcare.models.operation_instance import OperationInstance


def get_event(event_id: int) -> Optional[Event]:
    return db.get_db_obj(event_id, Event)


def get_current_events(user_id: int, pet_id=None, limit=10) -> List[Event]:
    session = db.create_session()
    try:
        events = session.query(Event) \
            .options(orm.joinedload(Event.pet)) \
            .options(orm.joinedload(Event.operations)) \
            .filter(Event.user_id == user_id) \
            .filter(Event.date > datetime.today() - timedelta(1)) \
            .order_by(Event.pet_id).limit(limit).all() \
            if not pet_id else \
            session.query(Event) \
                .options(orm.joinedload(Event.pet)) \
                .options(orm.joinedload(Event.operations)) \
                .filter(Event.user_id == user_id) \
                .filter(Event.pet_id == pet_id) \
                .filter(Event.date > datetime.today() - timedelta(1)) \
                .order_by(Event.date).limit(limit).all()
    finally:
        session.close()
    return events


def get_events_between(start_date, end_date, user_id) -> defaultdict:
    session = db.create_session()
    try:
        events = session.query(Event) \
            .options(orm.joinedload(Event.pet)) \
            .options(orm.joinedload(Event.operations)) \
            .filter(and_(Event.date > start_date - timedelta(1),
                         Event.date < end_date + timedelta(1))) \
            .filter(Event.user_id == user_id) \
            .order_by(Event.date).all()
        # events = session.query(Event, OperationInstance, Operation).select_from(Event) \
        #     .join(OperationInstance) \
        #     .join(Operation) \
        #     .filter(and_(Event.date > start_date, Event.date < end_date)) \
        #     .filter(Event.user_id == user_id) \
        #     .order_by(Event.date).all()

        from pprint import pprint
        pprint(events)
        event_dict = defaultdict(list)
        for event in events:
            event_dict[(event.date.month, event.date.day)].append({
                "title": event.description,
                "pet_name": event.pet.name,
                "pet_id": event.pet_id,
                "event_done": event.done_timestamp,
                "event_id": event.id,
                "event_time": event.date.time()
            })
            if event.operations:
                for oper in event.operations:
                    event_dict[(event.date.month, event.date.day)][-1]["oi_id"] = oper.id
                    event_dict[(event.date.month, event.date.day)][-1]["operation_name"] = oper.operation_id.lower()
                    event_dict[(event.date.month, event.date.day)][-1]["operator"] = oper.operator




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
                 operation_id=None, operator=None):
    event = Event()
    event.date = event_date
    event.description = event_desc
    event.user_id = user_id
    event.pet_id = pet_id

    op = None
    if operation_id:
        op = OperationInstance()
        op.operator = operator
        op.operation_id = operation_id
        op.event = event

    session = db.create_session()
    try:
        session.add(event)
        if op:
            session.add(op)
        session.commit()
    finally:
        session.close()


def insert_repeating_event(ldate: datetime, rdate: datetime, event_desc: str, user_id, pet_id: int,
                           operation_id, operator=None, repeat_name=None):
    delta = abs((rdate - ldate).days)
    session = db.create_session()
    try:
        series = EventSeries()
        series.name = repeat_name if repeat_name else "Toistuva tapahtuma alk. " + str(ldate)
        session.add(series)

        for i in range(delta):
            e = Event()
            e.date = ldate + timedelta(i)
            e.description = event_desc
            e.user_id = user_id
            e.pet_id = pet_id

            op = OperationInstance()
            op.operator = operator
            op.operation_id = operation_id
            op.event = e

            repeat = EventRepeat()
            repeat.event_series = series
            repeat.event = e

            session.add(e)
            session.add(op)
            session.add(repeat)
            #print(e.date)
            #print(e)
            #print(op)
            #print(repeat)

        session.commit()
    finally:
        session.close()


def update_event_done(event_id: int):
    event = db.get_db_obj(event_id, Event)
    event.done_timestamp = datetime.today()
    session = db.create_session()
    try:
        session.merge(event)
        session.commit()
    finally:
        session.close()




