from __future__ import unicode_literals

from django.db import models

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
    double_site = models.BooleanField(default=True)

    def __unicode__(self):
        # return "%s %s" % (unicode(self.marina), self.name)
        return self.name

    class Meta:
        ordering = ['order', 'id']


class Berth(models.Model):
    pier = models.ForeignKey(Pier)
    name = models.CharField(max_length=1024, db_index=True)
    min_length = models.DecimalField(max_digits=6, decimal_places=2)
    max_length = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s %s" % (unicode(self.pier), self.name)

    class Meta:
        ordering = ['order', 'id']


class Hub(models.Model):
    pier = models.ForeignKey(Pier)
    name = models.CharField(max_length=1024, db_index=True)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s %s" % (unicode(self.pier), self.name)

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


class Stay(models.Model):
    berth = models.ForeignKey(Berth)
    ship = models.ForeignKey(Ship, null=True)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return "%s: %s %s-%s" % (unicode(self.berth), unicode(self.ship), unicode(self.date_start), unicode(self.date_end))


class Contract(models.Model):
    berth = models.ForeignKey(Berth)
    ship = models.ForeignKey(Ship)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (unicode(self.ship.name), unicode(self.berth.name))


class Leave(models.Model):
    contractor = models.ForeignKey(Contract)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    def __unicode__(self):
        return "%s: %s-%s" % (unicode(self.member), unicode(self.date_start), unicode(self.date_end))


class Connector(models.Model):
    hub = models.ForeignKey(Hub)
    name = models.CharField(max_length=1024, db_index=True)

    def __unicode__(self):
        return "%s %s" % (unicode(self.hub), self.name)


class Connection(models.Model):
    connector = models.ForeignKey(Connector)
    berth = models.ForeignKey(Berth)
    ship = models.ForeignKey(Ship)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField(null=True, blank=True)
    counter_start = models.IntegerField(default=0)
    counter_end = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (unicode(self.connector), unicode(self.berth))



