#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _

from tools import py_to_iso_date, iso_to_py_date, pl_to_py_date
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from .models import Stay, Ship, Pier, Leave, Berth, Flag, Marina, Contract, Hub, Connector
from .miejsca import _gen_marina
from .flagi import _gen_flags

class PierCreate(CreateView):
    model = Pier
    fields = ['name']
    success_url = reverse_lazy('berths')


class PierUpdate(UpdateView):
    model = Pier
    fields = ['name']
    success_url = reverse_lazy('berths')


class PierDelete(DeleteView):
    model = Pier
    success_url = reverse_lazy('berths')


class BerthCreate(CreateView):
    model = Berth
    fields = ['name']
    success_url = reverse_lazy('berths')


class BerthUpdate(UpdateView):
    model = Berth
    fields = ['name']
    success_url = reverse_lazy('berths')


class BerthDelete(DeleteView):
    model = Berth
    success_url = reverse_lazy('berths')


def berths(request):
    _template = "berths.html"
    piers = []
    marina = Marina.objects.all()[0]

    if request.GET.get("gen_flags"):
        _gen_flags()

    if request.GET.get("gen_marina"):
        _gen_marina(marina)

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
                    _obj = Berth.objects.get(pk=_id)
                elif _type == 'hub':
                    _obj = Hub.objects.get(pk=_id)
                _obj.order = _order
                _obj.save()
            except:
                continue

    berth_id = request.POST.get('berth_id')
    if berth_id:
        # try:
        ship_name = request.POST.get('ship_name')
        ship_id = request.POST.get('ship_id')
        length = request.POST.get('length')
        flag_code = request.POST.get('flag')
        date_start = request.POST.get('date_start')
        date_end = request.POST.get('date_end')
        flag = Flag.objects.get(code=flag_code)
        if not ship_id:
            ship = Ship(name=ship_name, length=int(length), flag=flag)
            ship.save()
        else:
            ship = Ship.objects.get(pk=int(ship_id))
        berth = Berth.objects.get(pk=int(berth_id))
        stay = Stay(berth=berth, ship=ship, date_start=pl_to_py_date(date_start), date_end=pl_to_py_date(date_end))
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
        new_mooring = Berth(name=new_mooring_name, min_length=min_length, max_length=max_length, pier=new_mooring_pier)
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
        _moorings = []
        for mooring in Berth.objects.filter(pier=pier):
            mooring.type = "mooring"
            stays = Stay.objects.filter(berth=mooring)
            if stays:
                mooring.ship = stays[0].ship
            _moorings.append((mooring.order, mooring))
        for hub in Hub.objects.filter(pier=pier):
            hub.type = "hub"
            hub.connectors = Connector.objects.filter(hub=hub)
            for connector in hub.connectors:
                connector.counter = 4
            _moorings.append((hub.order, hub))
        piers.append([pier, map(lambda x: x[1], sorted(_moorings))])
        # column_size = max(2, int(12/(len(piers)+1)))

    ships = Ship.objects.all()

    context = {
        "title": unicode(marina),
        "piers": piers,
        # "column_size": column_size,
        "edit": True,
        "ships": ships,
    }
    return render(request, _template, context)

def map_demo(request):
    _template = "map.html"
    context = {}
    return render(request, _template, context)

def moorings_demo(request):
    _template = "moorings_static.html"
    context = {}
    return render(request, _template, context)