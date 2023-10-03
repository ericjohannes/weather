from django.db import models


class WeatherRecord(models.Model):
    """
    Model for the record of weather for one station on one date.
    """
    station = models.CharField(max_length=15, blank=False, default='')
    date = models.DateField()
    max_temp = models.SmallIntegerField()
    min_temp = models.SmallIntegerField()
    precip = models.SmallIntegerField()

    class Meta:
        ordering = ['station', 'date']  # order by station then by date
        constraints = [
            models.UniqueConstraint(
                fields=['station', 'date'],
                name='unique_date_station_combination'
            )
        ]


class WeatherRecordAnalyzed(models.Model):
    """
    Model for the aggregated weather data for one station for one year.
    """
    station = models.CharField(max_length=15, blank=False, default='')
    year = models.SmallIntegerField()
    max_temp_ave = models.DecimalField(  # in degrees C
        max_digits=4, decimal_places=1
    )
    min_temp_ave = models.DecimalField(  # in degrees C
        max_digits=4, decimal_places=1
    )
    precip_total = models.DecimalField(  # in centimeters
        max_digits=6, decimal_places=2
    )

    class Meta:
        ordering = ['station', 'year']  # order by station then by year

        constraints = [
            models.UniqueConstraint(
                fields=['station', 'year'],
                name='unique_year_station_combination'
            )
        ]
