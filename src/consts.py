"""Constants."""

import re

from PySide6 import QtCore

VERSION = "v1.2.3"

# Size of the main window
SIZE_MAIN_WINDOW = QtCore.QSize(1200, 800)

# Size of the tool bar icons
SIZE_ICON_TOOL_BAR = QtCore.QSize(30, 30)

# Size of the buttons
SIZE_BUTTON = 35

# Size of the icons
SIZE_ICON = 20

# Size of the margin between track layouts
MARGIN_TRACK_LAYOUT = 5

# Size of the progress bar
WIDTH_PROGRESS_BAR = 300
HEIGHT_PROGRESS_BAR = 25

# Margin of the central widget
MARGIN_CENTRAL_WIDGET = QtCore.QMargins(5, 5, 5, 5)

# Sizes of the cover
SIZE_COVER = 128

# Number of lyrics lines to display depending on the mode
LINES_LYRICS = 9

# URL of the Genius API page
URL_TOKEN = QtCore.QUrl("https://genius.com/api-clients")

# Splitters for the artists
SPLITTERS = " featuring | feat. | feat | ft. | ft | & | / "

# Remove multiple new lines
RE_REMOVE_LINES = re.compile(r"\n{2,}")

# Unwanted text in the title that would probably make the search fail
UNWANTED_TITLE_TEXT = [
    re.compile(r"\(radio\)", re.IGNORECASE),
    re.compile(r"\(radio edit\)", re.IGNORECASE),
    re.compile(r"\(live\)", re.IGNORECASE),
    re.compile(r"\(live version\)", re.IGNORECASE),
    re.compile(r"\(alternative\)", re.IGNORECASE),
    re.compile(r"\(alternative version\)", re.IGNORECASE),
    re.compile(r"\(extended\)", re.IGNORECASE),
    re.compile(r"\(extended version\)", re.IGNORECASE),
]

# If the artist is one of these, the lyrics are certainly wrong
DISCARD_ARTISTS = ["Genius", "Apple Music", "Pop Genius"]

# The lyrics of the song are missing
MISSING_LYRICS = "Tell us that you would like to have the lyrics of this song."

# Stylesheet for the QToolTip
STYLESHEET_QTOOLTIP = "QToolTip { font-size: 10pt; font-weight: 400 }"
