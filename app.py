# coding=utf-8

from copy import copy, deepcopy
import datetime

from icalendar import Calendar
from flask import Flask, request, abort, Response
import requests


app = Flask(__name__)

VEVENT_DTSTART = 'DTSTART'
VEVENT_DTEND = 'DTEND'


def _filter_by_datetime(ical):
    filterd_ical = copy(ical)
    filterd_vevents = [x for x in filterd_ical.subcomponents
                       if x.name == 'VEVENT'
                       and isinstance(x.get('DTSTART').dt, datetime.datetime)]
    filterd_ical.subcomponents = filterd_vevents
    return filterd_ical


def _fix_due_datetime(vevent):
    if VEVENT_DTSTART not in vevent or VEVENT_DTEND not in vevent:
        return
    fixed_vevent = deepcopy(vevent)
    fixed_vevent[VEVENT_DTSTART].dt = vevent[VEVENT_DTEND].dt
    fixed_vevent[VEVENT_DTEND].dt = (vevent[VEVENT_DTEND].dt
                                     + (vevent[VEVENT_DTEND].dt - vevent[VEVENT_DTSTART].dt))
    return fixed_vevent


def _fetch_ical_content(url):
    response = requests.get(url)
    return response.text


@app.route('/filter_by_datetime', methods=['GET'])
def filter_handler():
    url = request.args.get('url')
    is_fix_due_datetime = request.args.get('is_fix_due_datetime')
    if url is None:
        abort(406)
    ical_text = _fetch_ical_content(url)
    ical_filtered = _filter_by_datetime(Calendar.from_ical(ical_text))
    if is_fix_due_datetime == 'true':
        ical_filtered.subcomponents = [_fix_due_datetime(x) for x in ical_filtered.subcomponents]

    # fix ical bug: status unexpected newline, https://github.com/collective/icalendar/issues/312
    # fix ical bug: breakline
    ical_sanitized = ical_filtered.to_ical() \
        .decode('utf-8') \
        .replace('Status\r\n :', 'Status:') \
        .replace('\r\n', '\n')
    return Response(ical_sanitized, mimetype='text/calendar')


# app.run(debug=True)
app.run()
