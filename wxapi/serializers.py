
from rest_framework import serializers

from wxapi.models import WeatherRecord, WeatherRecordAnalyzed


class WeatherRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherRecord
        fields = ['id', 'station', 'date', 'max_temp', 'min_temp', 'precip']


class WeatherRecordAnalyzedSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherRecordAnalyzed
        fields = ['id', 'station', 'year', 'max_temp_ave',
                  'max_temp_ave', 'min_temp_ave', 'precip_total']
