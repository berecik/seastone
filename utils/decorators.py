# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render


def parse_args(*parse_args_funs):
    def _parse_decorator(view_fun):
        def _view_wrpapper(request, *args, **kwargs):
            if parse_args_funs:
                for _fun in parse_args_funs:
                    kwargs.update(_fun(request, *args, **kwargs))
            return view_fun(request, *args, **kwargs)
        return _view_wrpapper
    return _parse_decorator


def json_response(*parse_args_funs):
    def _json_response(view_fun):
        def _json_view_fun(request, *args, **kwargs):
            result = view_fun(*args, **kwargs)
            return JsonResponse(result, safe=False)
        return parse_args(*parse_args_funs)(_json_view_fun)
    return _json_response


def template_response(template_name, *parse_args_funs):
    def _template_response(view_fun):
        def _view_fun(request, *args, **kwargs):
            context = view_fun(*args, **kwargs)
            return render(request, template_name, context)
        return parse_args(*parse_args_funs)(_view_fun)
    return _template_response


def check_action(action_list, *action_decorators):
    if action_decorators:
        decorators = lambda _view: reduce(lambda _result_view, _decorator: _decorator(_result_view), action_decorators, _view)
    else:
        decorators = lambda f: f

    def _action_decorator(view_fun):
        def _view_fun(request, *args, **kwargs):
            for action_data in action_list:
                if len(action_data) == 2:
                    _decorators = decorators
                else:
                    if action_data[2]:
                        _decorators = action_data[2]
                    else:
                        _decorators = lambda f: f
                if action_data[0] in request.GET:
                    action_id = request.GET[action_data[0]]
                    if action_id:
                        kwargs["_id"] = action_id
                    else:
                        kwargs["_id"] = None
                    return _decorators(action_data[1])(request, *args, **kwargs)
            return view_fun(request, *args, **kwargs)
        return _view_fun
    return _action_decorator
