# -*- coding: utf-8 -*-
import logging
from optparse import make_option
import os
import sqlite3

from django.core.management.base import BaseCommand, CommandError

from django.conf import settings
from data_app.models import Anon, Project, Info, Machine

logger = logging.getLogger("")


class Command(BaseCommand):

    def handle(self, *args, **options):
        Project.objects.all().delete()
        directory = settings.BASE_DIR + '/projects'
        for item in os.listdir(directory):
            project_dir = os.path.join(directory, item)
            logger.warning(project_dir)
            if os.path.isdir(project_dir):
                project, __created = Project.objects.get_or_create(name=item, path=project_dir)
                project.save()
                db_path = project_dir + '/db/dane2.db'
                con = sqlite3.connect(db_path, 180)

                cur = con.cursor()
                cur.execute("SELECT * FROM 'info'")
                fields = cur.description

                for row in cur.fetchall():
                    kwargs = {}
                    for i, field in enumerate(fields[1:], 1):
                        kwargs[field[0]] = row[i]
                    print("info: %s" % kwargs)
                    info = Info(project=project, **kwargs)
                    info.save()

                cur = con.cursor()
                cur.execute("SELECT * FROM 'anon'")
                fields = cur.description
                anons = []
                rows = cur.fetchall()
                for row in rows:
                    kwargs = {}
                    for i, field in enumerate(fields[1:], 1):
                        kwargs[field[0]] = row[i]
                    print("anon: %s" % kwargs.keys())
                    anon_id = row[0]
                    anon = Anon(project=project, **kwargs)
                    anon.save()
                    anons.append((anon_id, anon))
                for anon_id, anon in anons:
                    cur.execute("SELECT * FROM 'machine' where 'anon_id' = %s" % anon_id)
                    fields = cur.description
                    for row in cur.fetchall():
                        kwargs = {}
                        for i, field in enumerate(fields[2:], 2):
                            kwargs[field[0]] = row[i]
                        print("machine: %s" % kwargs.keys())
                        machine = Machine(anon=anon, **kwargs)
                        machine.save()
            con.close()
        return 0
