# -*- coding: utf-8 -*-
__author__ = 'beret'
from marina.models import Pier, Berth, Hub, Connector, Marina
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create marina scheme'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        marina, created = Marina.objects.get_or_create(name="Marina Kamień Pomorski")
        if created:
            marina.save()
        _gen_marina(marina)
        self.stdout.write(self.style.SUCCESS('Successfully created marina %s scheme' % marina.name))

miejsca = [
    ['A', [
        False, True,
        53.9741927, 14.76704, 53.9737165, 14.7674627,
        [10, None],
        [1, None],
        [2, 6, 9]
    ]],
    ['B', [
        True, True,
        53.974448, 14.767642, 53.97391, 14.768145,
        [27, 28],
        [11, 44],
        [42, 38, 32, 28]
    ]],
    ['C', [
        True, True,
        53.9750375, 14.768005, 53.97411, 14.76886,
        [70, 71],
        [45, 96],
        [73, 76, 80, 84, 89, 92]
    ]],
    ['D', [
        True, True,
        53.975435, 14.76856, 53.97436, 14.769563,
        [127, 128],
        [97, 158],
        [154, 150, 146, 142, 138, 132, 128]
    ]],
    ['E', [
        True, True,
        53.974958, 14.770105, 53.974897, 14.771,
        [172, 173],
        [159, 186],
        [162, 166, 170]
    ]],
    ['F', [
        True, True,
        53.975321, 14.76981, 53.97523, 14.77107,
        [206, 207],
        [187, 226],
        [190, 194, 200, 206]
    ]],
    ['G', [
        True, False,
        53.975640, 14.769861, 53.975547, 14.771125,
        [246, None],
        [227, None],
        [230, 238, 244]
    ]]
]

def _del_all(cls):
    for o in cls.objects.all():
        o.delete()

def _gen_marina(marina):
    order = 0

    _del_all(Connector)
    _del_all(Hub)
    _del_all(Berth)
    _del_all(Pier)

    for pirs, details in miejsca:
        print "Pomost %s" % pirs

        left_site, right_site, loc_start_x, loc_start_y, loc_end_x, loc_end_y, starts, ends, hubs = details

        po = Pier(
            marina=marina,
            name="Pomost %s" % pirs,
            left_site=left_site,
            right_site=right_site,
            loc_start_x=loc_start_x,
            loc_start_y=loc_start_y,
            loc_end_x=loc_end_x,
            loc_end_y=loc_end_y,
            order=order)
        po.save()
        order +=1

        li, ri = starts
        le, re = ends
        hi = len(hubs)
        row = ""
        if li > le:
            row += "\t%s%s" % (pirs, li)
            bo = Berth(pier=po, name="%s%s" % (pirs, li), min_length=0, max_length=20, order=order)
            bo.save()
            order += 1
        if ri < re:
            row += "\t%s%s" % (pirs, ri)
            bo = Berth(pier=po, name="%s%s" % (pirs, ri), min_length=0, max_length=20, order=order)
            bo.save()
            order += 1
        print row
        if ri in hubs or li in hubs:
            print "\t\tPostument %s%s" % (pirs, hi)
            ho = Hub(pier=po, name="Postument %s%s" % (pirs, hi), order=order)
            ho.save()
            order += 1
            for i in range(1, 9):
                print "\t\t\t\t%s%sE%s" % (pirs, hi, i)
                co = Connector(hub=ho, name="%s%sE%s" % (pirs, hi, i))
                co.save()
            hi -= 1
        while li > le or ri < re:
            row = ""
            if li > le:
                li -= 1
                row += "\t%s%s" % (pirs, li)
                bo = Berth(pier=po, name="%s%s" % (pirs, li), min_length=0, max_length=20, order=order)
                bo.save()
                order += 1
            if ri < re:
                ri += 1
                row += "\t%s%s" % (pirs, ri)
                bo = Berth(pier=po, name="%s%s" % (pirs, ri), min_length=0, max_length=20, order=order)
                bo.save()
                order += 1
            print row
            if ri in hubs or li in hubs:
                print "\t\tPostument %s%s" % (pirs, hi)
                ho = Hub(pier=po, name="Postument %s%s" % (pirs, hi), order=order)
                ho.save()
                order += 1
                for i in range(1, 9):
                    print "\t\t\t\t%s%sE%s" % (pirs, hi, i)
                    co = Connector(hub=ho, name="%s%sE%s" % (pirs, hi, i))
                    co.save()
                hi -= 1