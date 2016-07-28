#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from datetime import date

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from .flagi import _gen_flags
from utils.tools import iso_to_py_date, py_to_iso_date, iso2js
from utils.decorators import parse_args, json_response, check_action, template_response

from tools import pl_to_py_date
from .models import Stay, Ship, Pier, Place, Flag, Marina, Hub, Connector, Contract, Leave, YBom
from .data import get_places, get_ships


class PierCreate(CreateView):
    model = Pier
    fields = ['name']
    success_url = reverse_lazy('places')


class PierUpdate(UpdateView):
    model = Pier
    fields = ['name']
    success_url = reverse_lazy('places')


class PierDelete(DeleteView):
    model = Pier
    success_url = reverse_lazy('places')


class PlaceCreate(CreateView):
    model = Place
    fields = ['name']
    success_url = reverse_lazy('places')


class PlaceUpdate(UpdateView):
    model = Place
    fields = ['name']
    success_url = reverse_lazy('places')


class PlaceDelete(DeleteView):
    model = Place
    success_url = reverse_lazy('places')


def _get_marina(*args, **kwargs):
    marina, created = Marina.objects.get_or_create(name=u"Marina Kamień Pomorski")
    _marina_dict = {
        "marina": marina,
    }
    return _marina_dict


def _get_get(request, *args, **kwargs):
    _kwargs = {}
    for name in request.GET:
        _kwargs[name] = request.GET[name]


def _get_post(request, *args, **kwargs):
    _kwargs = {}
    for name in request.POST:
        _kwargs[name] = request.POST[name]


def _get_boat_size(request, *args, **kwargs):
    boat_size_txt = request.GET.get('boat_size', None)
    _boat_size = {
        "boat_size": None,
    }
    if boat_size_txt:
        try:
            _boat_size = {
                "boat_size": float(boat_size_txt),
            }
        except:
            pass
    return _boat_size


def _get_range(request, *args, **kwargs):
    "&date_start=2016-7-4&date_end=2016-7-4"
    date_start_txt = request.GET.get('date_start', None)
    if date_start_txt:
        date_start = iso_to_py_date(date_start_txt)
    else:
        date_start = date.today()

    date_end_txt = request.GET.get('date_end', None)
    if date_end_txt:
        date_end = iso_to_py_date(date_end_txt)
    else:
        date_end = date.today()

    _range = {
        "date_start": date_start,
        "date_end": date_end
    }
    return _range


def close_popup(request, _id=None, **kwargs):
    place_id = _id
    _context = {
        "place_id": place_id
    }
    return render(request, "close_popup.html", _context)


def resident_place(request, date_start, date_end,  place, **kwargs):
    place_id = place.id
    ships = place.ships(date_start, date_end)
    residents = place.resident(date_start, date_end)
    _context = {
        "place_id": place_id,
        "place": place,
        "ships": ships,
        "residents": residents
    }
    return render(request, "resident_place.html", _context)


def booked_place(request, date_start, date_end,  place, **kwargs):
    place_id = place.id
    ships = place.ships(date_start, date_end)
    residents = place.resident(date_start, date_end)
    _context = {
        "place_id": place_id,
        "place": place,
        "ships": ships,
        "residents": residents
    }
    return render(request, "booked_place.html", _context)


def free_place(request, date_start, date_end, place=None, **kwargs):
    place_id = request.POST.get('place_id')
    if place_id:
        # try:
        ship_name = request.POST.get('ship_name')
        ship_id = request.POST.get('ship_id')
        length = request.POST.get('length')
        flag_code = request.POST.get('flag')
        contact_name = request.POST.get('contact_name')
        contact_phone = request.POST.get('contact_phone')
        contact_email = request.POST.get('contact_email')
        notices = request.POST.get('notices')
        # date_start = request.POST.get('date_start')
        # date_end = request.POST.get('date_end')
        flag = Flag.objects.get(code=flag_code)
        if not ship_id:
            ship = Ship(name=ship_name, length=int(length), flag=flag)
            ship.save()
        else:
            ship = Ship.objects.get(pk=int(ship_id))
        place = Place.objects.get(pk=int(place_id))
        type = request.POST.get('type')
        if type == "stay":
            stay = Stay(place=place, ship=ship, date_start=date_start, date_end=date_end, contact_name=contact_name, contact_phone=contact_phone, contact_email=contact_email, notices=notices)
            stay.save()
        elif type == "resident":
            contract = Contract(place=place, ship=ship, date_start=date_start, contact_name=contact_name, contact_phone=contact_phone, contact_email=contact_email, notices=notices)
            contract.save()
        return place_state(request, _id=place_id, **kwargs)
    elif place:
        place_id = place.pk
    else:
        return close_popup(request)

    flags = Flag.objects.all()
    _context = {
        "place": place,
        "flags": flags,
        "place_id": place_id
    }
    return render(request, "free_place.html", _context)


def edit_place(request, _id, **kwargs):
    place_id = request.POST.get('edit_place_id')
    if place_id:
        min_length = request.POST.get('min_length')
        max_length = request.POST.get('max_length')
        name = request.POST.get('name')
        place = Place.objects.get(pk=int(place_id))
        place.min_length = min_length
        place.max_length = max_length
        place.name = name
        place.save()
        return place_state(request, _id=place_id, **kwargs)
    elif _id:
        place_id = _id
        place = Place.objects.get(pk=int(place_id))
    else:
        return close_popup(request)

    _context = {
        "place": place,
        "place_id": place_id,
        "name": place.name,
        "min_length": place.min_length,
        "max_length": place.max_length
    }
    return render(request, "edit_place.html", _context)


def remove_stay(request, _id, **kwargs):
    stay = Stay.objects.get(pk=int(_id))
    place_id = stay.place.pk
    stay.delete()
    return place_state(request, _id=place_id, **kwargs)


def remove_contract(request, _id, **kwargs):
    contract = Contract.objects.get(pk=int(_id))
    place_id = contract.place.pk
    contract.delete()
    return place_state(request, _id=place_id, **kwargs)


PLACE_STATE_ACTION = {
    "resident": resident_place,
    "free": free_place,
    "booked": booked_place
}


@parse_args(_get_range)
def place_state(request, date_start, date_end, _id, **kwargs):
    place_id = int(_id)
    place = Place.objects.get(pk=place_id)
    state = place.state(date_start, date_end)
    return PLACE_STATE_ACTION[state](request, date_start=date_start, date_end=date_end, place=place, **kwargs)


def hub_state(request, _id, **kwargs):
    hub_id = int(_id)
    hub = Hub.objects.get(pk=hub_id)
    connectors = Connector.objects.filter(hub=hub)

    _context = {
        "hub": hub,
        "hub_id": hub_id,
        "connectors": connectors,
    }
    return render(request, "hub.html", _context)

def save_counters(request, _id, **kwargs):
    hub_id = int(_id)
    hub = Hub.objects.get(pk=hub_id)
    connectors = Connector.objects.filter(hub=hub)
    for connector in connectors:
        counter = request.GET.get('counter_%s' % connector.id)
        if counter:
            connector.set_counter(int(counter))
    return hub_state(request, _id=hub_id, **kwargs)

def connect_counter(request, _id, **kwargs):
    connector_id = int(_id)
    connector = Connector.objects.get(pk=connector_id)
    hub_id = connector.hub.id
    try:
        counter = int(request.GET.get('counter'))
        place_id = int(request.GET.get('place_id'))
    except:
        place_id = None

    if place_id:
        place = Place.objects.get(id=place_id)
        stays = place.ships(date_start=date.today(), date_end=date.today())
        if stays:
            stay = stays[0]
            connector.set_stay(stay, counter)
            return hub_state(request, _id=hub_id, **kwargs)
        contracts = place.resident(date_start=date.today(), date_end=date.today())
        if contracts:
            contract = contracts[0][0]
            connector.set_contract(contract, counter)
            return hub_state(request, _id=hub_id, **kwargs)
        place_id = None

    if not place_id:
        place_models = Place.objects.filter(pier=connector.hub.pier)
        places = []
        for place in place_models:
            state = place.state(date_start=date.today(), date_end=date.today())
            if state == "resident":
                contract = place.resident(date_start=date.today(), date_end=date.today())[0][0]
                if not contract.current_connector:
                    places.append((place, contract))
            elif state == "booked":
                stay = place.ships(date_start=date.today(), date_end=date.today())[0]
                if not stay.current_connector:
                    places.append((place, stay))
        _context = {
            "connector": connector,
            "places": places,
            "connector_id": connector_id,
            "hub_id": hub_id
        }
        return render(request, "connect_counter.html", _context)


PLACES_ACTIONS = (
    ("get_places", get_places),
    ("get_ships", get_ships),
    ("place_state", place_state, None),
    ("close_popup", close_popup, None),
    ("edit_place", edit_place, None),
    ("remove_stay", remove_stay, None),
    ("remove_contract", remove_contract, None),
    ("hub_state", hub_state, None),
    ("save_counters", save_counters, None),
    ("connect_counter", connect_counter, None)
)


@parse_args(_get_range, _get_marina, _get_boat_size)
@check_action(PLACES_ACTIONS, json_response())
def places(request, date_start, date_end, boat_size, marina, **kwargs):

    _template = "chart_ui.html"
    piers = []

    # if request.GET.get("gen_flags"):
    #     _gen_flags()
    #
    # if request.GET.get("gen_marina"):
    #     _gen_marina(marina)

    order_pier = request.GET.get("order_pier")
    if order_pier:
        new_order = filter(lambda x: x, order_pier.split('|'))
        for item in new_order:
            try:
                _order, _id = map(int, item.split(','))
                pier = Pier.objects.get(pk=_id)
                pier.order = _order
                pier.save()
            except:
                continue

    order_mooring = request.GET.get("order_mooring")
    if order_mooring:
        new_order = filter(lambda x: x, order_mooring.split('|'))
        for item in new_order:
            try:
                _order, _data = item.split(',')
                _order = int(_order)
                _pier_id, _type, _id = _data.split('__')
                _pier_id = int(_pier_id)
                _id = int(_id)
                pier = Pier.objects.get(pk=_pier_id)
                if _type == 'mooring':
                    _obj = Place.objects.get(pk=_id)
                elif _type == 'hub':
                    _obj = Hub.objects.get(pk=_id)
                _obj.order = _order
                _obj.save()
            except:
                continue

    place_id = request.POST.get('place_id')
    if place_id:
        # try:
        ship_name = request.POST.get('ship_name')
        ship_id = request.POST.get('ship_id')
        length = request.POST.get('length')
        flag_code = request.POST.get('flag')
        date_start = request.POST.get('date_start')
        date_end = request.POST.get('date_end')
        flag = Flag.objects.get(code=flag_code)
        if not ship_id:
            ship = Ship(name=ship_name, length=float(length), flag=flag)
            ship.save()
        else:
            ship = Ship.objects.get(pk=int(ship_id))
        place = Place.objects.get(pk=int(place_id))
        stay = Stay(place=place, ship=ship, date_start=pl_to_py_date(date_start), date_end=pl_to_py_date(date_end))
        stay.save()


    new_pier_name = request.POST.get('new_pier_name')
    if new_pier_name:
        # try:
        double_site = 'double_site' in request.POST
        new_pier = Pier(name=new_pier_name, marina=marina, double_site=double_site)
        new_pier.save()
        # except:
        #     pass

    new_mooring_name = request.POST.get('new_mooring_name')
    if new_mooring_name:
        # try:
        min_length = int(request.POST.get('min_length', 0))
        max_length = int(request.POST.get('max_length', 20))
        new_mooring_pier_id = int(request.POST.get('new_mooring_pier'))
        new_mooring_pier = Pier.objects.get(id=new_mooring_pier_id)
        new_mooring = Place(name=new_mooring_name, min_length=min_length, max_length=max_length, pier=new_mooring_pier)
        new_mooring.save()
        # except:
        #     pass

    new_hub_name = request.POST.get('new_hub_name')
    if new_hub_name:
        # try:
        amount = int(request.POST.get('amount', 0))
        new_hub_pier_id = int(request.POST.get('new_hub_pier'))
        new_hub_pier = Pier.objects.get(id=new_hub_pier_id)
        new_hub = Hub(name=new_hub_name, amount=amount, pier=new_hub_pier)
        new_hub.save()
        # except:
        #     pass

    for pier in Pier.objects.filter(marina=marina):
        _items = []
        places = Place.objects.filter(pier=pier)
        _len = len(places)
        if pier.left_site and pier.right_site:
            _len = int(_len/2)+(_len%2)
        pier.len = _len
        for place in Place.objects.filter(pier=pier):
            place.type = "place"
            stays = Stay.objects.filter(place=place)
            if stays:
                place.ship = stays[0].ship
            _items.append((place.order, place))
        for hub in Hub.objects.filter(pier=pier):
            hub.type = "hub"
            hub.connectors = Connector.objects.filter(hub=hub)
            _items.append((hub.order, hub))
        for ybom in YBom.objects.filter(pier=pier):
            ybom.type = "ybom"
            _items.append((ybom.order, ybom))
        piers.append([pier, map(lambda x: x[1], sorted(_items))])
        # column_size = max(2, int(12/(len(piers)+1)))

    ships = Ship.objects.all()
    flags = Flag.objects.all()

    context = {
        "title": unicode(marina),
        "piers": piers,
        # "column_size": column_size,
        "edit": True,
        "ships": ships,
        "flags": flags
    }
    return render(request, _template, context)

def map_demo(request):
    _template = "chart.html"
    context = {}
    return render(request, _template, context)

def moorings_demo(request):
    _template = "moorings_static.html"
    context = {}
    return render(request, _template, context)