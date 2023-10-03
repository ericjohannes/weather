from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from wxapi.models import WeatherRecord, WeatherRecordAnalyzed
from wxapi.serializers import (
    WeatherRecordSerializer,
    WeatherRecordAnalyzedSerializer
)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'weather-records': reverse(
            'weather-records-list',
            request=request, format=format
        ),
        'analyzed-weather-records': reverse(
            'weather-records-analyzed-list',
            request=request, format=format
        )
    })


class WeatherRecordList(generics.ListAPIView):
    """
    lists weather records, read only view.
    """
    serializer_class = WeatherRecordSerializer

    def get_queryset(self):
        queryset = WeatherRecord.objects.all()
        station = self.request.query_params.get('station')
        date = self.request.query_params.get('date')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        # allow for filtering on station id and date
        if station:
            queryset = queryset.filter(station=station)
        if date:
            queryset = queryset.filter(date=date)
        else:  # only use start and end date if date is not used
            if start_date:
                queryset = queryset.filter(date__gte=start_date)
            if end_date:
                queryset = queryset.filter(date__lte=end_date)

        return queryset


class WeatherRecordAnalyzedList(generics.ListAPIView):
    """
    lists analyzed weather data, read only view.
    """
    serializer_class = WeatherRecordAnalyzedSerializer

    def get_queryset(self):
        queryset = WeatherRecordAnalyzed.objects.all()
        station = self.request.query_params.get('station')
        year = self.request.query_params.get('year')

        # allow for filtering on station id and year
        if station:
            queryset = queryset.filter(station=station)
        if year:
            queryset = queryset.filter(year=year)
        return queryset
