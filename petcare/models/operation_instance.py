import sqlalchemy as sa
import sqlalchemy.orm as orm
from petcare.models.modelbase import Base, ModelBase


class OperationInstance(Base, ModelBase):
    __tablename__ = "operation_instance"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    operator: str = sa.Column(sa.String)

    operation_id: str = sa.Column(sa.String, sa.ForeignKey("operation.id"))
    operation = orm.relation("Operation", back_populates="operation_instance")

    event_id: int = sa.Column(sa.Integer, sa.ForeignKey("event.id"))
    # event = orm.relation("Event", back_populates="operation")
