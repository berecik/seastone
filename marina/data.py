# -*- coding: utf-8 -*-
from .models import Place, Pier, Ship


def get_places(date_start, date_end, boat_size, marina, **kwargs):
    places_dict = {}
    for pier in Pier.objects.filter(marina=marina):
        places = Place.objects.filter(pier=pier)
        if boat_size:
            places = places.filter(min_length__lte=boat_size, max_length__gte=boat_size)
        for place in places:
            state = place.state(date_start, date_end)
            if state not in places_dict:
                places_dict[state] = []
            places_dict[state].append(place.pk)
    return places_dict


def get_ships(**kwargs):
    ships = []
    ships_obj = Ship.objects.all()
    for ship in ships_obj:
        ship_dict = {
            "value": ship.id,
            "label": unicode(ship),
            "name": ship.name,
            "length": float(ship.length),
            "flag": ship.flag.code
        }
        ships.append(ship_dict)
    return ships