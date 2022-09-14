"""Application's informations window.

Handles the creation of the informations window.
"""

from PySide6 import QtCore, QtWidgets

from src.utils import VERSION, Color_


class WindowInformations(QtWidgets.QDialog):
    """Informations window of the GUI."""

    def __init__(self, parent):
        super().__init__(parent)

        self.setup_ui()

    def setup_ui(self) -> None:
        """Sets up the UI of the window."""
        self.label_gtagger = QtWidgets.QLabel(QtCore.QCoreApplication.applicationName())
        self.label_gtagger.setAlignment(QtCore.Qt.AlignCenter)
        self.label_gtagger.setStyleSheet("font-size: 20pt; font-weight:800")

        self.label_developper = QtWidgets.QLabel()
        self.label_developper.setAlignment(QtCore.Qt.AlignCenter)
        self.label_developper.setStyleSheet("font-size: 14pt; font-weight:600")
        self.label_developper.setTextFormat(QtCore.Qt.RichText)
        self.label_developper.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label_developper.setOpenExternalLinks(True)

        self.label_version = QtWidgets.QLabel(f"<i>{VERSION}</i>")
        self.label_version.setAlignment(QtCore.Qt.AlignCenter)
        self.label_version.setStyleSheet("font-size: 12pt;")
        self.label_developper.setTextFormat(QtCore.Qt.RichText)

        self.label_informations = QtWidgets.QLabel()
        self.label_informations.setAlignment(QtCore.Qt.AlignCenter)
        self.label_informations.setStyleSheet("font-size: 14pt; font-weight:400")
        self.label_informations.setTextFormat(QtCore.Qt.RichText)
        self.label_informations.setTextInteractionFlags(
            QtCore.Qt.TextBrowserInteraction
        )
        self.label_informations.setOpenExternalLinks(True)

        self.label_credits = QtWidgets.QLabel()
        self.label_credits.setStyleSheet("font-size: 12pt;")
        self.label_credits.setTextFormat(QtCore.Qt.RichText)
        self.label_credits.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label_credits.setOpenExternalLinks(True)

        self.set_texts(Color_.yellow_genius)

        self.layout_ = QtWidgets.QGridLayout()
        self.layout_.addWidget(self.label_gtagger, 0, 0, 1, 1, QtCore.Qt.AlignCenter)
        self.layout_.addWidget(self.label_developper, 1, 0, 1, 1, QtCore.Qt.AlignCenter)
        self.layout_.addWidget(self.label_version, 2, 0, 1, 1, QtCore.Qt.AlignCenter)
        self.layout_.addWidget(
            self.label_informations, 3, 0, 1, 1, QtCore.Qt.AlignCenter
        )
        self.layout_.addWidget(self.label_credits, 4, 0, 1, 1)

        self.setLayout(self.layout_)
        self.setWindowTitle("Informations")
        self.setWindowModality(QtCore.Qt.ApplicationModal)

    def set_texts(self, link_color: Color_) -> None:
        """Sets the texts of the labels.

        Args:
            link_color (Color_): Color of the links.
        """
        color = link_color.value

        self.label_developper.setText(
            f"""
            <a href="{QtCore.QCoreApplication.organizationDomain()}" style="color: {color}">{QtCore.QCoreApplication.organizationName()}</a>
            """
        )

        self.label_informations.setText(
            f"""
            <br />
            GTagger is a python tool that adds lyrics from <a href="https://genius.com" style="color: {color}">Genius</a> to <i>.mp3</i> files.
            <br />
            The code is open-source and hosted on <a href="https://github.com/maelchiotti/GTagger" style="color: {color}">GitHub</a>
            under the <a href="https://github.com/maelchiotti/GTagger/blob/main/LICENSE.txt" style="color: {color}">MIT license</a>.
            <br />
            """
        )
        self.label_credits.setText(
            f"""
            Credits (a more precise list can be found <a href=\"https://github.com/maelchiotti/GTagger/blob/main/CREDITS.md\" style="color: {color}">here</a>):
            <br />
            - <a href=\"https://genius.com\" style="color: {color}">Genius</a><br />
            - <a href=\"https://github.com/fedecalendino/wrap-genius\" style="color: {color}">wrap-genius</a><br />
            - <a href=\"https://github.com/nicfit/eyeD3\" style="color: {color}">eyeD3</a><br />
            - <a href=\"https://github.com/5yutan5/PyQtDarkTheme\" style="color: {color}">PyQtDarkTheme</a><br />
            - <a href=\"https://github.com/ionic-team/ionicons\" style="color: {color}">ionicons</a>
            """
        )
