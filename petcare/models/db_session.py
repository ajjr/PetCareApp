import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from sqlalchemy import text

from petcare.models.modelbase import Base

factory = None


def global_init(db_path: str):
    global factory

    if factory:
        return

    if not db_path or not db_path.strip():
        raise Exception("No DB Path")

    conn_str = db_path.strip()
    print("Connecting to {} with {}".format("Postgres", conn_str))

    engine = sa.create_engine(conn_str, echo=True)
    factory = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    import petcare.models.pet
    # noinspection PyUnresolvedReferences
    import petcare.models.event
    # noinspection PyUnresolvedReferences
    import petcare.models.user
    # noinspection PyUnresolvedReferences
    import petcare.models.breed
    # noinspection PyUnresolvedReferences
    import petcare.models.species
    Base.metadata.create_all(engine)


def create_session() -> Session:
    global factory

    session: Session = factory()
    session.expire_on_commit = False

    return session


def get_db_obj(obj_id, a_model):
    if obj_id is None or obj_id == "":
        return a_model()

    session = create_session()
    try:
        obj = session.query(a_model).filter(text(a_model.__tablename__ + ".id = " + str(obj_id))).first()
    finally:
        session.close()

    if obj is None:
        obj = a_model()

    return obj
