# coding=utf-8

from copy import copy
import datetime

from icalendar import Calendar
from flask import Flask, request, abort
import requests


app = Flask(__name__)


def _filter_by_datetime(ical):
    filterd_ical = copy(ical)
    filterd_vevents = [x for x in filterd_ical.subcomponents
                       if x.name == 'VEVENT'
                       and isinstance(x.get('DTSTART').dt, datetime.datetime)]
    filterd_ical.subcomponents = filterd_vevents
    return filterd_ical


def _fetch_ical_content(url):
    response = requests.get(url)
    return response.text


@app.route('/filter_by_datetime', methods=['GET'])
def filter_handler():
    url = request.args.get('url')
    if url is None:
        abort(406)
    ical_text = _fetch_ical_content(url)
    ical_filtered = _filter_by_datetime(Calendar.from_ical(ical_text))

    return ical_filtered.to_ical()


app.run()
