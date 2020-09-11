import sqlalchemy as sa
from petcare.models.modelbase import Base
# from sqlalchemy.ext.declarative import declarative_base

#Base = declarative_base()

class Pet(Base):
    __tablename__ = "pet"

    id = sa.Column(sa.String, primary_key=True)
    name = sa.Column(sa.String, nullable=False, index=True)
    birthday = sa.Column(sa.DATE)
    age = sa.Column(sa.INT)
    kennel = sa.Column(sa.String)
    summary = sa.Column(sa.String)
    image_url = sa.Column(sa.String)

    def __repr__(self):
        return "<Pet {}>".format(self.id)
