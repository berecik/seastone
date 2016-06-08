# -*- coding: utf-8 -*-
__author__ = 'beret'
from .models import Pier, Berth, Hub, Connector


miejsca = [
    ['A', [
        False,
        [10, None],
        [1, None],
        [2, 6, 9]
    ]],
    ['B', [
        True,
        [27, 28],
        [11, 44],
        [42, 38, 32, 28]
    ]],
    ['C', [
        True,
        [70, 71],
        [45, 96],
        [73, 76, 80, 84, 89, 92]
    ]],
    ['D', [
        True,
        [127, 128],
        [97, 158],
        [154, 150, 146, 142, 138, 132, 128]
    ]],
    ['E', [
        True,
        [172, 173],
        [159, 186],
        [162, 166, 170]
    ]],
    ['F', [
        True,
        [206, 207],
        [187, 226],
        [190, 194, 200, 206]
    ]],
    ['G', [
        False,
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

        site, starts, ends, hubs = details

        po = Pier(marina=marina, name="Pomost %s" % pirs, double_site=site, order=order)
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