import flask
from flask import request
import petcare.services.pet_service as pet_service
import petcare.services.user_service as user_service

blueprint = flask.Blueprint("pet", __name__, template_folder="templates")


@blueprint.route("/pet", methods=["GET", "POST"])
@blueprint.route("/pet/<string:pet_name>")
def pet(pet_name=None):
    pet_data = {
        "name": "",
        "birthday": "",
        "owner": "",
        "breeder": "",
        "summary": "",
        "image_url": ""
    }
    breed_data = {
        "name": "",
        "id": ""
    }
    sps_data = {
        "name": "",
        "id": ""
    }
    if pet_name is not None:
        (a_pet, user) = pet_service.get_pet_by_name(pet_name, 3)
        pet_data = {
            "name": a_pet.name,
            "birthday": a_pet.birthday,
            "owner": user.name,
            "breeder": a_pet.breeder,
            "summary": a_pet.summary,
            "image_url": a_pet.image_url
        }
        breed_data = {
            "name": a_pet.breed.name,
            "id": a_pet.breed_id
        }
        sps_data = {
            "name": a_pet.breed.species.name,
            "id": a_pet.breed.species_id
        }

    if request.method == "POST":
        breed = pet_service.get_breed(request.form["breed_id"])
        owner = user_service.get_user(3)
        if "pet_id" not in request.form.keys():
            print("Insetrting new pet with {} and {}".format(breed.name, owner.name))
            # pet_service.insert_pet(request.form["pet_name"],
            #                       breed, owner)
        else:
            print("Updating pet {}".format(""))
            pet_service.update_pet()

    else:
        pet_data["pet_name"] = "No luck!"

    breeds = pet_service.get_breeds()
    species = pet_service.get_species()
    return flask.render_template("pet.html", pet_data=pet_data, species_data=sps_data, breed_data=breed_data,
                                 breeds=breeds, species=species)
