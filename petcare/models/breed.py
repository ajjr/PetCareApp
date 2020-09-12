import sqlalchemy as sa
import sqlalchemy.orm as orm
from petcare.models.modelbase import ModelBase
from petcare.models.modelbase import Base


class Breed(Base, ModelBase):
    __tablename__ = "breed"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False, index=True)

    species_id = sa.Column(sa.Integer, sa.ForeignKey("species.id"))
    species = orm.relation("Species", lazy="joined", join_depth=2)
