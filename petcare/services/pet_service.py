import petcare.models.db_session as db
from petcare.models.db_session import get_db_obj
from petcare.models.pet import Pet
from petcare.models.breed import Breed
from petcare.models.species import Species
from sqlalchemy import and_


def get_breeds() -> list:
    session = db.create_session()
    try:
        breeds = session.query(Breed).all()
    finally:
        session.close()
    return breeds


def get_species() -> list:
    session = db.create_session()
    try:
        species = session.query(Species).all()
    finally:
        session.close()
    return species


def get_a_species(sps_id) -> Species:
    return db.get_db_obj(sps_id, Species)


def get_breed(breed_id) -> Breed:
    return db.get_db_obj(breed_id, Breed)


def get_pet(pet_id) -> Pet:
    return db.get_db_obj(pet_id, Pet)


def get_pet_by_name(pet_name, owner_id) -> Pet:
    session = db.create_session()
    try:
        pet = session.query(Pet).filter(and_(Pet.name == pet_name, Pet.owner.id == owner_id))
    finally:
        session.close()
    return pet


def insert(obj):
    session = db.create_session()
    try:
        session.add(obj)
        session.commit()
    finally:
        session.close()

    return obj


def insert_pet(name, breed, owner, birthday=None, breeder=None, summary=None, image_url=None) -> Pet:
    pet = Pet()
    pet.name = name
    pet.breed = breed
    pet.owner = owner
    pet.birthday = birthday
    pet.breeder = breeder
    pet.summary = summary
    pet.image_url = image_url

    return insert(pet)


def insert_species(name) -> Species:
    species = Species()
    species.name = name

    return insert(species)


def inset_breed(name, species) -> Breed:
    breed = Breed()
    breed.name = name
    breed.species = species

    return insert(breed)
