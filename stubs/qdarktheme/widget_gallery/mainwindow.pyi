from _typeshed import Incomplete
from qdarktheme.qtpy.QtCore import QDir as QDir, Qt as Qt, Slot as Slot
from qdarktheme.qtpy.QtGui import QAction as QAction, QActionGroup as QActionGroup, QFont as QFont, QIcon as QIcon
from qdarktheme.qtpy.QtWidgets import QApplication as QApplication, QColorDialog as QColorDialog, QFileDialog as QFileDialog, QFontDialog as QFontDialog, QLabel as QLabel, QMainWindow as QMainWindow, QMenuBar as QMenuBar, QMessageBox as QMessageBox, QSizePolicy as QSizePolicy, QStackedWidget as QStackedWidget, QStatusBar as QStatusBar, QToolBar as QToolBar, QToolButton as QToolButton, QWidget as QWidget
from qdarktheme.util import get_qdarktheme_root_path as get_qdarktheme_root_path
from qdarktheme.widget_gallery.ui.dock_ui import DockUI as DockUI
from qdarktheme.widget_gallery.ui.frame_ui import FrameUI as FrameUI
from qdarktheme.widget_gallery.ui.widgets_ui import WidgetsUI as WidgetsUI

class _WidgetGalleryUI:
    action_open_folder: Incomplete
    action_open_color_dialog: Incomplete
    action_open_font_dialog: Incomplete
    action_enable: Incomplete
    action_disable: Incomplete
    actions_theme: Incomplete
    actions_page: Incomplete
    actions_message_box: Incomplete
    actions_corner_radius: Incomplete
    central_window: Incomplete
    stack_widget: Incomplete
    toolbar: Incomplete
    def setup_ui(self, main_win: QMainWindow) -> None: ...

class WidgetGallery(QMainWindow):
    def __init__(self): ...
