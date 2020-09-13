import flask
from flask import request
from flask import redirect
import petcare.services.pet_service as pet_service
import petcare.services.user_service as user_service
from petcare.views.timeviews import blueprint
import petcare.services.event_service as event_service

blueprint = flask.Blueprint("home", __name__, template_folder="templates")


@blueprint.route("/")
def index():
    events = event_service.get_current_events()

    return flask.render_template("index.html", current_events=events)
