import configparser
import os

from .models import (AppConfig, Config, DatabaseConfig, DefaultConfig)

DEFAULT_CONFIG_PATH: str = "../../config/local.ini"


def load_config(path: str | None = None) -> Config:
    if path is None:
        path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)

    parser = configparser.ConfigParser()
    parser.read(path)

    application_data, database_data, default_data = parser["application"], parser["database"], parser["default"]

    application_config = AppConfig(
        debug=application_data.getboolean("debug"),
        major_version=application_data.getint("major_version"),
        minor_version=application_data.getint("minor_version"),
        patch_version=application_data.getint("patch_version"),
    )
    database_config = DatabaseConfig(
        url=database_data.get("url"),
    )
    default_config = DefaultConfig(
        url=default_data.get("upload_folder_url")
    )

    return Config(application_config, database_config, default_config)
