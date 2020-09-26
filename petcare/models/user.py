import datetime
from typing import List
import sqlalchemy as sa
import sqlalchemy.orm as orm
from petcare.models.modelbase import Base
from petcare.models.modelbase import ModelBase
from petcare.models.pet import Pet


class User(Base, ModelBase):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.String, unique=True, nullable=False, index=True)
    name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False, index=True)
    created_date = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.now, index=True)
    profile_image_url = sa.Column(sa.String)
    last_login = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    #timezone = sa.Column(sa.String)

    pets: List[Pet] = orm.relation("Pet", order_by=Pet.name.desc(), back_populates="owner")
