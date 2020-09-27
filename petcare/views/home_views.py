from collections import defaultdict

import flask
from flask import request
from flask import redirect
import petcare.services.pet_service as pet_service
import petcare.services.user_service as user_service
from petcare.services import auth_cookie
from petcare.views.timeviews import blueprint
import petcare.services.event_service as event_service

blueprint = flask.Blueprint("home", __name__, template_folder="templates")

#### Default views

@blueprint.route("/")
def index():
    user_id = auth_cookie.get_auth(flask.request)
    if not user_id:
        return flask.redirect("/login", code=302)

    events = event_service.get_current_events(user_id)

    return flask.render_template("index.html", user_id=user_id, current_events=events)


@blueprint.route("/profile", methods=["GET"])
def profile():
    user_id = auth_cookie.get_auth(flask.request)
    if not user_id:
        return flask.redirect("/login", code=302)

    user = user_service.get_user(user_id)

    pets = pet_service.get_pets_for_user(user_id)
    pet_data = defaultdict(list)
    for pet, breed, species in pets:
        pet_data[species.name].append({
            "name": pet.name,
            "breed": breed.name
        })

    return flask.render_template("/profile.html", user_id=user_id, username=user.username, species=list(pet_data.keys()), pet_data=pet_data)


#### Login methods


@blueprint.route("/login", methods=["GET"])
def login_get():
    return flask.render_template("login.html")


@blueprint.route("/login", methods=["POST"])
def login_post():
    username = flask.request.form["username"]
    password = flask.request.form["password"]

    user = user_service.authenticate(username, password)
    if not user:
        resp = flask.redirect("/login", code=302)
        return resp

    resp = flask.redirect("/", code=302)
    auth_cookie.set_auth(resp, user.id)
    return resp


@blueprint.route("/logout", methods=["GET"])
def logout():
    resp = flask.redirect("/login", code=302)
    auth_cookie.logout(resp)
    return resp


#### Register new user and manage account


@blueprint.route("/register", methods=["GET"])
@blueprint.route("/account", methods=["GET"])
@blueprint.route("/account/<string:state>", methods=["GET"])
def account_get(state=""):
    # TODO: if state is new_user we could do something different
    user_id = auth_cookie.get_auth(flask.request)
    if user_id:
        user = user_service.get_user(user_id)
        if user:
            username = user.username
            name = user.name
            email = user.email

            return flask.render_template("account.html", username=username,
                                         name=name, email=email, user_id=user_id)

    return flask.render_template("account.html")


@blueprint.route("/account", methods=["POST"])
def account_post():
    username = flask.request.form["username"]
    name = flask.request.form["name"]
    email = flask.request.form["email"]
    password = flask.request.form["password"]

    if not username or not name or not email or not password:
        error = "Pakollisia tietoja puuttuu!"
        return flask.render_template("/account.html", username=username,
                                     name=name, email=email, error=error)

    user = user_service.create_user(username, name, email, password)
    if not user:
        error = "Antamasi käyttäjätunnus tai sähköpostiosoite on varattu."
        return flask.render_template("/account.html", username=username,
                                     name=name, email=email, error=error)

    resp = flask.redirect("/account/new_user", code=302)
    auth_cookie.set_auth(resp, user.id)

    return resp
