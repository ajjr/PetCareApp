import datetime
from calendar import monthrange
from collections import defaultdict

import flask

import petcare.services.event_service as event_service

blueprint = flask.Blueprint("time", __name__, template_folder="templates")


# Some dummy models for starters
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


@blueprint.route("/month")
@blueprint.route("/month/<string:date_day>")
def month(date_day=None):
    user_id = 3

    if date_day is None:
        date_day = str(datetime.datetime.today())
    a_date = datetime.datetime.fromisoformat(date_day)
    a_month = a_date.month
    a_year = a_date.year
    a_day = a_date.day
    month_start, month_end = monthrange(a_year, a_month)

    events = event_service.get_events_between(datetime.datetime(a_year, a_month, month_start),
                                              datetime.datetime(a_year, a_month, month_end),
                                              user_id)

    event_dict = defaultdict(list)
    for event in events:
        event_dict[(event.date.month, event.date.day)].append({
            "title": event.description,
            "pet_name": event.pet.name,
            "pet_id": event.pet_id,
            "event_id": event.id
        })
        # event_dict[(event.date.month, event.date.day)] = el

    print(events)

    return flask.render_template("month.html", year=a_year, month=a_month, day=a_day, month_start=month_start,
                                 month_end=month_end, events=event_dict)
