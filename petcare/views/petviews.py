from datetime import datetime

import flask
from flask import request
from flask import redirect
import petcare.services.pet_service as pet_service
import petcare.services.user_service as user_service
from petcare.services import auth_cookie, event_service

blueprint = flask.Blueprint("pet", __name__, template_folder="templates")


@blueprint.route("/pet", methods=["GET"])
@blueprint.route("/pet/<string:pet_name>")
def pet_get(pet_name=None):
    user_id = auth_cookie.get_auth(flask.request)
    if not user_id:
        return flask.redirect("/login", code=302)

    pet_data = {
        "name": "",
        "birthday": "",
        "owner": user_service.get_user(user_id).name,
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
    pet_id = ""
    if pet_name is not None:
        (a_pet, user) = pet_service.get_pet_by_name(pet_name, user_id)
        today = datetime.today()
        birthday = a_pet.birthday
        pet_id = a_pet.id
        pet_data = {
            "name": a_pet.name,
            "birthday": birthday,
            "owner": user.name,
            "breeder": a_pet.breeder,
            "summary": a_pet.summary,
            "image_url": a_pet.image_url,
            "age": today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
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
    events = event_service.get_current_events(user_id, pet_id, 5)
    return flask.render_template("pet.html", pet_id=pet_id, pet_data=pet_data, species_data=sps_data,
                                 breed_data=breed_data,
                                 breeds=breeds, species=species, user_id=user_id, events=events)


@blueprint.route("/pet", methods=["POST"])
def pet_post():
    user_id = auth_cookie.get_auth(flask.request)
    if not user_id:
        return flask.redirect("/login", code=302)

    pet_data = {"name": request.form["pet_name"].strip(), "breed_id": request.form["breed_id"].strip(),
                "owner_id": user_id, "birthday": request.form["pet_birthday"].strip(),
                "breeder": request.form["breeder"].strip(), "summary": request.form["pet_summary"].strip(),
                "image_url": request.form["pet_image_url"].strip(), "pet_id": request.form["pet_id"].strip()}

    if not (pet_data["birthday"] and pet_data["name"]):
        # Pet must have at least a name and a birthday
        referrer = request.referrer if request.referrer else "/"
        return flask.redirect(referrer, code=302)

    # Delete Pet
    if "delete" in request.form.keys():
        print("Delete requested for {}".format(pet_data["name"], pet_data["pet_id"]))
        # Perform delete
        pet_service.delete_pet(pet_data["pet_id"])
        return flask.redirect("/profile", code=302)

    breed = pet_service.get_breed(request.form["breed_id"])
    owner = user_service.get_user(user_id)
    a_pet = None
    pet_data["pet_id"] = request.form["pet_id"].strip()
    if "pet_id" not in request.form.keys() or request.form["pet_id"] != "":
        print("Insetrting new pet with {} and {}".format(breed.name, owner.name))
        a_pet = pet_service.commit_pet(**pet_data)
    else:
        print("Updating pet {}".format(""))
        pet_data["pet_id"] = request.form["pet_id"].strip()
        a_pet = pet_service.commit_pet(**pet_data)

    if not a_pet:
        return flask.abort(status=402)

    return flask.redirect("/pet/" + a_pet.name, code=302)
