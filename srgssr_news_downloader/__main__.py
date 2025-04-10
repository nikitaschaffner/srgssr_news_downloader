import logging
import os
import sys

from PyQt6 import QtGui, QtWidgets, uic
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from srgssr_news_downloader.utils.config_helper import ConfigHelper
from srgssr_news_downloader.utils.srgssr_api_helper import APIThread
from srgssr_news_downloader.version import __version__

main_window_ui_file = "srgssr_news_downloader/gui/main_window.ui"
icon_file = "srgssr_news_downloader/res/icon.ico"
config_window_ui_file = ""
config_file_name = "config.ini"


class Window(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        ## GUI Setup
        uic.loadUi(main_window_ui_file, self)
        self.setWindowTitle("SRGSSR News Downloader")

        # MenuBar Setup
        self.configMenu = QtGui.QAction("Konfiguration", self)
        self.infoMenu = QtGui.QAction("Info", self)
        self.menuBar.addAction(self.configMenu)
        self.menuBar.addAction(self.infoMenu)
        self.configMenu.triggered.connect(self.config_menu_clicked)
        self.infoMenu.triggered.connect(self.info_menu_clicked)

        self.label_status_value.setText("Initialisiere Programm")
        self.label_download_value.setText("-")

        ## Helper Setup
        self.log = logging.getLogger("news_downloader")
        self.config_helper = ConfigHelper(config_file_name)
        self.setup_config()

        ## Init Api Worker
        self.start_api_worker()

    ## API Worker
    def start_api_worker(self):
        self.api_thread = APIThread(self.config_helper)
        self.api_thread.worker.connection_status.connect(self.update_status_labels)
        self.api_thread.worker.error.connect(self.api_error_return)
        self.api_thread.start()

    ## GUI Events
    def closeEvent(self, event):
        # Stop API thread when window is closed
        self.api_thread.stop()
        self.log.info("---  End Session")
        event.accept()  # Execute close event

    def config_menu_clicked(self) -> None:
        dlg = configWindow(self, self.config_helper)
        r = dlg.exec()
        if r:
            self.log.info("New configuration saved by user.")
            # Restart API Worker
            try:
                self.api_thread.stop()
            except Exception:
                pass
            self.start_api_worker()

    def info_menu_clicked(self) -> None:
        dlg = infoWindow(self)
        dlg.show()

    ## GUI / API Worker Signals
    def update_status_labels(self, label_dict: dict):
        """Change labels based on values in dict. Only send dict for the label you want to change.

        Args:
            dict (dict): {
                status_label: {
                    text: str,
                    color: str
                },
                download_label: {
                    text: str,
                    color: str
                }
            }
        """
        self.log.debug(f"Label change: {label_dict}")

        if "status_label" in label_dict:
            if "text" in label_dict["status_label"]:
                self.label_status_value.setText(label_dict["status_label"]["text"])
                if "color" in label_dict["status_label"]:
                    self.label_status_value.setStyleSheet(
                        f"color: {label_dict['status_label']['color']};"
                    )
                else:
                    self.label_status_value.setStyleSheet("color: black")
            else:
                self.log.error(
                    "Error in text label change: 'status_label' was sent but no text information was given."
                )

        if "download_label" in label_dict:
            if "text" in label_dict["download_label"]:
                self.label_download_value.setText(label_dict["download_label"]["text"])
                if "color" in label_dict["download_label"]:
                    self.label_download_value.setStyleSheet(
                        f"color: {label_dict['download_label']['color']};"
                    )
                else:
                    self.label_download_value.setStyleSheet("color: black")
            else:
                self.log.error(
                    "Error in text label change: 'label_download_value' was sent but no text information was given."
                )

    def api_error_return(self, value):
        """Log Critical error and call error dialog window.

        Args:
            value (_type_): Exception Object
        """
        self.log.critical(value)
        self.log.exception(value)
        ErrorDialog(value, self)

    ## Functions
    def setup_config(self):
        """Initial Setup of Configuration. Load file if it exists, if not create it."""
        try:
            if os.path.exists(config_file_name):
                self.log.info("Load config settings from file.")
                self.config_helper.load_config()
            else:
                self.create_new_config()
        except Exception as ex:
            self.log.critical(f"Error while setting up configuration: {repr(ex)}")
            ErrorDialog(ex, self)
            sys.exit()

        # Validate the loaded config file. In case of error, ask if default should be loaded, or abort.
        try:
            self.log.info("Validating loaded config file.")
            self.config_helper.validate_config()
        except KeyError as ex:
            self.log.error(f"There was an error loading the config file: {repr(ex)}")
            dlg = confirmationDialog(
                self,
                "Standard Einstellungen Laden",
                "Die Konfigurationsdatei ist Fehlerhaft. Möchtest Du die Standardeinstellungen wiederherstellen?\n"
                "Achtung: Die bestehende Konfigurationsdatei wird dabei gelöscht.",
            )
            if dlg.show():
                self.create_new_config()
            else:
                self.log.info("Loading default settings aborted by user. Exit App.")
                sys.exit()

    def create_new_config(self):
        self.log.info("Creating new config file from default settings.")
        self.config_helper.create_config()


class confirmationDialog(QMessageBox):
    def __init__(self, parent: QtWidgets.QMainWindow, title: str, text: str):
        """Dialog Window with Simple Yes No Confirmation

        Args:
            parent (QtWidgets.QMainWindow): Parent window object
            title (str): Dialog Window Title
            text (str): Dialog Window Text
        """
        super().__init__(parent)
        self.setIcon(QMessageBox.Icon.Question)
        self.setWindowTitle(title)
        self.setText(text)

        # Add buttons
        self.yes_button = self.addButton("Ja", QMessageBox.ButtonRole.YesRole)
        self.no_button = self.addButton("Nein", QMessageBox.ButtonRole.NoRole)

    def show(self) -> bool:
        """Show dialog, return choice.

        Returns:
            bool: Return True if user clicked on Yes.
        """
        self.exec()
        return self.clickedButton() == self.yes_button


class configWindow(QDialog):
    def __init__(self, parent: QtWidgets.QMainWindow, config_helper: ConfigHelper):
        """Configuration window for the app user.

        Args:
            parent (QtWidgets.QMainWindow): Main window object
            config_helper (ConfigHelper): Config Helper object
        """
        super().__init__(parent)
        self.config_helper = config_helper
        self.setWindowTitle("Konfiguration")
        self.setup_ui()

    def setup_ui(self):
        """Config window UI"""
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        # URL's
        self.auth_url_input = QLineEdit(
            self.config_helper.get_value("auth", "auth_url")
        )
        self.api_url_input = QLineEdit(self.config_helper.get_value("api", "api_url"))
        form_layout.addRow("Auth API URL:", self.auth_url_input)
        form_layout.addRow("API URL:", self.api_url_input)

        # Auth section
        self.client_id_input = QLineEdit(
            self.config_helper.get_value("auth", "client_id")
        )
        self.client_secret_input = QLineEdit(
            self.config_helper.get_value("auth", "client_secret")
        )
        form_layout.addRow("API Client ID:", self.client_id_input)
        form_layout.addRow("API Client Secret:", self.client_secret_input)

        # API section
        self.business_unit_input = QComboBox()
        self.business_unit_input.addItems(["srf", "rts", "rsi"])
        self.business_unit_input.setCurrentText(
            self.config_helper.get_value("api", "business_unit")
        )
        self.update_cycle_input = QLineEdit(
            self.config_helper.get_value("api", "update_cycle")
        )
        form_layout.addRow("Business Unit:", self.business_unit_input)
        form_layout.addRow("Update Zyklus (Sekunden):", self.update_cycle_input)

        # Audio file section
        self.filename_input = QLineEdit(
            self.config_helper.get_value("audio_file", "filename")
        )
        self.filepath_input = QLineEdit(
            self.config_helper.get_value("audio_file", "filepath")
        )
        self.filepath_button = QPushButton("Speicherort...")
        self.filepath_button.clicked.connect(self.browse_filepath)
        form_layout.addRow("Dateiname:", self.filename_input)
        form_layout.addRow("Speicherort:", self.filepath_input)
        form_layout.addWidget(self.filepath_button)

        layout.addLayout(form_layout)

        # Save button
        button_layout = QHBoxLayout()
        save_button = QPushButton("Speichern")
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton("Abbrechen")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def browse_filepath(self):
        filepath = QFileDialog.getExistingDirectory(self, "Speicherort wählen..")
        if filepath:
            self.filepath_input.setText(filepath)

    def save_settings(self):
        # Update and save the config
        self.config_helper.set_value("auth", "auth_url", self.auth_url_input.text())
        self.config_helper.set_value("api", "api_url", self.api_url_input.text())
        self.config_helper.set_value("auth", "client_id", self.client_id_input.text())
        self.config_helper.set_value(
            "auth", "client_secret", self.client_secret_input.text()
        )
        self.config_helper.set_value(
            "api", "business_unit", self.business_unit_input.currentText()
        )
        self.config_helper.set_value(
            "api", "update_cycle", self.update_cycle_input.text()
        )
        self.config_helper.set_value(
            "audio_file", "filename", self.filename_input.text()
        )
        self.config_helper.set_value(
            "audio_file", "filepath", self.filepath_input.text()
        )

        # Show confirmation message
        QMessageBox.information(self, "Info", "Konfiguration gespeichert.")
        self.accept()


class infoWindow(QMessageBox):
    def __init__(self, parent: QtWidgets.QMainWindow):
        """_summary_

        Args:
            parent (QtWidgets.QMainWindow): Main Window object.
        """
        super().__init__(parent)
        self.setIcon(QMessageBox.Icon.Information)
        self.setWindowFilePath("App Information")
        self.setText(
            "SRGSSR News Downloader"
            "\n\nAuthor: Nikita Schaffner for Radio4TNG"
            f"\nVersion: {__version__}"
            "\nMIT License"
        )

        self.exec()


class ErrorDialog(QDialog):
    def __init__(self, error: Exception, parent: QtWidgets.QMainWindow = None):
        """Show Error Dialog with information from raised exception.

        Args:
            error (Exception): Exception Object from raised Exception.
            parent (QtWidgets.QMainWindow): Pyqt6 Main GUI Window. Only optional if called outside from main Window scope.
        """
        if parent:
            super().__init__(parent)
        else:
            super().__init__()

        self.setWindowTitle("Fehler")

        QBtn = QDialogButtonBox.StandardButton.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        # TODO THIS DOES NOT YET WORK
        message = QLabel(
            f"Ein Fehler ist aufgetreten:\n\n{type(error)}\n{error}\n{error.__traceback__}"
        )
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        self.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(icon_file))

    ## Setup Logging
    log = logging.getLogger("news_downloader")
    log.info("---   New Session started")

    ## Setup App and window
    window = Window()
    window.show()
    app.exec()
    sys.exit()
