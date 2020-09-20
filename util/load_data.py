from petcare.config.config import Config
import petcare.models.db_session as db
from petcare.models.operation import Operation
from petcare.models.breed import Breed
from petcare.models.species import Species
from petcare.models.user import User


def main():
    init_db()
    sps_dog, sps_cat = insert_species()
    insert_operations(read_input_file("../data/operaatiot.txt"))
    insert_dog_breeds(read_input_file("../data/koirarodut.txt"), sps_dog)
    insert_cat_breeds(read_input_file("../data/kissarodut.txt"), sps_cat)


def read_input_file(file_path: str):
    with open(file_path, "r") as fin:
        data = fin.readlines()
    return data


def insert_test_user(username="Test User"):
    session = db.create_session()
    user = User()
    user.id = 3 # TODO: Get rid of magic user id
    user.username = username
    user.email = "fake"
    user.password = "this will be hashed"
    session.add(user)
    session.commit()
    session.close()


def insert_species():
    session = db.create_session()
    dog = Species()
    dog.name = "koira"
    session.add(dog)
    cat = Species()
    cat.name = "kissa"
    session.add(cat)
    session.commit()

    sps_dog = dog.id
    sps_cat = cat.id
    session.close()

    return sps_dog, sps_cat


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

if __name__ == "__main__":
    main()
