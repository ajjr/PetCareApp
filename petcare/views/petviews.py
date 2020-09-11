import flask

blueprint = flask.Blueprint("pet", __name__, template_folder="templates")


@blueprint.route("/pet")
@blueprint.route("/pet/<string:pet_name>")
def pet(pet_name=None):
    pet_data = {
        "pet_name": "",
        "pet_species": "",
        "pet_race": "",
        "pet_birthday": "",
        "pet_owner": ""
    }
    if pet_name is not None:
        pet_data = {
            "pet_name": pet_name,
            "pet_species": "koira",
            "pet_race": "villakoira",
            "pet_birthday": "2009-04-13",
            "pet_owner": "Aki"
        }

    return flask.render_template("pet.html", pet_name=pet_data["pet_name"],
                                 pet_species=pet_data["pet_species"],
                                 pet_race=pet_data["pet_race"],
                                 pet_birthday=pet_data["pet_birthday"],
                                 pet_owner=pet_data["pet_owner"])
