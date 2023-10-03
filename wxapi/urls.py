from django.urls import path
from django.views.generic import TemplateView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view

from wxapi import views

app_name = "wxapi"

urlpatterns = [
        path('api/', views.api_root),
        path(
            'api/weather/',
            views.WeatherRecordList.as_view(),
            name='weather-records-list'
        ),
        path(
            'api/weather/stats/',
            views.WeatherRecordAnalyzedList.as_view(),
            name='weather-records-analyzed-list'
        ),
        path('api/openapi/', get_schema_view(
            title="Weather records",
            description="API for records of weather data.",
            version="1.0.0"
        ), name='openapi-schema'),
        # Route TemplateView to serve Swagger UI template.
        #   * Provide `extra_context` with view name of `SchemaView`.
        path('api/swagger-ui/', TemplateView.as_view(
            template_name='swagger-ui.html',
            extra_context={'schema_url': 'openapi-schema'}
        ), name='swagger-ui'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
