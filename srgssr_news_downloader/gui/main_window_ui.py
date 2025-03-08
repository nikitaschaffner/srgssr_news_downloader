# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QRect,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QFont,
)
from PySide6.QtWidgets import (
    QFrame,
    QGroupBox,
    QLabel,
    QMenuBar,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 173)
        self.actionBearbeiten = QAction(MainWindow)
        self.actionBearbeiten.setObjectName("actionBearbeiten")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 781, 131))
        self.verticalLayoutWidget = QWidget(self.groupBox)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 761, 111))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.verticalLayoutWidget)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.label_status_name = QLabel(self.frame)
        self.label_status_name.setObjectName("label_status_name")
        self.label_status_name.setGeometry(QRect(10, 0, 161, 51))
        font = QFont()
        font.setFamilies(["Arial"])
        font.setPointSize(14)
        font.setBold(True)
        self.label_status_name.setFont(font)
        self.label_status_name.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.label_status_value = QLabel(self.frame)
        self.label_status_value.setObjectName("label_status_value")
        self.label_status_value.setGeometry(QRect(190, 0, 561, 51))
        font1 = QFont()
        font1.setFamilies(["Arial"])
        font1.setPointSize(14)
        font1.setBold(False)
        self.label_status_value.setFont(font1)
        self.label_status_value.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.label_status_value.setMargin(0)

        self.verticalLayout.addWidget(self.frame)

        self.frame_2 = QFrame(self.verticalLayoutWidget)
        self.frame_2.setObjectName("frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.label_download_name = QLabel(self.frame_2)
        self.label_download_name.setObjectName("label_download_name")
        self.label_download_name.setGeometry(QRect(10, 0, 161, 51))
        self.label_download_name.setFont(font)
        self.label_download_name.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.label_download_value = QLabel(self.frame_2)
        self.label_download_value.setObjectName("label_download_value")
        self.label_download_value.setGeometry(QRect(190, 0, 561, 51))
        self.label_download_value.setFont(font1)
        self.label_download_value.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.label_download_value.setMargin(0)

        self.verticalLayout.addWidget(self.frame_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName("menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menuBar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.actionBearbeiten.setText(
            QCoreApplication.translate("MainWindow", "Bearbeiten", None)
        )
        self.groupBox.setTitle("")
        self.label_status_name.setText(
            QCoreApplication.translate("MainWindow", "Status:", None)
        )
        self.label_status_value.setText(
            QCoreApplication.translate("MainWindow", "VALUE", None)
        )
        self.label_download_name.setText(
            QCoreApplication.translate("MainWindow", "Letzer Download:", None)
        )
        self.label_download_value.setText(
            QCoreApplication.translate("MainWindow", "VALUE", None)
        )

    # retranslateUi
