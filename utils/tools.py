# -*- coding: utf-8 -*-
__author__ = 'beret'
import pprint
import json
import os
import calendar
from datetime import datetime, date

try:
    from django.conf import settings
    DEBUG_FILE = settings.DEBUG_FILE
    QUERY_DEBUG = settings.QUERY_DEBUG
except:
    QUERY_DEBUG = True
    DEBUG_FILE = os.path.join(settings.BASE_DIR, '_debug_log.txt')



_cout = True
_pp = pprint.PrettyPrinter(indent=2)


def iso_to_py_date(txt_date):
    return date(*map(int, txt_date.split('-')))


def py_to_iso_date(date):
    return "-".join(map(str,[date.year, date.month, date.day]))


def to_js_date(py_date):
    return int(calendar.timegm(py_date.timetuple())) * 1000


def iso2js(iso_date):
    return to_js_date(iso_to_py_date(iso_date))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def try_int(data, default=None):
    try:
        if isinstance(data, (list, tuple)):
            return try_int(data[0], default)
        return int(data)
    except:
        return default


def _get_write(f):
    if f:
        if f == True:
            _debug_file = open(DEBUG_FILE, 'a')
        else:
            _debug_file = f
        return _debug_file.write
    return False


def get_pp(*args, **kwargs):
    def __pp(data):
        return pp(data, *args, **kwargs)
    return __pp


def pp(txt, parse=None, cout=_cout, f=True, string=None):
    if string==None:
        string = not cout
    if parse == 'json':
        _txt = json.loads(txt)
    elif parse:
        _txt = parse(txt)
    else:
        _txt = txt
    w = _get_write(f)
    if w:
        w(_txt)
    if cout:
        _pp.pprint(_txt)
    if string:
        return _pp.pformat(_txt)


def p(parse=None, cout=_cout, f=True, **kwargs):
    def __pp(*txts):
        for txt in txts:
            pp(txt=txt, parse=parse, cout=cout, f=f, **kwargs)
    return __pp


def jprint(json_txt, f=False):
    if f:
        cout = False
    else:
        cout = True
    return pp(txt=json_txt, parse='json', cout=cout, f=f)


def del_key(dict, key):
    if key in dict:
        del dict[key]
        return True
    return False


class BeretDebug:
    def __init__(self,
            value = None,
            label="DEBUG",
            json_parse=False,
            cout=True,
            force_cout=None,
            before=lambda txt: txt,
            after=lambda txt: txt):
        self.label = label
        self.json_parse = json_parse
        self.cout = cout
        self.force_cout = force_cout
        self.before = before
        self.after = after
        self.value = value
        self.debug_str = ""
        self.value_str = ""
        self._current_value = None

    def set(self, value=None):
        if value:
            self.value = value
        if self._current_value != self.value:
            _parse = None
            if self.json_parse:
                _parse = 'json'
            self.value_str = pp(self.value, parse=_parse, cout=False, f=False, string=True)
            self.debug_str = ""
            self.debug_str += "==============%s=============\n" % self.label
            self.debug_str = self.before( self.debug_str)
            self.debug_str += "%s\n" % self.value_str
            self.debug_str = self.after( self.debug_str)
            self.debug_str += "=======END=OF=%s=============\n" % self.label

    def show(self, value=None):
        self.set(value)
        if self.force_cout or (QUERY_DEBUG and self.cout):
            print self.debug_str
        return self.debug_str

    def __unicode__(self):
        return self.show()


def _debug(*args, **kwargs):
    return BeretDebug(*args, **kwargs).show()


def env(fun):
    def _fun_wrap(*args, **kwargs):
        import os
        import sys
        SETTINGS_PATH = "seastone"
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" % SETTINGS_PATH)
        sys.path.append(settings.BASE_DIR)

        return fun(*args, **kwargs)

    return _fun_wrap


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