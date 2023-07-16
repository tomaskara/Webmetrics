import smtplib
import ssl
import os
import hashlib
import requests
import datetime
from statistics import mean
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from speedcheck.models import Urls, CruxHistory, ProfileUrl, CruxWeeklyHistory
from dashboard.functions import create_plot

BASE_DIR = settings.BASE_DIR
load_dotenv(os.path.join(BASE_DIR, ".env"))

shortcuts = {
    "largest_contentful_paint": "lcp",
    "first_input_delay": "fid",
    "cumulative_layout_shift": "cls",
    "first_contentful_paint": "fcp",
    "experimental_time_to_first_byte": "ttfb",
    "interaction_to_next_paint": "inp",
}


def get_all_urls_data():
    for url in Urls.objects.all():
        get_api_data(url.url)
    return


def get_api_data(url):
    """Retrieves the latest data from the CrUX API, saves it to the database
    (if data is new), and triggers other function to send email alerts if needed.

    Args:
        url (str): url address for which we want to download data

    Returns:
        This function has no return value.
    """
    api_url = f"https://chromeuxreport.googleapis.com/v1/records:queryRecord?key={os.getenv('API_KEY')}"
    for device in ["PHONE", "DESKTOP"]:
        request_body = {
            "url": url,
            "formFactor": device,
            "metrics": list(shortcuts.keys()),
        }

        api_call = requests.post(api_url, json=request_body)
        if api_call.status_code == 404:
            continue
        json_response = api_call.json()
        date = datetime.date(
            json_response["record"]["collectionPeriod"]["lastDate"]["year"],
            json_response["record"]["collectionPeriod"]["lastDate"]["month"],
            json_response["record"]["collectionPeriod"]["lastDate"]["day"],
        )

        if device == "PHONE":
            # check if combination url and date exists in db, if not: create new record with values for mobile
            if not CruxHistory.objects.filter(url__url=url, date=date).exists():
                new_values = {"url": Urls.objects.get(url=url), "date": date}
                # create dictionary of new values from API
                for name, value in json_response["record"]["metrics"].items():
                    new_values[f"{shortcuts[name]}m"] = float(
                        value["percentiles"]["p75"]
                    )
                # save new values to database
                CruxHistory.objects.create(**new_values)
                # check if there are some alerts set for current url
                if ProfileUrl.objects.filter(url__url=url, email_alert=True).exists():
                    email_launcher(url, new_values)

        elif device == "DESKTOP":
            # check if combination url and date exists with empty desktop values, if yes: update desktop values
            if CruxHistory.objects.filter(
                url__url=url, date=date, clsd__isnull=True
            ).exists():
                new_values = {}
                for name, value in json_response["record"]["metrics"].items():
                    new_values[f"{shortcuts[name]}d"] = float(
                        value["percentiles"]["p75"]
                    )
                object_to_update = CruxHistory.objects.filter(url__url=url, date=date)
                object_to_update.update(**new_values)
    return


def get_api_history_data(url):
    """Retrieves the latest data from the CrUX History API, saves it to the database
    (if data is new).

    Args:
        url (str): url address for which we want to download data

    Returns:
        This function has no return value.
    """
    api_url = f"https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord?key={os.getenv('API_KEY')}"
    for device in ["PHONE", "DESKTOP"]:
        request_body = {
            "url": url,
            "formFactor": device,
            "metrics": list(shortcuts.keys()),
        }
        api_call = requests.post(api_url, json=request_body)
        if api_call.status_code == 404:
            continue
        json_response = api_call.json()
        dates = []
        for date in json_response["record"]["collectionPeriods"]:
            date_list = [int(x) for x in date["lastDate"].values()]
            dates.append(datetime.date(date_list[0], date_list[1], date_list[2]))

        if device == "PHONE":
            for index, date in enumerate(dates):
                # check if combination url and date exists in db, if not: create new record with values for mobile
                if not CruxWeeklyHistory.objects.filter(
                    url__url=url, lastdate=date
                ).exists():
                    new_values = {"url": Urls.objects.get(url=url), "lastdate": date}
                    for name, value in json_response["record"]["metrics"].items():
                        new_values[f"{shortcuts[name]}m"] = float(
                            value["percentilesTimeseries"]["p75s"][index]
                        )
                    CruxWeeklyHistory.objects.create(**new_values)

        elif device == "DESKTOP":
            for index, date in enumerate(dates):
                # check if combination url and date exists with empty desktop values, if yes: update desktop values
                if CruxWeeklyHistory.objects.filter(
                    url__url=url, lastdate=date, clsd__isnull=True
                ).exists():
                    new_values = {}
                    for name, value in json_response["record"]["metrics"].items():
                        new_values[f"{shortcuts[name]}d"] = float(
                            value["percentilesTimeseries"]["p75s"][index]
                        )
                    object_to_update = CruxWeeklyHistory.objects.filter(
                        url__url=url, lastdate=date
                    )
                    object_to_update.update(**new_values)
    return


def email_trigger(url, new_values, sensitivity=2):
    """Checks whether the rules for sending an email alert for a given url and
    sensitivity settings are met.

    Args:
        url (str): url address for which we want check conditions for email alert
        new_values (dict): dict with url, date, and values of metrics for this date
        sensitivity (int): valufe that sets a different set of rules for evaluating
            conditions for sending alerts

    Returns:
        Dict containing metrics for which the condition for sending an alert
            has been met. Value for each metric is list of "current value" and
            "average of last 5 days".
            False if the condition for sending an alert is not met for any metric.
    """
    query_set_for_url = CruxHistory.objects.filter(url__url=url).order_by("-date")
    query_list = [
        entry for entry in query_set_for_url
    ]  # evaluate query set to cache results
    metrics_to_alert = {}
    trigger = False
    if len(query_set_for_url) >= 6:
        clsm = [q.clsm for q in query_set_for_url[1:6]]
        fidm = [q.fidm for q in query_set_for_url[1:6]]
        lcpm = [q.lcpm for q in query_set_for_url[1:6]]
        if sensitivity == 1:
            if new_values["clsm"] > mean(clsm):
                metrics_to_alert["clsm"] = [new_values["clsm"], mean(clsm)]
                trigger = True
            if new_values["fidm"] > mean(fidm):
                metrics_to_alert["fidm"] = [new_values["fidm"], mean(fidm)]
                trigger = True
            if new_values["lcpm"] > mean(lcpm):
                metrics_to_alert["lcpm"] = [new_values["lcpm"], mean(lcpm)]
                trigger = True
            if trigger:
                return metrics_to_alert
        elif sensitivity == 2:
            if new_values["clsm"] >= 0.8:
                if new_values["clsm"] > mean(clsm):
                    metrics_to_alert["clsm"] = [new_values["clsm"], mean(clsm)]
                    trigger = True
            if new_values["fidm"] >= 80:
                if new_values["fidm"] > mean(fidm):
                    metrics_to_alert["fidm"] = [new_values["fidm"], mean(fidm)]
                    trigger = True
            if new_values["lcpm"] >= 2500:
                if new_values["lcpm"] > mean(lcpm):
                    metrics_to_alert["lcpm"] = [new_values["lcpm"], mean(lcpm)]
                    trigger = True
            if trigger:
                return metrics_to_alert
    else:
        return False


def email_launcher(url, new_values):
    """Checks if there are users with alerts set for a given URL and triggers sending
     them.

    Args:
        url (str): The URL for which the email alerts are checked.
        new_values (dict): A dictionary of new values associated with the URL.

    Returns:
        This function has no return value.
    """
    alerts_s1 = ProfileUrl.objects.filter(email_alert=True, url__url=url, sensitivity=1)
    alerts_s2 = ProfileUrl.objects.filter(email_alert=True, url__url=url, sensitivity=2)
    trigger_s1 = email_trigger(url, new_values, 1)
    trigger_s2 = email_trigger(url, new_values, 2)
    if alerts_s1 and trigger_s1:
        for alert in alerts_s1:
            user_email = alert.profile.user.email
            send_email(user_email, url, trigger_s1)
    if alerts_s2 and trigger_s2:
        for alert in alerts_s2:
            user_email = alert.profile.user.email
            send_email(user_email, url, trigger_s2)


def send_email(user_email, url, metrics_to_alert):
    """Sends an email notification to the user with the given email address, containing
    information about the URL and the alerted metrics.

    Args:
        user_email (str): The email address of the user to send the notification to.
        url (str): The URL associated with the metrics.
        metrics_to_alert (dict): A dictionary mapping metrics to their values.

    Returns:
        This function has no return value.
    """
    port = 465  # For SSL
    password = os.getenv("EMAIL_PASSWORD")
    sender_email = os.getenv("EMAIL")
    urlid = Urls.objects.get(url=url).id
    metrics = [x for x in metrics_to_alert.keys()]
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.seznam.cz", port, context=context) as server:
        server.login(sender_email, password)
        if True:
            message_root = MIMEMultipart("related")
            message_root[
                "Subject"
            ] = f"ALERT - rychlost pro {url} se zhoršila v metrikách: {', '.join(metrics)}"
            message_root["From"] = sender_email
            message_root["To"] = user_email
            msg_body = MIMEMultipart("alternative")
            text = f"""\
          Rychlost metrik {' a '.join(metrics)} stoupla oproti průměru za posledních 5 dní.
          {os.linesep.join(f"Aktuální hodnota metriky {key} je {value[0]} a průměr je {value[1]}" for key, value in metrics_to_alert.items())}"""

            html = f"""\
              <html>
                <body>
                  <p>Rychlost metrik {' a '.join(metrics)} stoupla oproti průměru za posledních 5 dní.
                    {os.linesep.join(f"Aktuální hodnota metriky {key} je {value[0]} a průměr je {value[1]}" for key, value in metrics_to_alert.items())}          
                  </p>
                  <a href='https://www.webmetrics.cz/dashboard/{urlid}'>Dashboard této url</a>
                  {os.linesep.join(f"<img src='https://www.webmetrics.cz/{create_png_plot(metric, url, user_email)}' alt='Plot'>" for metric in metrics_to_alert.keys())}
                </body>
              </html>
              """

            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            msg_body.attach(part1)
            msg_body.attach(part2)
            message_root.attach(msg_body)
            server.sendmail(sender_email, user_email, message_root.as_string())


def create_png_plot(metric, url, user_email):
    query_set = CruxHistory.objects.filter(url__url=url)
    fig = create_plot(query_set, metric[:3], metric[-1])
    hash_email = hashlib.sha256(user_email.encode("utf-8"))
    hash_url = hashlib.sha256(url.encode("utf-8"))
    path = f"/static/images/{hash_email.hexdigest()[:6]}{metric}{hash_url.hexdigest()[:6]}.png"
    fig.write_image(f"{BASE_DIR}{path}")
    return path
