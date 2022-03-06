from typing import List
import json
import smtplib
from smtplib import SMTP

from global_entry_appointment_checker.schemas import Appointment
from global_entry_appointment_checker.settings import ApplicationSettings


def _format_message(appts: List[Appointment], location_data) -> str:
    dates = "\n".join([_.startTimestamp.isoformat() for _ in appts])
    body = f"""
Global Entry Interview Appointment{'s' if len(appts) > 1 else ''} Available at {location_data["name"]}:

{dates}

Visit https://ttp.cbp.dhs.gov/ schedule interview

Location Data:
{json.dumps(location_data, indent=2)}
    """
    return body


def _get_server(settings: ApplicationSettings) -> SMTP:
    server = smtplib.SMTP(settings.SMTP_ENDPOINT)
    server.starttls()
    server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
    return server


def send_notification(
    appts: List[Appointment], location_data, settings: ApplicationSettings
):
    message = _format_message(appts, location_data)
    server = _get_server(settings)
    server.sendmail(settings.EMAIL_SENDER, settings.EMAIL_RECIPIENT, message)
