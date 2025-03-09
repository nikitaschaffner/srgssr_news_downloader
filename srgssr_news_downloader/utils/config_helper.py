import configparser
import os

from dataclasses import dataclass
from typing import Dict, Literal


@dataclass
class AuthConfiguration:
    auth_url: str = (
        "https://api.srgssr.ch/oauth/v1/accesstoken?grant_type=client_credentials"
    )
    client_id: str = ""
    client_secret: str = ""

    @classmethod
    def from_dict(cls, parser):
        return AuthConfiguration(
            auth_url=parser["auth"]["auth_url"],
            client_id=parser["auth"]["client_id"],
            client_secret=parser["auth"]["client_secret"],
        )

    def to_dict(self):
        return {
            "auth_url": self.auth_url,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }


@dataclass
class APIConfiguration:
    api_url: str = "https://api.srgssr.ch/srgssr-news-podcasts/v1/{bu}/podcasts"

    business_unit: Literal["srf"] | Literal["rts"] | Literal["rsi"] = "srf"
    """Can be srf / rts / rsi"""

    update_cycle: int = 60  # In seconds
    """In Seconds"""

    @classmethod
    def from_dict(cls, parser):
        return APIConfiguration(
            api_url=parser["api"]["api_url"],
            business_unit=parser["api"]["business_unit"],
            update_cycle=parser["api"]["update_cycle"],
        )

    def to_dict(self):
        return {
            "api_url": self.api_url,
            "business_unit": self.business_unit,
            "update_cycle": self.update_cycle,
        }


@dataclass
class AudioFileConfiguration:
    filename: str = "{bu}_news"
    filepath: str = ""

    @classmethod
    def from_dict(cls, parser):
        return AudioFileConfiguration(
            filename=parser["audio_file"]["filename"],
            filepath=parser["audio_file"]["filepath"],
        )

    def to_dict(self):
        return {"filename": self.filename, "filepath": self.filepath}


@dataclass
class Configuration:
    auth: AuthConfiguration
    api: APIConfiguration
    audio_file: AudioFileConfiguration

    @classmethod
    def load_from_ini(cls, ini_path: str):
        parser = configparser.ConfigParser()

        # Actually load from a file
        parser.read(ini_path)

        return cls.load_from_dict(parser.__dict__["_sections"])

    @classmethod
    def load_from_dict(cls, config: Dict):
        auth = AuthConfiguration.from_dict(config)
        api = APIConfiguration.from_dict(config)
        audio = AudioFileConfiguration.from_dict(config)

        return Configuration(auth=auth, api=api, audio_file=audio)

    def to_dict(self):
        return {
            "auth": self.auth.to_dict(),
            "api": self.api.to_dict(),
            "audio_file": self.audio_file.to_dict(),
        }

    @classmethod
    def load_default(cls):
        return Configuration(
            auth=AuthConfiguration(),
            api=APIConfiguration(),
            audio_file=AudioFileConfiguration(),
        )


default_config: dict[str, dict[str, str]] = {
    "auth": {
        "auth_url": "https://api.srgssr.ch/oauth/v1/accesstoken?grant_type=client_credentials",  # Set 16.02.2025, from SRGSSR Dev Portal
        "client_id": "",  # From SRGSSR Dev Portal
        "client_secret": "",  # From SRGSSR Dev Portal
    },
    "api": {
        "api_url": "https://api.srgssr.ch/srgssr-news-podcasts/v1/{bu}/podcasts",  # Set 16.02.2025, from SRGSSR Dev Portal
        "business_unit": "srf",  # Can be srf / rts / rsi
        "update_cycle": "60",  # In seconds
    },
    "audio_file": {"filename": "{bu}_news", "filepath": ""},
}


class ConfigHelper:
    def __init__(self, filename: str = "config.ini"):
        """
        Init ConfigHelper.

        Args:
            filename (str): Name of configuration file. Default "config.ini".
        """
        self.parser = configparser.ConfigParser()
        self._config: Configuration
        self.filename = filename

    def load_config(self) -> None:
        """
        Load existing configuration file.

        Returns:
            configpaser.Configparser: Loaded configuration object.

        Raises:
            FileNotFoundError: Configuration file does not exist.
        """
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"Configuration file '{self.filename}' not found.")

        self.parser.read(self.filename)

        self._config = Configuration.load_from_dict(self.parser.__dict__["_sections"])

    def create_config(self) -> None:
        """
        Create new config file with default values.

        Returns:
            configparser.ConfigParser: The created configuration object.
        """
        # Read default values into config object and write new config file
        self.parser.read_dict(default_config)
        with open(self.filename, "w") as f:
            self.parser.write(f)

    def get_value(self, section: str, key: str) -> str:
        """
        Get a specific value from the config object.

        Args:
            section (str): The configuration section (f.ex. "auth")
            key (str): The key in the section (f.ex. "auth_url")

        Returns:
            str: Value of the section-key combination

        Raises:
            KeyError: If section or key do not exist.
        """
        try:
            self._config.__dict__[section]
        except KeyError:
            raise KeyError(f"Section '{section}' not found in configuration")

        try:
            return self._config.__dict__[section].__dict__[key]
        except KeyError:
            raise KeyError(
                f"Key '{key}' not found in section '{section}' in configuration"
            )

    def set_value(self, section: str, key: str, value: str) -> None:
        """Set a value in the configuration and save it in the config file.

        Args:
            section (str): The configuration section (f.ex. "auth")
            key (str): The key in the section (f.ex. "auth_url")
            value (str): The value to set.
        """
        if section not in self._config.__dict__:
            raise ValueError(f"unknown section {section}")

        self._config.__dict__[section].__dict__[key] = value

        # Overwrite config file
        with open(self.filename, "w") as f:
            self.parser.write(f)

    def validate_config(self) -> bool:
        """Validate if the config file by comparing it to default values.

        Raises:
            KeyError: If a section or key is missing in the config file.

        Returns:
            bool: Returns True if config file is valid.
        """
        for section, keys in default_config.items():
            if section not in self._config:
                raise KeyError(f"Missing section '{section}' in '{self.filename}'.")

            for key, value in keys.items():
                if key not in self._config[section]:
                    raise KeyError(f"Missing key '{key}' in '{self.filename}'.")

        return True
