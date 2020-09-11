import sqlalchemy as sa
import sqlalchemy.orm as orm

from petcare.data.modelbase import Base

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
    import petcare.data.pet
    Base.metadata.create_all(engine)
