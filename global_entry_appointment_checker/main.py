from typing import Optional, Sequence
import logging
from urllib.parse import urljoin

import requests
from global_entry_appointment_checker.notify import send_notification
from global_entry_appointment_checker.settings import ApplicationSettings
from global_entry_appointment_checker.schemas import Appointment


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

settings: ApplicationSettings = ApplicationSettings.create()


def _check_for_appointments(location_code: int) -> Sequence[Optional[Appointment]]:
    url = urljoin(
        base=settings.CBP_BASE_URL,
        url=f"/schedulerapi/slots?orderBy=soonest&limit=3&locationId={location_code}&minimum=1",
    )
    with requests.Session() as s:
        r = s.get(url)
    if not r.ok:
        raise RuntimeError(f"Response not ok: {r}")
    appointments = [Appointment.parse_obj(_) for _ in r.json()]
    return appointments


def _get_location_info(location_code: int):
    url = urljoin(
        base=settings.CBP_BASE_URL,
        url="/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=Global%20Entry",
    )
    with requests.Session() as s:
        r = s.get(url)
    if not r.ok:
        raise RuntimeError(f"Response not ok: {r}")
    data = r.json()
    location_data = [_ for _ in data if int(_["id"]) == location_code][0]
    return location_data


def main():
    appointments = _check_for_appointments(settings.INTERVIEW_LOCATION_ID)
    if not appointments:
        log.info("No appointments found")
        return
    log.info("Found appointment(s)")
    location_info = _get_location_info(settings.INTERVIEW_LOCATION_ID)
    send_notification(appointments, location_info, settings)


if __name__ == "__main__":
    main()
