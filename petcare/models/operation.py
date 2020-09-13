import sqlalchemy as sa
import sqlalchemy.orm as orm
from petcare.models.modelbase import Base, ModelBase


class Operation(Base, ModelBase):
    __tablename__ = "operation"

    id: str = sa.Column(sa.String, primary_key=True)

    # events = orm.relation("OperationInstance", back_populates="event")
    operation_instance = orm.relation("OperationInstance", back_populates="operation")
