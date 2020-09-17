from petcare.config.config import Config
import petcare.models.db_session as db
from petcare.models.operation import Operation
from petcare.models.breed import Breed
from petcare.models.species import Species


def main():
    init_db()
    insert_operations(read_input_file("../data/operaatiot.txt"))
    insert_dog_breeds(read_input_file("../data/koirarodut.txt"))
    insert_cat_breeds(read_input_file("../data/kissarodut.txt"))


def read_input_file(file_path: str):
    with open(file_path, "r") as fin:
        data = fin.readlines()
    return data


def insert_operations(data):
    session = db.create_session()
    for row in data:
        o = Operation()
        o.id = row.strip()
        session.add(o)

    session.commit()
    session.close()


def insert_dog_breeds(data, species_id=1):
    session = db.create_session()
    s = db.get_db_obj(species_id, Species)
    for row in data:
        b = Breed()
        b.name = row.strip()
        b.species = s
        session.add(b)

    session.commit()
    session.close()


def insert_cat_breeds(data, species_id=2):
    session = db.create_session()

    s = db.get_db_obj(species_id, Species)
    for row in data:
        b = Breed()
        b.name = row.strip()
        b.species = s
        session.add(b)

    session.commit()
    session.close()


def init_db():
    db_path = Config.DATABASE_URI
    db.global_init(db_path)


main()
