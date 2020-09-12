from typing import List
import json
import sqlalchemy as sa
import sqlalchemy.orm as orm
from petcare.models.modelbase import ModelBase
from petcare.models.modelbase import Base
from petcare.models.breed import Breed


class Species(Base, ModelBase):
    __tablename__ = "species"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False, index=True)

    breeds: List[Breed] = orm.relation("Breed", order_by=Breed.name.desc(), back_populates="species")
