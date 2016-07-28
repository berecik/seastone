from __future__ import unicode_literals
from datetime import date

from django.db import models
from django.db.models import Q

# Create your models here.
# no problem dude, so let do a bert place model first


class Marina(models.Model):
    name = models.CharField(max_length=1024, db_index=True)

    def __unicode__(self):
        return self.name


class Pier(models.Model):
    marina = models.ForeignKey(Marina)
    name = models.CharField(max_length=1024, db_index=True)
    order = models.IntegerField(default=0)
    # double_site = models.BooleanField(default=True)
    left_site = models.BooleanField(default=True)
    right_site = models.BooleanField(default=True)
    loc_start_x = models.FloatField()
    loc_start_y = models.FloatField()
    loc_end_x = models.FloatField()
    loc_end_y = models.FloatField()


    def __unicode__(self):
        # return "%s %s" % (unicode(self.marina), self.name)
        return self.name

    class Meta:
        ordering = ['order', 'id']


class Place(models.Model):
    pier = models.ForeignKey(Pier)
    name = models.CharField(max_length=1024, db_index=True)
    min_length = models.DecimalField(max_digits=6, decimal_places=2)
    max_length = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.IntegerField(default=0)
    # loc = models.TextField()

    def state(self, date_start, date_end):

        stays = Stay.objects.filter(place=self).filter(date_start__lte=date_end, date_end__gte=date_start)
        contracts = Contract.objects.filter(place=self, date_start__lte=date_end)\
            .filter(Q(date_end__gte=date_start) | Q(date_end__isnull=True))
        leaves = Leave.objects.filter(contractor__place=self, date_start__lte=date_end, date_end__gte=date_start)

        if contracts and not leaves:
            return "resident"
        elif not stays:
            return "free"
        else:
            return "booked"

    def ships(self, date_start, date_end):
        ships = []

        stays = Stay.objects.filter(place=self, date_start__lte=date_end, date_end__gte=date_start)

        if stays:
            for stay in stays:
                ships.append(stay)
        return ships

    def resident(self, date_start, date_end):
        residents = []

        contracts = Contract.objects.filter(place=self, date_start__lte=date_end)\
            .filter(Q(date_end__gte=date_start) | Q(date_end__isnull=True))

        if contracts:
            for contract in contracts:
                leaves = Leave.objects.filter(contractor=contract, date_end__gte=date_start)
                leaves_list = []
                for leave in leaves:
                    leaves_list.append(leave)
                residents.append([contract, leaves])

        return residents

    def __unicode__(self):
        return "%s %s" % (unicode(self.pier), self.name)

    class Meta:
        ordering = ['order', 'id']


class Hub(models.Model):
    pier = models.ForeignKey(Pier)
    name = models.CharField(max_length=1024, db_index=True)
    order = models.IntegerField(default=0)
    # loc_x = models.FloatField()
    # loc_y = models.FloatField()

    def __unicode__(self):
        return "%s %s" % (unicode(self.pier), self.name)

    class Meta:
        ordering = ['order', 'id']


class YBom(models.Model):
    pier = models.ForeignKey(Pier)
    left = models.BooleanField()
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s %s" % (unicode(self.pier), self.order)

    class Meta:
        ordering = ['order', 'id']


class Flag(models.Model):
    name = models.CharField(max_length=1024, db_index=True)
    code = models.CharField(max_length=6, db_index=True)

    def __unicode__(self):
        return self.code


class Ship(models.Model):

    name = models.CharField(max_length=1024, db_index=True)
    flag = models.ForeignKey(Flag)
    length = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return "%s (%s) %sm" % (self.name, unicode(self.flag), unicode(self.length))


class Occupation(models.Model):
    place = models.ForeignKey(Place)
    ship = models.ForeignKey(Ship)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    contact_name = models.CharField(max_length=1024, db_index=True, null=True, blank=True)
    contact_phone = models.CharField(max_length=64, db_index=True, null=True, blank=True)
    contact_email = models.CharField(max_length=64, db_index=True, null=True, blank=True)
    notices = models.TextField(default="")

    class Meta:
        abstract = True


class Stay(Occupation):

    @property
    def current_connector(self):
        connection = Connection.objects.filter(stay=self)
        if connection:
            connector = connection[0].connector
            return connector
        return None

    def __unicode__(self):
        return "%s: %s %s-%s" % (unicode(self.place), unicode(self.ship), unicode(self.date_start), unicode(self.date_end))


class Contract(Occupation):

    @property
    def current_connector(self):
        connection = Connection.objects.filter(contract=self)
        if connection:
            connector = connection[0].connector
            return connector
        return None

    def __unicode__(self):
        return "%s %s" % (unicode(self.ship.name), unicode(self.place.name))


class Leave(models.Model):
    contractor = models.ForeignKey(Contract)
    date_start = models.DateField()
    date_end = models.DateField()

    def __unicode__(self):
        return "%s: %s-%s" % (unicode(self.member), unicode(self.date_start), unicode(self.date_end))


class Connector(models.Model):
    hub = models.ForeignKey(Hub)
    name = models.CharField(max_length=1024, db_index=True)

    @property
    def last_connection(self):
        conection = Connection.objects.filter(connector=self).last()
        return conection

    @property
    def counter(self):
        if self.last_connection:
            if self.last_connection.counter_end:
                return self.last_connection.counter_end
            else:
                if self.last_connection.counter_start:
                    return self.last_connection.counter_start
        return 0

    @property
    def conected(self):
        if self.last_connection:
            if self.last_connection.counter_end:
                return False
            else:
                return True
        else:
            return False

    @property
    def current_occupation(self):
        if self.conected:
            if self.last_connection.stay:
                return self.last_connection.stay
            if self.last_connection.contract:
                return self.last_connection.contract
        return None

    @property
    def current_ship(self):
        if self.current_occupation:
            return self.current_occupation.ship
        return None

    @property
    def current_place(self):
        if self.current_occupation:
            return self.current_occupation.place
        return None

    def set_stay(self, stay, counter):
        connection = Connection(
            connector=self,
            stay=stay,
            contract=None,
            date_start=date.today(),
            date_end=None,
            counter_start=counter,
            counter_end=None
        )
        connection.save()

    def set_contract(self, contract, counter):
        connection = Connection(
            connector=self,
            stay=None,
            contract=contract,
            date_start=date.today(),
            date_end=None,
            counter_start=counter,
            counter_end=None
        )
        connection.save()

    def close_connection(self, counter):
        last_connection = self.last_connection
        last_connection.counter_end = counter
        last_connection.date_end = date.today()
        last_connection.save()

    def set_counter(self, counter):
        last_connection = self.last_connection
        if last_connection and last_connection.date_end:
            new_connection = Connection(
                connector=self,
                stay=None,
                contract=None,
                date_start=last_connection.date_end,
                date_end=date.today(),
                counter_start=last_connection.counter_end,
                counter_end=counter
            )
            new_connection.save()
        else:
            new_connection = Connection(
                connector=self,
                stay=last_connection.stay if last_connection else None,
                contract=last_connection.contract if last_connection else None,
                date_start=date.today(),
                date_end=None if last_connection else date.today(),
                counter_start=counter if last_connection else 0,
                counter_end=None if last_connection else counter
            )
            new_connection.save()
            if last_connection:
                last_connection.date_end = date.today()
                last_connection.counter_end = counter
                last_connection.save()
        return new_connection

    def __unicode__(self):
        return "%s %s" % (unicode(self.hub), self.name)


class Connection(models.Model):
    connector = models.ForeignKey(Connector)
    stay = models.ForeignKey(Stay, null=True)
    contract = models.ForeignKey(Contract, null=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField(null=True, blank=True)
    counter_start = models.IntegerField(default=0)
    counter_end = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (unicode(self.connector), unicode(self.place))

    class Meta:
        ordering = ['counter_start', '-counter_end']



