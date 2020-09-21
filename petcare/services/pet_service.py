from typing import List

import petcare.models.db_session as db
from petcare.models.db_session import get_db_obj
from petcare.models.pet import Pet
from petcare.models.breed import Breed
from petcare.models.species import Species
from petcare.models.user import User
import petcare.services.user_service as user_service
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


def get_pet(pet_id=None) -> Pet:
    if pet_id is None:
        return Pet()
    return db.get_db_obj(pet_id, Pet)


def get_pet_by_name(pet_name, owner_id) -> Pet:
    session = db.create_session()
    try:
        # pet = session.query(Pet).filter(and_(Pet.name == pet_name, Pet.owner.id == owner_id))
        pet = session.query(Pet, User).filter(Pet.name == pet_name).filter(User.id == owner_id).first()
    finally:
        session.close()
    return pet


def get_pets_for_user(user_id):
    session = db.create_session()
    return session.query(Pet, Breed, Species).select_from(Pet).\
        join(Breed).\
        join(Species).\
        filter(Pet.user_id == user_id).order_by(Species.id).all()


def insert(obj):
    print("--Commiting into database:", obj, obj.birthday, obj.breed, obj.owner)
    session = db.create_session()
    try:
        if obj.id is None:
            session.add(obj)
        else:
            session.merge(obj)
        session.commit()
    finally:
        session.close()

    return obj


def commit_pet(name: str, breed_id: str, owner_id: str,
               pet_id=None,
               birthday=None,
               breeder=None,
               summary=None,
               image_url=None) -> Pet:
    """
    Commit pet data into database.
    @param name: Pet name used in url routing
    @param breed_id:
    @param owner_id:
    @param pet_id:
    @param birthday:
    @param breeder:
    @param summary:
    @param image_url:
    @return:
    """
    print("***********************************************", pet_id)
    pet = get_pet(pet_id)
    pet.name = name
    breed = get_breed(breed_id)
    if pet.breed is None:
        pet.breed = breed
    elif pet.breed.id != breed.id:
        pet.breed = breed

    owner = user_service.get_user(owner_id)
    if pet.owner is None or pet.owner.id != owner.id:
        pet.owner = owner

    pet.birthday = birthday if birthday != "" else None
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
