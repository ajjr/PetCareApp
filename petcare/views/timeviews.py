import datetime
import calendar

import flask

import petcare.services.event_service as event_service
from petcare.services import auth_cookie, pet_service

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


def event_insert_data(user_id):
    return map(lambda x: x[0], pet_service.get_pets_for_user(user_id)), \
           event_service.get_operations()


@blueprint.route("/day", defaults={"date_day": None})
@blueprint.route("/day/<string:date_day>")
def day(date_day):
    user_id = auth_cookie.get_auth(flask.request)
    if not user_id:
        return flask.redirect("/login", code=302)

    if date_day is None:
        date_day = str(datetime.date.today())
    day_ = datetime.date.fromisoformat(date_day)
    # user_id = 3
    # Display events for day_
    # next_events = get_next_events()
    events = event_service.get_events_between(day_ - datetime.timedelta(days=1), day_ + datetime.timedelta(days=1),
                                              user_id)
    #pet_data = pet_service.get_pets_for_user(user_id)
    pet_data, operations = event_insert_data(user_id)

    return flask.render_template("day.html", today=datetime.date.today().ctime(), day_str=day_.ctime(),
                                 next_events=events[(day_.month, day_.day)], pet_data=pet_data, operations=operations, user_id=user_id)


@blueprint.route("/week")
@blueprint.route("/week/<string:date_day>")
def week(date_day=None):
    user_id = auth_cookie.get_auth(flask.request)
    if not user_id:
        return flask.redirect("/login", code=302)

    if date_day is None:
        date_day = str(datetime.date.today())
    a_date = datetime.date.fromisoformat(date_day)
    start_of_week = a_date.day - a_date.weekday()
    end_of_week = start_of_week + 6
    a_year, a_week, day_of_week = a_date.isocalendar()
    month_first, month_last = calendar.monthrange(a_year, a_date.month)
    start_month = a_date.month
    end_month = a_date.month

    if start_of_week < 1:
        start_month = a_date.month - 1
        month_last = calendar.monthrange(a_year, a_date.month - 1)[1]
        start_of_week = start_of_week + month_last
    if end_of_week > month_last:
        end_of_week = end_of_week - calendar.monthrange(a_year, a_date.month)[1]
        end_month = a_date.month + 1

    events = event_service.get_events_between(datetime.datetime(a_year, start_month, start_of_week),
                                              datetime.datetime(a_year, end_month, end_of_week),
                                              user_id)
    pet_data, operations = event_insert_data(user_id)
    print(start_month, start_of_week, end_month, end_of_week)
    from pprint import pprint
    pprint(events)

    return flask.render_template("week.html", start_of_week=start_of_week, year=a_year, month=a_date.month, week=a_week,
                                 day_of_week=day_of_week, start_month=start_month, end_month=end_month, month_last=month_last, events=events, user_id=user_id, operations=operations, pet_data=pet_data)


@blueprint.route("/month")
@blueprint.route("/month/<string:date_day>")
def month(date_day=None):
    user_id = auth_cookie.get_auth(flask.request)
    if not user_id:
        return flask.redirect("/login", code=302)

    if date_day is None:
        date_day = str(datetime.date.today())
    elif date_day.isnumeric():
        if 0 < int(date_day) < 10:
            date_day = str(datetime.date.today().year) + "-0" + date_day + "-01"
        elif 10 <= int(date_day) <= 12:
            date_day = str(datetime.date.today().year) + "-" + date_day + "-01"

    a_date = datetime.date.fromisoformat(date_day)
    a_month = a_date.month
    a_year = a_date.year
    a_day = a_date.day
    month_start, month_end = calendar.monthrange(a_year, a_month)
    formatted_date = str(a_date.year) + "-" + ("0" + str(a_date.month))[-2:] + "-"

    events = event_service.get_events_between(datetime.datetime(a_year, a_month, 1),
                                              datetime.datetime(a_year, a_month, month_end),
                                              user_id)
    pet_data, operations = event_insert_data(user_id)

    # event_dict[(event.date.month, event.date.day)] = el

    print(events)

    return flask.render_template("month.html", year=a_year, month=a_month, day=a_day, month_start=month_start,
                                 month_end=month_end, events=events, date_stub=formatted_date, user_id=user_id, operations=operations, pet_data=pet_data)


@blueprint.route("/insert_event", methods=["POST"])
def insert_event():
    req = flask.request
    user_id = auth_cookie.get_auth(req)
    if not user_id:
        return flask.redirect("/login", code=302)

    event_date = datetime.datetime.fromisoformat(req.form["event_date"] + " "
                                                 + req.form["event_time"])
    event_desc = req.form["event_description"]
    pet_id = req.form["pet_id"]


    if req.form["operation_id"]:
        print("Inserting operation, too.")
        operation_id = req.form["operation_id"]
        operator = req.form["operator"]
        if req.form["repeat_check"]:
            rdate = datetime.datetime.combine(datetime.date.fromisoformat(req.form["repeat_rdate"]), datetime.datetime.min.time())
            event_service.insert_repeating_event(event_date, rdate, event_desc, user_id, pet_id, operation_id, operator)
        else:
            event_service.insert_event(event_date, event_desc, user_id, pet_id, operation_id, operator)
        target = req.referrer if req.referrer else "/"
        return flask.redirect(target, code=302)

    print("Insert event", event_date)
    event_service.insert_event(event_date, event_desc, user_id, pet_id)
    target = req.referrer if req.referrer else "/"
    return flask.redirect(target, code=302)


@blueprint.route("/mark_done/<int:event_id>")
def mark_done(event_id: int):
    req = flask.request
    user_id = auth_cookie.get_auth(req)
    if not user_id:
        return flask.redirect("/login", code=302)

    event_service.update_event_done(event_id)

    target = req.referrer if req.referrer else "/"
    return flask.redirect(target, code=302)


@blueprint.route("/insert_repeat")
def insert_repeat():
    event_service.insert_repeating_event(
        datetime.datetime(2020, 9, 27, 11, 00),
        datetime.datetime(2020, 11, 22, 11, 00),
        "", 0, 0)

    target = req.referrer if req.referrer else "/"
    return flask.redirect(target, code=302)

