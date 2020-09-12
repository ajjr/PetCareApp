import flask

import petcare.models.db_session as db_session
from petcare.config.config import Config

app = flask.Flask(__name__)


def main():
    config = Config()
    setup_db(config.DATABASE_URI)
    register_blueprints()
    app.run(debug=True)


def setup_db(db_path):
    db_session.global_init(db_path)


def register_blueprints():
    from petcare.views import timeviews
    from petcare.views import petviews

    app.register_blueprint(timeviews.blueprint)
    app.register_blueprint(petviews.blueprint)

main()