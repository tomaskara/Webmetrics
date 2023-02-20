import smtplib, ssl
import os
import json
import requests
import datetime
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from django.conf import settings
import django
django.setup()
from speedcheck.models import Urls, CruxHistory

BASE_DIR = settings.BASE_DIR
#project_folder = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

def get_all_urls_data():
    for url in Urls.objects.all():
        get_api_data(url.url)
    return

def get_api_data(url):
    api_url = f"https://chromeuxreport.googleapis.com/v1/records:queryRecord?key={os.getenv('API_KEY')}"
    shortcuts = { "largest_contentful_paint":"lcp",
                  "first_input_delay":"fid",
                  "cumulative_layout_shift":"cls",
                  "first_contentful_paint":"fcp",
                  "experimental_time_to_first_byte":"ttfb",
                  "experimental_interaction_to_next_paint":"inp"}
    for device in ["PHONE", "DESKTOP"]:
        request_body = {

              "url": url,
              "formFactor": device,
              "metrics": [
                  "largest_contentful_paint",
                  "first_input_delay",
                  "cumulative_layout_shift",
                  "first_contentful_paint",
                  "experimental_time_to_first_byte",
                  "experimental_interaction_to_next_paint"
              ]
        }

        api_call = requests.post(api_url, json=request_body)
        if api_call.status_code == 404:
            continue
        json_response = api_call.json()
        date = datetime.date(json_response['record']['collectionPeriod']['lastDate']['year'],
                             json_response['record']['collectionPeriod']['lastDate']['month'],
                             json_response['record']['collectionPeriod']['lastDate']['day'])

        if device == "PHONE":
            if not CruxHistory.objects.filter(url__url=url,date=date).exists():
                new_values = {"url": Urls.objects.get(url=url),
                              "date": date}
                for name, value in json_response['record']['metrics'].items():
                    new_values[f"{shortcuts[name]}m"] = float(value['percentiles']['p75'])
                CruxHistory.objects.create(**new_values)
        elif device == "DESKTOP":
            if CruxHistory.objects.filter(url__url=url, date=date, clsd__isnull=True).exists():
                new_values = {}
                for name, value in json_response['record']['metrics'].items():
                    new_values[f"{shortcuts[name]}d"] = float(value['percentiles']['p75'])
                object_to_update = CruxHistory.objects.filter(url__url=url,date=date)
                object_to_update.update(**new_values)

