import configparser
import os

default_config: dict[str, dict[str, str]] = {
    "auth": {
        "auth_url" : "https://api.srgssr.ch/oauth/v1/accesstoken?grant_type=client_credentials", # Set 16.02.2025, from SRGSSR Dev Portal
        "cliend_id": "",        # From SRGSSR Dev Portal
        "client_secret": ""     # From SRGSSR Dev Portal
    },
    "api": {
        "api_url": "https://api.srgssr.ch/srgssr-news-podcasts/v1/{bu}/podcasts", # Set 16.02.2025, from SRGSSR Dev Portal
        "business_unit": "srf",     # Can be srf / rts / rsi
        "update_cycle":"60"         # In seconds
    },
    "audio_file": {
        "filename": "news",
        "filepath": ""
    }
}


class ConfigHelper():
    def __init__(self, filename: str = "config.ini"):
        """
        Init ConfigHelper.

        Args:
            filename (str): Name of configuration file. Default "config.ini".
        """
        self.config = configparser.ConfigParser()
        self.filename = filename

    def load_config(self) -> configparser.ConfigParser:
        """
        Load existing configuration file.
        
        Returns:
            configpaser.Configparser: Loaded configuration object.

        Raises:
            FileNotFoundError: Configuration file does not exist.
        """
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"Configuration file '{self.filename}' not found.")
        
        self.config.read(self.filename)
        return self.config

    def create_config(self) -> configparser.ConfigParser:
        """
        Create new config file with default values.
        
        Returns:
            configparser.ConfigParser: The created configuration object.
        """
        # Read default values into config object and write new config file
        self.config.read_dict(default_config)
        with open(self.filename, "w") as f:
            self.config.write(f)

        return self.config
    
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
            self.config[section]
        except KeyError:
            raise KeyError(f"Section '{section}' not found in configuration")
        
        try:
            return self.config[section][key]
        except KeyError:
            raise KeyError(f"Key '{key}' not found in section '{section}' in configuration")
        
    def set_value(self, section: str, key: str, value: str) -> None:
        """
        Set a value in the configuration and save it in the config file.

        Args:
            section (str): The configuration section (f.ex. "auth")
            key (str): The key in the section (f.ex. "auth_url")
            value (str): The value to set.
        """
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value

        # Overwrite config file
        with open(self.filename, "w") as f:
            self.config.write(f)

    def validate_config(self) -> bool:
        """Validate if the config file by comparing it to default values.

        Raises:
            KeyError: If a section or key is missing in the config file.

        Returns:
            bool: Returns True if config file is valid.
        """
        for section, keys in default_config.items():
            if section not in self.config:
                raise KeyError("Missing section '{section}' in '{self.filename}'.")
            
            for key, value in keys.items():
                if key not in self.config[section]:
                    raise KeyError("Missing key '{key}' in '{self.filename}'.")
                    
        return True
                