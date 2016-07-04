import json

from django.shortcuts import render

import common_settings


def render_js(request, *args, **kwargs):
    response = render(request, *args, **kwargs)
    return response

def settings_js(request):
    _settings = {}
    _settings_names = dir(common_settings)
    for _name in _settings_names:
        if _name[0] != '_' and _name[0].isupper():
            _settings[_name] = json.dumps(getattr(common_settings, _name, None))
    context = {
        "settings_dir": _settings
    }
    response = render(request, "settings.js", context)
    return response
