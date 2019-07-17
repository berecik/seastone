#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'beret'
from marina.models import Pier, Place, Hub, Connector, Marina, YBom
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create marina scheme'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        marina, created = Marina.objects.get_or_create(name=u"Marina Kamień Pomorski")
        if created:
            marina.save()
        _gen_marina(marina)
        self.stdout.write(self.style.SUCCESS(u'Successfully created marina %s scheme' % marina.name))

miejsca = [
    ['A', [
        False, True, False, False,
        53.9741927, 14.76704, 53.9737165, 14.7674627,
        [10, None],
        [1, None],
        [2, 6, 9]
    ]],
    ['B', [
        True, True, True, False,
        53.974448, 14.767642, 53.97391, 14.768145,
        [27, 28],
        [11, 44],
        [43, 39, 33, 29]
    ]],
    ['C', [
        True, True, True, [66, 75],
        53.9750375, 14.768005, 53.97411, 14.76886,
        [70, 71],
        [45, 96],
        [74, 77, 81, 85, 89, 93]
    ]],
    ['D', [
        True, True, True, False,
        53.975435, 14.76856, 53.97436, 14.769563,
        [127, 128],
        [97, 158],
        [155, 151, 147, 143, 139, 133, 129]
    ]],
    ['E', [
        True, True, True, False,
        53.974958, 14.770105, 53.974897, 14.771,
        [172, 173],
        [159, 186],
        [161, 165, 169]
    ]],
    ['F', [
        True, True, True, False,
        53.975321, 14.76981, 53.97523, 14.77107,
        [206, 207],
        [187, 226],
        [189, 193, 199, 205]
    ]],
    ['G', [
        True, False, True, False,
        53.975640, 14.769861, 53.975547, 14.771125,
        [246, None],
        [227, None],
        [229, 237, 243]
    ]]
]

length = (
    (1, 1),
    (11, 2),
    (21, 3),
    (35, 2),
    (45, 2),
    (55, 3),
    (61, 4),
    (63, 5),
    (66, 1),
    (76, 5),
    (79, 4),
    (81, 3),
    (87, 2),
    (97, 2),
    (119, 4),
    (123, 5),
    (133, 4),
    (137, 2),
    (999,0)
)

sizes = (
    (0, 12),
    (10, 16),
    (0, 8),
    (7, 9),
    (8, 10),
    (10, 14),
)

def _del_all(cls):
    for o in cls.objects.all():
        o.delete()

def _gen_marina(marina):
    order = 0

    _del_all(Connector)
    _del_all(Hub)
    _del_all(Place)
    _del_all(Pier)
    _del_all(YBom)

    places_dict = {}

    for pirs, details in miejsca:
        print "Pomost %s" % pirs

        left_site, right_site, is_ybom, ybom_start,loc_start_x, loc_start_y, loc_end_x, loc_end_y, starts, ends, hubs = details

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
        _bom_r = 1
        _bom_l = 1
        row = ""
        _yb_row = False
        if is_ybom and li > le and not ybom_start:
            yb = YBom(pier=po, order=order, left=True)
            yb.save()
            row += "\t<<<<<<<"
            order += 1
            _yb_row = True
        if is_ybom and ri < re and not ybom_start:
            yb = YBom(pier=po, order=order, left=False)
            yb.save()
            order += 1
            row += "\t>>>>>>>"
            _yb_row = True

        if _yb_row:
            row += "\n"

        if li > le:
            row += "\t%s%s" % (pirs, li)
            bo = Place(pier=po, name="%s%s" % (pirs, li), min_length=0, max_length=20, order=order)
            bo.save()
            places_dict[li] = bo
            order += 1
        if ri < re:
            row += "\t%s%s" % (pirs, ri)
            bo = Place(pier=po, name="%s%s" % (pirs, ri), min_length=0, max_length=20, order=order)
            bo.save()
            places_dict[ri] = bo
            order += 1
        print row
        if ri in hubs or li in hubs:
            print "\t\tPostument %s%s" % (pirs, hi)
            ho = Hub(pier=po, name="Postument %s%s" % (pirs, hi), order=order)
            ho.save()
            order += 1
            for i in range(1, 9):
                print "\t\t\t\t%s%sE%s" % (pirs, hi, i)
                co = Connector(hub=ho, name="%s" % i)
                co.save()
            hi -= 1
        while li > le or ri < re:
            row = ""
            _yb_row = False
            if ybom_start:
                if ybom_start[0] < li:
                    _bom_l = 1
                elif ybom_start[0] == li:
                    _bom_l = 0

                if ybom_start[1] > ri:
                    _bom_r = 1
                elif ybom_start[1] == ri:
                    _bom_r = 0
                # print ybom_start[0], li, _bom_l
                # print ybom_start[1], ri, _bom_r
            if is_ybom and not _bom_l and li > le:
                yb = YBom(pier=po, order=order, left=True)
                yb.save()
                order += 1
                _bom_l = 2
                row += "\t<<<<<<<"
                _yb_row = True

            if is_ybom and not _bom_r and ri < re:
                yb = YBom(pier=po, order=order, left=False)
                yb.save()
                order += 1
                _bom_r = 2
                row += "\t>>>>>>>"
                _yb_row = True

            if _yb_row:
                row += "\n"

            if li > le:
                li -= 1
                row += "\t%s%s" % (pirs, li)
                bo = Place(pier=po, name="%s%s" % (pirs, li), min_length=0, max_length=20, order=order)
                bo.save()
                places_dict[li] = bo
                order += 1
                _bom_l -= 1
            if ri < re:
                ri += 1
                row += "\t%s%s" % (pirs, ri)
                bo = Place(pier=po, name="%s%s" % (pirs, ri), min_length=0, max_length=20, order=order)
                bo.save()
                places_dict[ri] = bo
                order += 1
                _bom_r -= 1
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
    li = 0
    nl = 1
    for i in xrange(1,247):
        if i == nl:
            size = sizes[length[li][1]]
            nl = length[li+1][0]
            li += 1
        bo = places_dict[i]

        bo.min_length, bo.max_length = size
        bo.save()