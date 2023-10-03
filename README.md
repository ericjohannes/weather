This project ingests some weather, puts it into a database, and exposes the data through a REST API.

# Questions
Responses to the several questions for this exercise

## Problem 1 - Data Modeling

[Weather data model](weather/wxapi/models.py#L4) 

## Problem 2 - Ingestion

[Code to ingest weather data](weather/wxapi/management/commands/ingest_data.py) 

## Problem 3 - Data Analysis

[Code to analyze data](weather/wxapi/management/commands/analyze_data.py)

[Analyzed data model](weather/wxapi/models.py#L24)

## Problem 4 - REST API

I used Django and the Django REST API package for this portion. You can [see the api in action](myawsthing.com). The code for it mainly lives in the [views](weather/wxapi/views.py), [urls](weather/wxapi/urls.py), and [serializers](weather/wxapi/serializers.py) files.


## Extra Credit - Deployment

My app is [deployed on AWS](myawsthing.com).