#!/bin/sh

echo "drop database seastone; create database seastone;" | psql
./manage.py migrate
./manage.py createsuperuser --username beret --email beret@hipisi.org.pl
./manage.py flags
./manage.py example_places
./manage.py example_ships
