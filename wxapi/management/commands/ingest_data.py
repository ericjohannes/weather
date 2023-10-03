import os
import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.utils import IntegrityError
import csv

from wxapi.models import WeatherRecord

DATA_DIR = 'wx_data'


def get_station(file_name):
    """
    turns file name of form '<station code>.txt' into station name.
    """
    return file_name.split('.')[0]


class Command(BaseCommand):
    help = "Ingests data from a set of files."
    records_ingested = 0
    data_dir = os.path.join(settings.BASE_DIR, DATA_DIR)

    def handle_records_individually(self, record_list):
        """
        add one weather record at a time the database when bulk create fails.
        """
        for r in record_list:
            try:
                r.save()
                self.records_ingested += 1
            except IntegrityError:
                continue

    def handle_file(self, f, station):
        """
        Read all records from one file and save it to the db.
        """
        created_objs = []
        csv_reader = csv.reader(f, delimiter='\t')
        wx_record_list = []
        for row in csv_reader:
            wx_record_list.append(
                WeatherRecord(
                    station=station,
                    date=row[0],
                    max_temp=row[1],
                    min_temp=row[2],
                    precip=row[3],
                )
            )
        try:
            created_objs = WeatherRecord.objects.bulk_create(wx_record_list)

        except IntegrityError:
            try:
                self.stdout.write(f"Already ingested some data for {station}")
                self.handle_records_individually(wx_record_list)
            except AttributeError:
                pass
        self.records_ingested += len(created_objs)

    def handle(self, *args, **options):
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_msg = f"Stated ingesting data at {start_time}"
        self.stdout.write(start_msg)
        files = os.listdir(self.data_dir)
        for file in files:
            path = os.path.join(self.data_dir, file)
            station = get_station(file)
            with open(path) as f:
                self.handle_file(f, station)

        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        end_msg = f"Ended ingesting data at {end_time}"
        end_msg += f"\n{self.records_ingested} records added"
        self.stdout.write(end_msg)
