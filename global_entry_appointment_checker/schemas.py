from datetime import datetime

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class Appointment(BaseModel):
    locationId: int
    startTimestamp: datetime
    endTimestamp: datetime
    active: bool
    duration: int
    remoteInd: bool
