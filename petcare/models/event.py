import sqlalchemy as sa
import sqlalchemy.orm as orm
from petcare.models.modelbase import Base


class Event(Base):
    __tablename__ = "event"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    date = sa.Column(sa.DATE, nullable=False)
    add_timestamp = sa.Column(sa.DateTime, nullable=False)
    done_timestamp = sa.Column(sa.DateTime, nullable=False)
    done_date = sa.Column(sa.DATE)
    description = sa.Column(sa.String, nullable=False)

    pet_id = sa.Column(sa.Integer, sa.ForeignKey("pet.id"))
    pet = orm.relation("Pet")
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    user = orm.relation("User")
