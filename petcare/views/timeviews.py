import datetime
import flask

blueprint = flask.Blueprint("time", __name__, template_folder="templates")


# Some dummy data for starters
def get_next_events():
    return [
        {"pet_name": "Rekku",
         "event_name": "Kynsien leikkuu",
         "event_date": datetime.date.fromisoformat("2020-10-19")},
        {"pet_name": "Paukku",
         "event_name": "Antibiootti",
         "event_date": datetime.date.fromisoformat("2020-10-19"),
         "event_time": datetime.time.fromisoformat("08:00:00")},
        {"pet_name": "Paukku",
         "event_name": "Antibiootti",
         "event_date": datetime.date.fromisoformat("2020-10-19"),
         "event_time": datetime.time.fromisoformat("20:00:00")},
        {"pet_name": "Paukku",
         "event_name": "Kynsien leikkuu",
         "event_date": datetime.date.fromisoformat("2020-10-20")},
        {"pet_name": "Paukku",
         "event_name": "Antibiootti",
         "event_date": datetime.date.fromisoformat("2020-10-20"),
         "event_time": datetime.time.fromisoformat("08:00:00")},
        {"pet_name": "Paukku",
         "event_name": "Antibiootti",
         "event_date": datetime.date.fromisoformat("2020-10-20"),
         "event_time": datetime.time.fromisoformat("20:00:00")},
        {"pet_name": "Rekku",
         "event_name": "Pesu",
         "event_date": datetime.date.fromisoformat("2020-10-24")}
    ]


@blueprint.route("/")
def index():
    return flask.render_template("index.html")


@blueprint.route("/day", defaults={"date_day": None})
@blueprint.route("/day/<string:date_day>")
def day(date_day):
    if date_day is None:
        date_day = str(datetime.date.today())
    day_ = datetime.date.fromisoformat(date_day)
    # Display events for day_
    next_events = get_next_events()
    return flask.render_template("day.html", today=datetime.date.today().ctime(), day_str=day_.ctime(),
                                 next_events=next_events)


@blueprint.route("/week")
@blueprint.route("/week/<string:date_day>")
def week(date_day=None):
    if date_day is None:
        date_day = str(datetime.date.today())
    week_ = datetime.date.fromisoformat(date_day).isocalendar()

