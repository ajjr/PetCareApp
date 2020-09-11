import datetime
import flask

import petcare.models.db_session as db_session

app = flask.Flask(__name__)

def main():
    print("Are we running?")
    setup_db()
    register_blueprints()
    app.run(debug=True)


def setup_db():
    db_path = "postgresql://postgres:e625BnU2J@localhost:5432/petcare"
    db_session.global_init(db_path)


def register_blueprints():
    from petcare.views import timeviews
    from petcare.views import petviews

    app.register_blueprint(timeviews.blueprint)
    app.register_blueprint(petviews.blueprint)

main()