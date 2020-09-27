from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm

from petcare.models.event_repeat import EventRepeat
from petcare.models.modelbase import Base, ModelBase


class EventSeries(Base, ModelBase):
    __tablename__ = "event_series"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name: str = sa.Column(sa.String)

    event_repeat: List[EventRepeat] = orm.relation("EventRepeat", back_populates="event_series")
