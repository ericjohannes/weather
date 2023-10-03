import csv
import os

from django.test import TestCase
from django.conf import settings
from django.urls import reverse

from .models import WeatherRecord
from .management.commands.analyze_data import (
    clean_temp_record,
    clean_precip_record
)
from .management.commands.ingest_data import get_station
from .management.commands import ingest_data, analyze_data

TEST_RECORDS = [
    {'station': 'USC00110072', 'date': '20140801',
        'max_temp': 278, 'min_temp': 161, 'precip': 224},
    {'station': 'USC00110072', 'date': '20140802',
        'max_temp': 283, 'min_temp': 139, 'precip': 8},
    {'station': 'USC00110072', 'date': '20140803',
        'max_temp': 289, 'min_temp': 144, 'precip': 0},
]


class ApiTest(TestCase):
    """
    test the api serves correct data.
    """

    def test_api_up(self):
        """
        Test whether api code returns a 200
        """
        api_url = reverse('wxapi:weather-records-list')
        response_status = self.client.get(api_url).status_code
        self.assertEqual(response_status, 200)

    def test_insert_record_and_serve_it(self):
        """
        Inserts one record into db and tests that the api app serves it.
        """
        wx_obj = WeatherRecord.objects.create(
            station=TEST_RECORDS[0]['station'],
            date=TEST_RECORDS[0]['date'],
            max_temp=TEST_RECORDS[0]['max_temp'],
            min_temp=TEST_RECORDS[0]['min_temp'],
            precip=TEST_RECORDS[0]['precip'],
        )
        wx_obj.save()

        api_url = reverse('wxapi:weather-records-list')
        response = self.client.get(api_url)

        with self.subTest():
            self.assertContains(response, TEST_RECORDS[0]['max_temp'])
        with self.subTest():
            self.assertContains(response, TEST_RECORDS[0]['min_temp'])
        with self.subTest():
            self.assertContains(response, TEST_RECORDS[0]['precip'])
    # todo test analyzed data api similarly

    def test_query_for_data(self):
        """
        Tests that the query parameters work as expected.
        """
        # load db
        for r in TEST_RECORDS:
            wx_obj = WeatherRecord.objects.create(
                station=r['station'],
                date=r['date'],
                max_temp=r['max_temp'],
                min_temp=r['min_temp'],
                precip=r['precip'],
            )
            wx_obj.save()

        test_params = {'date': '2014-08-01', 'station': 'USC00110072'}
        api_url = reverse('wxapi:weather-records-list')
        results = self.client.get(api_url, test_params).json()['results'][0]
        assert_bool = test_params['date'] == results['date'] and\
            test_params['station'] == results['station']
        self.assertEqual(assert_bool, True)


class IngestDataTests(TestCase):
    DATA_DIR = 'wx_data'
    data_dir = os.path.join(settings.BASE_DIR, DATA_DIR)

    file = 'USC00110072.txt'
    station = 'USC00110072'

    def test_get_station(self):
        """
        tests function that parses a station id from a file name.
        """
        station = get_station(self.file)
        self.assertEqual(station, self.station)

    def test_ingesting_file(self):
        """
        tests whether one file is ingested as expected.
        """
        path = os.path.join(self.data_dir, self.file)
        station = get_station(self.file)

        with open(path) as f:
            ingest_data.Command.handle_file(ingest_data.Command, f, station)

        with open(path) as f:  # count lines in file
            csv_reader = csv.reader(f, delimiter='\t')
            row_count = sum(1 for row in csv_reader)

        # test whether the ingester ingested all rows from a file
        with self.subTest():
            self.assertEqual(row_count, ingest_data.Command.records_ingested)

        # spot check one record
        # 19850121	  -44	 -200	    0
        test_obj = WeatherRecord.objects.filter(
            date='19850121', station='USC00110072')[0]
        with self.subTest():
            self.assertEqual(test_obj.max_temp, -44)
        with self.subTest():
            self.assertEqual(test_obj.min_temp, -200)
        with self.subTest():
            self.assertEqual(test_obj.precip, 0)

        # add more records from same file and ensure the number doesn't change
        with open(path) as f:
            ingest_data.Command.handle_file(ingest_data.Command, f, station)

        with self.subTest():
            self.assertEqual(row_count, ingest_data.Command.records_ingested)
        # TODO:
        # test adding records individually if bulk create fails
        #


class AnalyzeDataTests(TestCase):
    def test_clean_temp_record(self):
        """
        tests whether clean_temp_record converts from a temp in 10ths
        of a degree C to degrees C.
        """
        raw = 115
        converted = 11.5
        cleaned = clean_temp_record(raw)
        self.assertEqual(cleaned, converted)

    def test_clean_precip_record(self):
        """
        tests whether clean_precip_record converts number from 10ths of
        millimeters to centimeters.
        """

        # 12345 == 5 10ths mm, 4 mm, 3 cm, 2 decimeters, 1 m
        raw = 12345  # 1 meter, 10 cm, 1 mm and 1/10th of a mm
        converted = 123.45  # 11 cm, 1 mm and 1 10th of a mm
        cleaned = clean_precip_record(raw)
        self.assertEqual(cleaned, converted)

    def test_aggregate_by_year(self):
        """
        tests whether analyzing data function produces correct results.
        """
        simple_aggregated_data = {
            'max_temp_ave': 0,
            'min_temp_ave': 0,
            'precip_total': 0,
        }

        for r in TEST_RECORDS:
            simple_aggregated_data['max_temp_ave'] += r['max_temp']
            simple_aggregated_data['min_temp_ave'] += r['min_temp']
            simple_aggregated_data['precip_total'] += r['precip']

            WeatherRecord.objects.create(
                station=r['station'],
                date=r['date'],
                max_temp=r['max_temp'],
                min_temp=r['min_temp'],
                precip=r['precip'],
            )

        # calculate averages wtih db method
        station_records = analyze_data.Command.aggregate_by_year(
            analyze_data.Command,
            TEST_RECORDS[0]['station']
        )
        aggregated_data = station_records.filter(
            station='USC00110072', date__year='2014')[0]

        # calculate averages using simple math
        simple_aggregated_data['max_temp_ave'] = clean_temp_record(
            simple_aggregated_data['max_temp_ave'] / 3)
        simple_aggregated_data['min_temp_ave'] = clean_temp_record(
            simple_aggregated_data['min_temp_ave'] / 3)
        simple_aggregated_data['precip_total'] = clean_precip_record(
            simple_aggregated_data['precip_total'])

        # test all data points
        with self.subTest():
            self.assertEqual(
                aggregated_data['max_temp_ave'],
                simple_aggregated_data['max_temp_ave']
            )
        with self.subTest():
            self.assertEqual(
                aggregated_data['min_temp_ave'],
                simple_aggregated_data['min_temp_ave']
            )
        with self.subTest():
            self.assertEqual(
                aggregated_data['precip_total'],
                simple_aggregated_data['precip_total']
            )
