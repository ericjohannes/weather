This project ingests some weather, puts it into a database, and exposes the data through a REST API.

Note, while exploring AWS deployment options I deleted and recreated the github repo so the commit history here does not reflect my commit process when building this app.

The data is all in the `wx_data` folder. To load the data base run `python manage.py ingest_data` and `python manage.py analyze_data`. After that run `python manage.py runserver` and check out the api at  http://127.0.0.1:8000/api/weather and http://127.0.0.1:8000/api/weather/stats.

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

I used Django and the Django REST API package for this portion. The code for it mainly lives in the [views](weather/wxapi/views.py), [urls](weather/wxapi/urls.py), and [serializers](weather/wxapi/serializers.py) files. It will return html if you visit the api with a broswer but returns json if you go to http://127.0.0.1:8000/api/weather.json or http://127.0.0.1:8000/api/weather/stats.json


A swagger endpoint is at http://127.0.0.1:8000/api/swagger-ui/ 

## Extra Credit - Deployment

What tools and AWS services would you use to deploy the API, database, and a scheduled version of your data ingestion code?

Steps to deploy app:
1. Create requirements.txt file from virtual environment
2. Change allow host settings of django app for AWS
3. Create apprunner.yaml file to configure deployment
4. Create a startup shell bash file
5. Create git repo and push to github
6. create and deploy apprunner service that follows main branch on github repo 
6. create a postgres database on Amazon RDS, create a database in the database, configure a user to use
7. Add databse secrets to AWS secret manager, create a role with access to those secrets, give the apprunner service that secruity role. Add secrets in apprunner yaml
8. Add section in settings.py to look for postgres secrets in environment and if they're there make a postgres connection
9. Push to git and have apprunner automatically redeploy

Steps to ingest data on a schdule:
1. move data files to s3 bucket 
2. change ingest and analyze processes to read from s3 bucket
3. move those processes to lambdas and set up a trigger on a schedule or when a new file drops on s3 bucket  