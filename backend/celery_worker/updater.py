from datetime import datetime
import logging
from django.conf import settings

from stops.models import Stop
from stops.serializer import ExportStopSerializer
from agencies.models import Agency
from agencies.serializer import ExportAgencySerializer
from routes.models import Route
from routes.serializer import ExportRouteSerializer
from trips.models import Trip
from trips.serializer import ExportTripSerializer
from stop_times.models import StopTime
from stop_times.serializer import ExportStopTimeSerializer
from calendars.models import Calendar
from calendars.serializer import ExportCalendarSerializer
from calendar_dates.models import CalendarDate
from calendar_dates.serializer import ExportCalendarDateSerializer
from fares.models import Fare
from fares.serializer import ExportFareSerializer
from transfers.models import Transfer
from transfers.serializer import ExportTransferSerializer

import os
import shutil
import csv
from django.db import models

SERIALIZABLE_TABLES = [
    [Agency, ExportAgencySerializer, 'agency.txt'],
    [Stop, ExportStopSerializer, 'stops.txt'],
    [Route, ExportRouteSerializer, 'routes.txt'],
    [Trip, ExportTripSerializer, 'trips.txt'],
    [StopTime, ExportStopTimeSerializer, 'stop_times.txt'],
    [Calendar, ExportCalendarSerializer, 'calendar.txt'],
    [CalendarDate, ExportCalendarDateSerializer, 'calendar_dates.txt'],
    [Fare, ExportFareSerializer, 'fare_rules.txt'],
    [Transfer, ExportTransferSerializer, 'transfers.txt'],
]
TEMP_DIR_NAME = settings.TEMP_DIR_NAME
BASE_DIR = settings.BASE_DIR

logger = logging.getLogger()

def get_connection():
    import psycopg2
    logger.warn(settings.DATABASES)
    conn = psycopg2.connect(
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT'],
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD']
    )

def start_serializing():
    get_connection()
    path = os.path.join(BASE_DIR, TEMP_DIR_NAME)
    if not os.path.exists(path):
        os.mkdir(os.path.join(BASE_DIR, TEMP_DIR_NAME))
    logger.info("Starting serializing at:" + datetime.now().strftime("%H:%M:%S"))
    for model, serializer, filename in SERIALIZABLE_TABLES:
        write_to_file(model, serializer, filename)
    logger.info("Finished serializing at:" + datetime.now().strftime("%H:%M:%S"))
    logger.info("Zipping all gtfs files")
    shutil.make_archive(os.path.join(BASE_DIR, 'gtfs'), 'zip', os.path.join(BASE_DIR, TEMP_DIR_NAME))

def write_to_file(Model, Serializer, filename):
    logger.info("Starting to seralize " + filename)
    items = Model.objects.all()
    serializer = Serializer(items, many=True)
    header = [field_name for field_name in Serializer.Meta.fields]
    data = serializer.data
    with open(os.path.join(BASE_DIR, TEMP_DIR_NAME, filename), 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(data)
    logger.info("Finished writing " + filename)

