import flask
from flask import request
from flask import redirect
import petcare.services.pet_service as pet_service
import petcare.services.user_service as user_service

blueprint = flask.Blueprint("pet", __name__, template_folder="templates")


@blueprint.route("/pet", methods=["GET"])
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
    pet_id = None
    if pet_name is not None:
        (a_pet, user) = pet_service.get_pet_by_name(pet_name, 3)
        pet_id = a_pet.id
        pet_data = {
            "name": a_pet.name,
            "birthday": a_pet.birthday,
            "owner": user.id,
            "breeder": a_pet.breeder,
            "summary": a_pet.summary,
            "image_url": a_pet.image_url
        }
        breed_data = {
            "name": a_pet.breed.id,
            "id": a_pet.breed_id
        }
        sps_data = {
            "name": a_pet.breed.species.id,
            "id": a_pet.breed.species_id
        }

    breeds = pet_service.get_breeds()
    species = pet_service.get_species()
    return flask.render_template("pet.html", pet_id=pet_id, pet_data=pet_data, species_data=sps_data,
                                 breed_data=breed_data,
                                 breeds=breeds, species=species)


@blueprint.route("/pet", methods=["POST"])
def post_pet():
    pet_data = {
        "name": request.form["pet_name"].strip(),
        "breed_id": request.form["breed_id"].strip(),
        "owner_id": "3",  # request.form["owner_id"].strip(),
        "birthday": request.form["pet_birthday"].strip(),
        "breeder": request.form["breeder"].strip(),
        "summary": request.form["pet_summary"].strip(),
        "image_url": request.form["pet_image_url"].strip()
    }

    breed = pet_service.get_breed(request.form["breed_id"])
    owner = user_service.get_user(3)
    a_pet = None
    if "pet_id" not in request.form.keys():
        print("Insetrting new pet with {} and {}".format(breed.name, owner.name))
        a_pet = pet_service.commit_pet(**pet_data)
    else:
        print("Updating pet {}".format(""))
        pet_data["pet_id"] = request.form["pet_id"].strip()
        a_pet = pet_service.commit_pet(**pet_data)

    if not a_pet:
        return flask.abort(status=402)

    return flask.redirect("/pet/" + a_pet.name, code=302)
