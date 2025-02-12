import os
import requests
from requests.auth import HTTPBasicAuth
import configparser


class app():
    def __init__(self):
        pass

        self.oauth_url      = str
        self.oauth_token    = str
        self.client_id      = str
        self.client_secret  = str

        self.api_url        = str
        self.business_unit  = str
        self.show           = str

        self.config_file    = "config.ini"
        self.config         = configparser.ConfigParser()


    def read_config(self):
        if not os.path.exists(self.config_file):
            raise ValueError("Config File does not exist")
        
        self.config.read(self.config_file)

        self.oauth_url      = self.config["oauth"]["oauth_url"]
        self.client_id      = self.config["oauth"]["client_id"]
        self.client_secret  = self.config["oauth"]["client_secret"]

        self.api_url        = self.config["api"]["api_url"]
        self.business_unit  = self.config["api"]["business_unit"]
        self.show           = self.config["api"]["show"]


    def api_get_auth_token(self):
        data = {
            "grant_type": "client_credentials"
        }
        response = requests.post(
            self.oauth_url, 
            data = data,
            auth=HTTPBasicAuth(self.client_id, self.client_secret)
        )

        if not response.status_code == 200:
            return

        response_json = response.json()
        if response_json["access_token"]:
            self.oauth_token = response_json["access_token"]
        
        return


    def api_get_news_data(self):
        if not self.oauth_token:
            raise ValueError("Oauth token is missing.")

        if not self.business_unit:
            raise ValueError("Business unit not defined. Must be srf, rts or rsi")
        
        request_url = self.api_url.format(bu=self.business_unit)

        headers = {
            "Authentication": self.oauth_token
        }

        response = requests.get(request_url, headers=headers)
        print(response.text)


    def download_news_audio(self):
        pass


if __name__ == "__main__":
    app = app()

    try:
        app.read_config()
    except Exception as ex:
        print(f"-- ERROR Reading config file --\n{ex}")

    try:
        app.api_get_auth_token()
    except Exception as ex:
        print(f"-- ERROR Getting auth token --\n{ex}")

    try:
        app.api_get_news_data()
    except Exception as ex:
        print(f"-- ERROR Getting News Data --\n{ex}")

    try:
        app.download_news_audio()
    except Exception as ex:
        print(f"-- ERROR Downloading News Audio --\n{ex}")