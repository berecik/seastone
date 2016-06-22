# -*- coding: utf-8 -*-
__author__ = 'beret'

from marina.models import Ship, Flag
from django.core.management.base import BaseCommand, CommandError

ships_examples = [
    {
        "name": 'Sofia',
        "length": '8.86',
        "flag": 'nl'
    },
    {
        "name": 'Titanic',
        "length": '268.99',
        "flag": 'gb'
    },
    {
        "name": 'Bismarck',
        "length": '251',
        "flag": 'de'
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
        ship_dict["flag"] = Flag.objects.get(code=ship_dict["flag"])
        ship, created = Ship.objects.get_or_create(**ship_dict)
        if created:
            ship.save()
            print ship
