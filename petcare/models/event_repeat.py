import sqlalchemy as sa
import sqlalchemy.orm as orm
from petcare.models.modelbase import Base, ModelBase


class EventRepeat(Base, ModelBase):
    __tablename__ = "event_repeat"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    event_series_id: int = sa.Column(sa.Integer, sa.ForeignKey("event_series.id"))
    event_id: int = sa.Column(sa.Integer, sa.ForeignKey("event.id"))

    event = orm.relation("Event", back_populates="event_repeat")
    event_series = orm.relation("EventSeries", back_populates="event_repeat")
