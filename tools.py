# -*- coding: utf-8 -*-
__author__ = 'beret'
import calendar
import json
import urllib
from datetime import datetime, date
from inspect import isfunction


def iso_to_py_date(txt_date):
    return date(*map(int, txt_date.split('-')))

def pl_to_py_date(txt_date):
    l = map(int, txt_date.split('.'))
    l.reverse()
    return date(*l)

def py_to_iso_date(date):
    return "-".join(map(str,[date.year, date.month, date.day]))


def to_js_date(py_date):
    return int(calendar.timegm(py_date.timetuple())) * 1000


def iso2js(iso_date):
    return to_js_date(iso_to_py_date(iso_date))