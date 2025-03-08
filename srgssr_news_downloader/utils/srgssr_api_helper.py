from requests.auth import HTTPBasicAuth
from PyQt6.QtCore import QThread, pyqtSignal as Signal, QObject
from datetime import datetime
import logging
import os
import requests
import time
import validators

class APIWorker(QObject):
    # Communication signals
    connection_status = Signal(dict)
    error = Signal(object)

    """
    connection_status (dict): {
        status_label: {
            text: str,
            color: str
            },
        download_label: {
            text: str,
            color: str
            }
        }

    error (object): Exception Object, only called in uncaught exceptions
    """

    def __init__(self, config_helper = object):
        super().__init__()
        from utils.logging_setup import logger  
        self.log = logging.getLogger("news_downloader")

        self.config_helper = config_helper

        self.oauth_url          = str
        self.oauth_token        = str
        self.client_id          = str
        self.client_secret      = str

        self.api_url            = str
        self.business_unit      = str
        self.update_cycle       = int

        self.filepath           = str
        self.filename           = str
        self.savepath           = str

        self.response_content   = {}

        self.datetime_format = "%Y-%m-%dT%H:%M:%S%z"
        self.last_download_datetime_obj = datetime.strptime("0001-01-01T00:00:00+01:00", self.datetime_format)

        try:
            self.populate_config_data()
        except Exception as ex:
            pass

        self.running            = True
        self.config_helper      = config_helper

    def populate_config_data(self):
        config_get = self.config_helper.get_value

        self.oauth_url          = config_get("auth", "auth_url")
        self.client_id          = config_get("auth", "client_id")
        self.client_secret      = config_get("auth", "client_secret")

        self.api_url            = config_get("api", "api_url")
        self.business_unit      = config_get("api", "business_unit")
        self.update_cycle       = int(config_get("api", "update_cycle"))

        self.filepath           = config_get("audio_file", "filepath")
        self.filename           = config_get("audio_file", "filename")
        self.savepath           = f"{self.filepath}/{self.filename}"

        # Reformat
        self.api_url            = self.api_url.format(bu=self.business_unit)
        self.savepath           = self.savepath.format(bu=self.business_unit)
        print(self.api_url)
        print(self.savepath)

    def test_configuration(self):
        """Testing and validating the configurations.

        Raises:
            KeyError: Catching Errors with KeyError to display on GUI and stop the API Worker.
        """
        # Do we have any credentials in config?
        if not self.client_id:
            raise KeyError("Keine 'Client ID' in Konfiguration.")
        if not self.client_secret:
            raise KeyError("Kein 'Client Secret' in Konfiguration.")

        # Check if Business Unit is correct
        if not self.business_unit in ("srf", "rts", "rsi"):
            raise KeyError("Business Unit in Konfiguration fehlerhaft.")
        
        # Test OAuth URL
        self.log.info(f"Validating: {self.oauth_url}")
        if not self.oauth_url:
            raise KeyError("Keine 'oAuth URL' in Konfiguration.")
        if not validators.url(self.oauth_url):
            raise KeyError("OAUTH URL fehlerhaft")
        
        try: # Oauth Connection Test
            test_oauth_url = requests.get(self.oauth_url)
            self.log.debug(f"oAuth connection test: {test_oauth_url.status_code}")
            if not test_oauth_url.status_code == 401:
                raise KeyError("Verbindung zu oAuth Server nicht erfolgreich.")
        except Exception as ex:
            raise ex
        
        # Test API URL
        self.log.info(f"Validating: {self.api_url}")
        if not self.oauth_url:
            raise KeyError("Keine 'API URL' in Konfiguration.")
        if not validators.url(self.api_url):
            raise KeyError("API URL fehlerhaft")
        
        try: # API Connection Test
            test_api_url = requests.get(self.api_url)
            self.log.debug(f"API connection test: {test_api_url.status_code}")
            if not test_api_url.status_code == 401:
                raise KeyError("Verbindung zu API Server nicht erfolgreich.")
        except Exception as ex:
            raise ex
        
        # Test Filepath
        try:
            if self.filepath:
                if not os.path.exists(self.filepath):
                    raise KeyError("Speicherort existiert nicht.")
            else:
                raise KeyError("Kein Speicherort in Konfiguration")
        except Exception as ex:
            raise ex
        
        if not self.filename:
            raise KeyError("Kein Dateiname in Konfiguration.")

    def get_auth_token(self):
        """Fetch API Token from oAuth Server and save token in variable.

        Raises:
            RuntimeError: Raised in case of bad status code.
            KeyError: Raised in case the token is missing in response.
        """
        data = {
            "grant_type": "client_credentials"
        }
        response = requests.post(
            self.oauth_url, 
            data = data,
            auth=HTTPBasicAuth(self.client_id, self.client_secret)
        )
        self.log.debug(f"oAuth API: URL -> {self.oauth_url}")

        if response.status_code == 401:
            self.log.error("oAuth API: Client Credentials are wrong. 401 returned.")
            self.connection_status.emit({"status_label": {"text": "Fehler: Client ID oder Secret falsch", "color": "red"},
                                         "download_label": {"text": "Konfiguration öffnen und speichern für neustart.", "color": "red"}})
            raise RuntimeError()

        if not response.status_code == 200:
            self.log.error(f"oAuth API: Error handling oauth request. Status: {response.status_code}")
            self.connection_status.emit({"status_label": {"text": "Fehler bei Verbindung zu oAuth Server.", "color": "red"},
                                         "download_label": {"text": "Konfiguration öffnen und speichern für neustart.", "color": "red"}})
            raise RuntimeError()

        response_json = response.json()
        if response_json["access_token"]:
            self.oauth_token = response_json["access_token"]
        else:
            self.log.error("oAuth API: Did not receive token from api.")
            self.log.error(f"oAuth API: Server Response -> {response.text}")
            raise KeyError()

    def get_news_data(self):
        """Fetch News data from SRG API and save data in variable.

        Raises:
            RuntimeError: Raised if the auth token is invalid.
        """
        request_url = self.api_url
        headers = {
            "Authorization": f"Bearer {self.oauth_token}",
            "Content-Type": "application/json"
        }

        response = requests.get(request_url, headers=headers)
        if response.status_code == 401:
            raise RuntimeError()
        self.response_content = response.json()
        self.log.debug(self.response_content)

    def download(self):
        mp3 = requests.get(self.latest_file_dict["podcastHdUrl"], stream=True)

        if not mp3.status_code == 200:
            self.log.error(f"API: Error while trying to download latest audio file. Status -> {mp3.status_code}")
            self.log.error(mp3.text)
            raise RuntimeError()
        
        self.savepath_w_ext = f"{self.savepath}.mp3"
        self.log.debug("API: Download succesful. Writing file.")
        self.log.debug(f"API: Saving as {self.savepath_w_ext}")
        try:
            with open(self.savepath_w_ext, "wb") as file:
                for chunk in mp3.iter_content(chunk_size=1024):
                    file.write(chunk)
        except Exception as ex:
            raise ex
        finally:
            self.log.info("API: New audiofile has been saved.")
            self.last_download_datetime_obj = datetime.strptime(self.latest_file_dict["date"], self.datetime_format)
            self.response_content = {}
    
    def run(self):
        
        api_update_count = 0
        force_update = True
        self.oauth_token = ""

        try:
            self.connection_status.emit({"status_label": {"text": "Konfigurationsdaten werden getestet."},
                                         "download_label": {"text": "-"}})
            self.log.debug("Populate config data")
            self.populate_config_data()

            self.log.info("Test config")
            self.test_configuration()



            self.log.info("Config test successful")
            self.connection_status.emit({"status_label": {"text": "Starte Routine"},
                                         "download_label": {"text": "-"}})
            
        except KeyError as ex:
            self.connection_status.emit({"status_label": {"text": f"Fehler: {ex}", "color": "red"},
                                         "download_label": {"text": "Konfiguration öffnen und speichern für neustart.", "color": "red"}})
            self.running = False    # Kill worker in case of an error

        except Exception as ex:
            self.error.emit(ex)
            self.running = False    # Kill worker in case of an error

        while self.running:
            if force_update:
                api_update_count = self.update_cycle # Update the count to force start the cycle
                force_update = False

            if api_update_count >= self.update_cycle and self.running:
                self.log.debug("New cycle in worker routine starts.")

                # oAuth Routine, run when we have no token
                if not self.oauth_token:
                    try:
                        self.connection_status.emit({"status_label": {"text": "API Token wird angefordert..."},
                                                     "download_label": {"text": f"{self.last_download_datetime_obj}"}})
                        self.log.debug("Getting new oAuth token.")
                        self.get_auth_token()
                        self.log.debug(f"Received new oAuth token: {self.oauth_token}")
                    except RuntimeError:
                        self.oauth_token = ""
                        self.running = False
                    except KeyError:
                        self.oauth_token = ""
                        self.connection_status.emit({"status_label": {"text": "Warten auf oAuth Token.", "color": "orange"},
                                                     "download_label": {"text": f"{self.last_download_datetime_obj}"}})
                    except requests.exceptions.ConnectTimeout:
                        self.oauth_token = ""
                        self.connection_status.emit({"status_label": {"text": f"Verbindungsfehler zu oAuth Server. Neuversuch in {self.update_cycle}s", "color": "orange"},
                                                    "download_label": {"text": "Gegebenfalls Konfiguration überprüfen."}})
                    except Exception as ex:
                        self.oauth_token = ""
                        self.connection_status.emit({"status_label": {"text": "Ein unbekannter Fehler ist aufgetreten", "color": "red"},
                                                     "download_label": {"text": "Bitte Log Datei überprüfen und Fehler melden."}})
                        self.error.emit(ex)

                # News Fetch routine, run when we have oAuth token
                if self.oauth_token and self.running:
                    self.log.debug("API: Fetching news data.")
                    self.connection_status.emit({"status_label": {"text": "News Daten werden angefordert..."},
                                                 "download_label": {"text": f"{self.last_download_datetime_obj}"}})
                    try:
                        self.get_news_data()
                    except RuntimeError:
                            self.log.info("API: oAuth token not valid or expired.")
                            self.response_content = {} # Empty response content to skip download
                            self.oauth_token = "" # Empty token to force getting new token
                            force_update = True # Force start the next cycle
                    except requests.exceptions.ConnectionError:
                        self.response_content = {}
                        self.connection_status.emit({"status_label": {"text": f"Verbindungsfehler zu API Server. Neuversuch in {self.update_cycle}s", "color": "orange"},
                                                    "download_label": {"text": "Gegebenfalls Konfiguration überprüfen."}})
                    except Exception as ex:
                        self.connection_status.emit({"status_label": {"text": "Ein unbekannter Fehler ist aufgetreten", "color": "red"},
                                                     "download_label": {"text": "Bitte Log Datei überprüfen und Fehler melden."}})
                        self.error.emit(ex)
                    
                # Download routine, run when we have new content from news fetch
                if self.response_content:
                    # Content check before Download
                    if "podcasts" in self.response_content and self.running: 
                        try:
                            self.latest_file_dict = self.response_content["podcasts"][0]
                            if datetime.strptime(self.latest_file_dict["date"], self.datetime_format) > self.last_download_datetime_obj:
                                self.log.info("API: Download news file.")
                                self.connection_status.emit({"status_label": {"text": "Download Audiofile..."}, "download_label": {"text": f"{self.last_download_datetime_obj}"}})
                                try:
                                    self.download()
                                    # Success !
                                    self.connection_status.emit({"status_label": {"text": "Programm läuft ohne Fehler."}, "download_label": {"text": f"{self.last_download_datetime_obj}"}})
                                except RuntimeError:
                                    self.connection_status.emit({"status_label": {"text": f"Download Error. Neuversuch in {self.update_cycle}s", "color": "red"},
                                                            "download_label": {"text": f"{self.last_download_datetime_obj}"}})
                                    self.response_content = {}
                                except Exception as ex:
                                    self.connection_status.emit({"status_label": {"text": "Ein unbekannter Fehler ist aufgetreten", "color": "red"},
                                                                "download_label": {"text": "Bitte Log Datei überprüfen und Fehler melden."}})
                                    self.response_content = {}
                                    self.error.emit(ex)
                            else:
                                self.connection_status.emit({"status_label": {"text": "Programm läuft ohne Fehler."}, "download_label": {"text": f"{self.last_download_datetime_obj}"}})
                        except IndexError:
                            self.log.info("API: No News data in received podcast data. Normal if it's after midnight.")
                            self.connection_status.emit({"status_label": {"text": "Keine News Daten verfügbar", "color": "orange"},
                                                    "download_label": {"text": f"{self.last_download_datetime_obj}"}})
                            self.response_content = {}
                    else:
                        self.log.error("API: No Podcast data was received from API response.")
                        self.connection_status.emit({"status_label": {"text": "Keine Podcast Daten von API erhalten.", "color": "orange"},
                                                    "download_label": {"text": f"{self.last_download_datetime_obj}"}})
                        self.response_content = {}

                api_update_count = 0
            
            if self.running:
                api_update_count += 1
                time.sleep(1)

        self.log.info("API Worker finished work.")
        self.connection_status.emit({"status_label": {"text": "API Worker stopped.", "color": "red"},
                                         "download_label": {"text": "Konfiguration öffnen und speichern für neustart.", "color": "red"}})

    def stop(self):
        self.running = False


class APIThread(QThread):
    def __init__(self, config_helper):
        super().__init__()
        from utils.logging_setup import logger  
        self.log = logging.getLogger("news_downloader")

        self.log.info("Initializing API Worker.")
        self.worker = APIWorker(config_helper)

    def run(self):
        self.log.info("Starting API Worker.")
        self.worker.run()

    def stop(self):
        self.log.info("Stopping API worker.")
        self.worker.stop()  # Stop worker and its loop
        self.quit()         # Stop thread and exit
        self.wait()         # Make main thread wait until api thread is fully terminated
        self.log.info("API worker Stopped")