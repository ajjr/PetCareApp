print("This is", __name__)
import flask

import petcare.models.db_session as db_session
from petcare.config.config import Config

app = flask.Flask(__name__)


def main():
    configure()
    app.run(debug=True)


def configure():
    config = Config()
    setup_db(config.DATABASE_URI)
    register_blueprints()


def setup_db(db_path):
    db_session.global_init(db_path)


def register_blueprints():
    from petcare.views import timeviews
    from petcare.views import petviews
    from petcare.views import home_views

    app.register_blueprint(timeviews.blueprint)
    app.register_blueprint(petviews.blueprint)
    app.register_blueprint(home_views.blueprint)


if __name__ == "__main__":
    main()
else:
    configure()
