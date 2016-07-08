#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'beret'

from marina.models import Ship, Flag
from django.core.management.base import BaseCommand, CommandError


ships_examples = [
    {
        "name": 'Dar Pomorza',
        "length": '81.5',
        "flag": 'pl'
    },
    {
        "name": 'Zawisza Czarny',
        "length": '42.7',
        "flag": 'pl'
    },
    {
        "name": 'Bismarck',
        "length": '251',
        "flag": 'de'
    },
    {
        "name": 'Vasa',
        "length": '61',
        "flag": 'se'
    },
    {
        "name": 'Draken Harald',
        "length": '35',
        "flag": 'no'
    },
    {
        "name": 'Sofia',
        "length": '8.86',
        "flag": 'nl'
    },
    {
        "name": 'Eifel',
        "length": '115',
        "flag": 'fr'
    },
    {
        "name": 'Hercules Poirot',
        "length": '12',
        "flag": 'be'
    },
    {
        "name": 'Lordi',
        "length": '666',
        "flag": 'fi'
    },
    {
        "name": 'Szwejk',
        "length": '19.14',
        "flag": 'cz'
    },
    {
        "name": 'Titanic',
        "length": '268.99',
        "flag": 'gb'
    },
    {
        "name": 'Enterprise',
        "length": '330',
        "flag": 'us'
    }
]

class Command(BaseCommand):
    help = 'Generate example ships'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        _gen_ships()
        self.stdout.write(self.style.SUCCESS('Successfully created example ships'))

def _gen_ships():

    for ship_dict in ships_examples:
        print ship_dict
        ship_dict["flag"] = Flag.objects.get(code=ship_dict["flag"])
        ship, created = Ship.objects.get_or_create(**ship_dict)
        if created:
            ship.save()
            print ship
