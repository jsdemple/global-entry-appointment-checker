import logging
import os
import pathlib

from pydantic import BaseSettings, ConfigError  # pylint: disable=no-name-in-module


log = logging.getLogger(__name__)


class ApplicationSettings(BaseSettings):
    APP_ENV: str
    CBP_BASE_URL: str = "https://ttp.cbp.dhs.gov"
    EMAIL_PASSWORD: str
    EMAIL_SENDER: str
    EMAIL_RECIPIENT: str
    EMAIL_USERNAME: str
    INTERVIEW_LOCATION_ID: int
    SEND_EMAIL: bool
    SMTP_ENDPOINT: str

    class Config:
        case_sensitive = True
        allow_mutation = False
        frozen = True

    @staticmethod
    def create():
        env = os.environ["APP_ENV"]
        env_file = pathlib.Path(f"./config/{env}.env")
        if not env_file.exists():
            raise ConfigError(f"{env_file} does not exist.")

        log.debug(f"Creating settings using {env_file}")
        app_settings = ApplicationSettings(_env_file=env_file)
        return app_settings
