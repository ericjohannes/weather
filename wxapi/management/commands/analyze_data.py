import datetime

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.db.models import Sum, Avg, Q

from wxapi.models import WeatherRecord, WeatherRecordAnalyzed


def clean_temp_record(tenths):
    """
    Temps in WeatherRecords model are stored as tenths of a degree Celsius.
    Convert to Celcius degrees. Rounding and accuracy enforced in db.
    """
    return tenths / 10.0


def clean_precip_record(tenths):
    """
    Precip in WeatherRecords model are stored as tenths of a millimeter.
    Convert to centimeters. Rounding and accuracy enforced in db.
    """
    return tenths / 100.0


class Command(BaseCommand):
    help = """Computes avearge high temperature, average low temperature
    and total precipitation for each weather station and year. Loads
    data into database."""

    created_objs = []
    records_ingested = 0

    def aggregate_by_year(self, station):
        """
        aggregate one station's data by year. Return list of objects.
        """
        return (
                WeatherRecord.objects
                .filter(station=station, )
                .values('station', 'date__year')
                .annotate(
                    max_temp_ave=clean_temp_record(
                        Avg('max_temp', filter=Q(max_temp__gt=-9999))
                    ),
                    min_temp_ave=clean_temp_record(
                        Avg('min_temp', filter=Q(min_temp__gt=-9999))
                    ),
                    precip_total=clean_precip_record(
                        Sum('precip', filter=Q(precip__gt=-9999))
                    )
                )
            )

    def handle_station(self, station):
        """
        Analyze and store one station's data
        """
        station_records = self.aggregate_by_year(station)

        for sr in station_records:
            try:
                created_obj = WeatherRecordAnalyzed.objects.create(
                    station=sr['station'],
                    year=sr['date__year'],
                    max_temp_ave=sr['max_temp_ave'],
                    min_temp_ave=sr['min_temp_ave'],
                    precip_total=sr['precip_total']
                )
                created_obj.save()
                self.records_ingested += 1

            except IntegrityError:
                self.stdout.write(
                    f"Already analyzed for {station}, {sr['date__year']}"
                )

    def handle(self, *args, **options):
        # gets list of distinct stations
        key = 'station'
        stations = WeatherRecord.objects.order_by().values_list(key).distinct()
        station_ids = [station[0] for station in stations]

        # crunch numbers for one station at a time. Doing all stations and all
        # years at once might be too much memory, but could be faster.
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_msg = f"Stated ingesting data at {start_time}"
        self.stdout.write(start_msg)

        for id in station_ids:
            self.handle_station(id)

        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        end_msg = f"Ended ingesting data at {end_time}\n"
        end_msg += f"{self.records_ingested} rows of analyzed data added"
        self.stdout.write(end_msg)
