
# SRGSSR News Downloader

This tool will automatically download the audio news from SRGSSR using their own development API. The tool was developed for Radio4TNG and is free to use for anyone else. You are always welcome to support us: www.radio4tng.ch

To be able to use this tool, you are required to have a developer account at https://developer.srgssr.ch/ and need to have access to the "SRGSSR News Podcasts" API. Using those credentials, you will be able to use this tool.

The tool has only been tested on Windows Computers. A terminal only version for servers is planned for the future.

## Installation

Currently the tool requires a python installation on your windows computer.

1. Install Python 3.13 on your computer directly via the Microsoft Appstore: https://apps.microsoft.com/detail/9pnrbtzxmb4z
Restart your machine after installation. 

2. Download the latest version from here: https://github.com/nikitaschaffner/srgssr_news_downloader/releases/download/v101.0.0/srgssr_news_downloader_101.0.0.zip

3. Extract the .zip folder. Optionally copy the complete folder to where you want it to stay on your machine.

4. run the install.bat file in the folder. It will install all necessary python modules that are required for the tool to run. After the setup is complete, it will automatically create a shortcut inside the same folder. With that you can run the tool.

5. Start the tool with the newly created "SRGSSR News Downloader" shortcut.

6. Upon first startup, setup the configurations by clicking on the "Konfiguration" button. Afterwards the tool will automatically start the download whenever you startup the tool.

## Configuration

The following configuration options exist:

| Parameter  | Description                       |
| :--------  | :-------------------------------- |
| `Auth APi URL`       | URL of the SRGSSR Authentication API. Needed to login to the SRGSSR server. Please refer to the SRGSSR Developer Portal. |
| `API URL`       | URL of the SRGSSR News Podcast API. Needed to fetch the audio news data from the SRGSSR server. Please refer to the SRGSSR Developer Portal. |
| `API Client ID`       | Your Client ID from the SRGSSR News Podcast API. Please refer to the SRGSSR Developer Portal. |
| `API Client Secret`       | Your Client Secret from the SRGSSR News Podcast API. Please refer to the SRGSSR Developer Portal. |
| `Business Unit`       | Can be either SRF, RTS, RSI. |
| `Update Zyklus (seconds)`       | After how many seconds the Tool should check if there are new news. Default to 60 seconds. |
| `Dateiname`       | The filename that the news file should have, after the news have been downloaded. You can use the key {bu} to automatically set the name of the business unit. For example if business unit is SRF and the filename is set to "{bu}_news", it will be saved as "srf_news". |
| `Speicherort`       | Save path where the file should be saved. |

After saving the configuration, the tool will automatically start. If you need to quickly restart the tool for some reason, just open and save the configuration once without making any changes.

## Feedback

If you have any feedback, please reach out to me via Github, or via e-mail at dev@schaffnern.ch.
