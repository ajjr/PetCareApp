from datetime import datetime
from typing import List
import sqlalchemy as sa
import sqlalchemy.orm as orm

from petcare.models.event_repeat import EventRepeat
from petcare.models.modelbase import Base, ModelBase
from petcare.models.operation_instance import OperationInstance
from petcare.models.operation import Operation


class Event(Base, ModelBase):
    __tablename__ = "event"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    date: datetime = sa.Column(sa.DateTime, nullable=False)
    add_timestamp: datetime = sa.Column(sa.DateTime, default=datetime.utcnow(), nullable=False)
    done_timestamp: datetime = sa.Column(sa.DateTime)
    done_date: str = sa.Column(sa.DATE)
    description: str = sa.Column(sa.String)

    # Foreign key relationships
    pet_id: int = sa.Column(sa.Integer, sa.ForeignKey("pet.id"))
    pet = orm.relation("Pet")
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    user = orm.relation("User")

    # List of operations related to this event
    operations: OperationInstance = orm.relation("OperationInstance")

    event_repeat: List[EventRepeat] = orm.relation("EventRepeat")
