import logging
import os
import sys

from PyQt6 import (
    QtCore,
    QtWidgets,
    QtGui,
    uic
)

from utils.config_helper import ConfigHelper

main_window_ui_file = "srgssr_news_downloader/res/main_window.ui"
config_window_ui_file = ""
config_file = "config.ini"


class Window(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        
        ## GUI Setup
        uic.loadUi(main_window_ui_file, self)

        # MenuBar
        self.configMenu = QtGui.QAction("Konfiguration", self)
        self.infoMenu = QtGui.QAction("Info", self)
        self.menuBar.addAction(self.configMenu)
        self.menuBar.addAction(self.infoMenu)
        self.configMenu.triggered.connect(self.config_menu_clicked)
        self.infoMenu.triggered.connect(self.info_menu_clicked)

        self.label_status_value.setText("Initialisiere Programm")
        self.label_download_value.setText("Kein letzter Download.")

        ## Helper Setup
        self.log = logging.getLogger("news_downloader")
        self.config = ConfigHelper(config_file)
        self.setup_config()

    def config_menu_clicked(self) -> None:
        dlg = configWindow()
        dlg.exec()

    def info_menu_clicked(self) -> None:
        print("info")

    def update_status_label(self, value: str) -> None:
        """Update the status label with a new value.

        Args:
            value (str): Value that replaces the label text.
        """
        self.label_status_value.setText(value)

    def update_download_label(self, value: str) -> None:
        """Update the download label with a new value.

        Args:
            value (str): Value that replaces the label text.
        """
        self.label_download_value.setText(value)

    def setup_config(self):
        """Initial Setup of Configuration. Load file if it exists, if not create it.
        """
        try:
            if os.path.exists(config_file):
                self.log.info("Load config settings from file.")
                self.config.load_config()
            else:
                self.log.info("Creating new config file from default settings.")
                self.config.create_config()
        except Exception as ex:
            self.log.critical(f"Error while setting up configuration: {repr(ex)}")


class infoWindow(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QMainWindow):
        super().__init__(parent)


class configWindow(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QMainWindow, config: ConfigHelper):
        super().__init__(parent)

        self.setWindowTitle("Konfiguration")

        QBtn = QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel

        auth_group_box = QtWidgets.QGroupBox("Auth")


class ErrorDialog(QtWidgets.QDialog):
    def __init__(self, error: Exception, parent: QtWidgets.QMainWindow = None):
        """Show Error Dialog with information from raised exception.
        
        Args:
            error (Exception): Exception Object from raised Exception.
            parent (QtWidgets.QMainWindow): Pyqt6 Main GUI Window. Only optional for outside main Window scope.
        """
        if parent:
            super().__init__(parent)
        else:
            super().__init__()

        self.setWindowTitle("Fehler")
        
        QBtn = (QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel(
            f"Ein Fehler ist aufgetreten:\n\n{error}"
        )
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)


def replace_log() -> None:
    """ If a log file of an older session still exists, rename last sessions log file to "_old".
    Oldest log file gets deleted.
    """
    log_file = "output_log.txt"
    old_log_file = "output_log_old.txt"
    if os.path.exists(old_log_file): # Delete oldest log file
        os.remove(old_log_file)
    if os.path.exists(log_file): # Rename log file of the last session
        os.rename(log_file, old_log_file)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Rename old log files. Save exception, so we can write it to new log.
    replacement_exception = None
    try:
        replace_log()
    except Exception as ex:
        replacement_exception = ex

    ## Setup Logging
    # Import logger only after old log was replaced! Otherwise we get a permission error.
    from utils.logging_setup import logger  
    log = logging.getLogger("news_downloader")
    log.info("---   New Session started")

    # If logging replacement failed before, we will write it now.
    if replacement_exception: 
        ErrorDialog(replacement_exception).exec()
        log.error(f"Error occured when replacing logs: {repr(replacement_exception)}")


    window = Window()
    window.show()
    app.exec()
    sys.exit()

