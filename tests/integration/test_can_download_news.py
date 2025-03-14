from pathlib import Path
from tempfile import TemporaryDirectory

from srgssr_news_downloader.utils.config_helper import ConfigHelper, Configuration
from srgssr_news_downloader.utils.srgssr_api_helper import APIWorker

config_file_for_testing = "config_test.ini"


def test_can_connect_to_the_api():
    config_helper = ConfigHelper()
    config_helper._config = Configuration.load_from_ini(config_file_for_testing)

    agent = APIWorker(config_helper=config_helper)
    agent.connect_to_api()

    assert agent.is_connected()


def test_can_request_news():
    config_helper = ConfigHelper()
    config_helper._config = Configuration.load_from_ini(config_file_for_testing)

    agent = APIWorker(config_helper=config_helper)
    agent.connect_to_api()
    assert agent.is_connected()

    agent.get_news_data()
    assert agent.has_fetched_data()


def test_can_download_news():
    with TemporaryDirectory() as tmp_dir:
        config_helper = ConfigHelper()
        config = Configuration.load_from_ini(config_file_for_testing)

        config.audio_file.filepath = tmp_dir

        config_helper._config = config

        agent = APIWorker(config_helper=config_helper)
        agent.connect_to_api()
        assert agent.is_connected()

        agent.get_news_data()
        assert agent.has_fetched_data()

        # Downloading happens
        # Is my drectory empty ?
        clean_directory = set(Path(tmp_dir).iterdir())
        assert clean_directory == set()
        # ^ this should be empty

        agent.download_podcast()

        directory_after_download = set(Path(tmp_dir).iterdir())
        assert directory_after_download != set()
        # ^ this should contain any files

        downloaded_files = directory_after_download - clean_directory
        assert downloaded_files != set()
        # ^ this should contain donwloaded files
