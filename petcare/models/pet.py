from typing import List
import sqlalchemy as sa
import sqlalchemy.orm as orm
from petcare.models.modelbase import ModelBase
from petcare.models.modelbase import Base
from petcare.models.event import Event
import petcare.models.db_session as db


class Pet(Base, ModelBase):
    __tablename__ = "pet"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False, index=True)
    birthday = sa.Column(sa.DATE)
    age = sa.Column(sa.INT)
    breeder = sa.Column(sa.String)
    summary = sa.Column(sa.String)
    image_url = sa.Column(sa.String)

    breed_id = sa.Column(sa.Integer, sa.ForeignKey("breed.id"))
    breed = orm.relation("Breed", lazy="joined", join_depth=3)

    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    owner = orm.relation("User", lazy="joined", join_depth=1)

    events: List[Event] = orm.relation("Event", lazy="joined", join_depth=2, order_by=Event.date.desc(),
                                       back_populates="pet")
