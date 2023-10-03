This project ingests some weather, puts it into a database, and exposes the data through a REST API.

Note, in the process of deploying to AWS I deleted and recreated the github repo so the commit history here does not reflect my commit process when building this app.

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

Steps to deploy to AWS Apprunner
1. Created requirements.txt file
2. Change settings of django app for AWS
3. Create apprunner.yaml file to configure deployment
4. Create a startup shell bash file
5. Create git repo and push to github
6. create and deploy apprunner service
7. create a postgres database on Amazon RDS

Next steps:
1. save data files to s3 bucket
2. have ingest and analyze processes read from s3 bucket
3. move those processes to lambdas and have them trigger when a new file drops on s3 bucket

My app is [deployed on AWS](myawsthing.com).
