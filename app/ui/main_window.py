import logging
from PyQt6 import uic
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow
from app.settings import (
    APP_TITLE,
    DEFAULT_WIDTH,
    DEFAULT_HEIGHT,
    MIN_WIDTH,
    MIN_HEIGHT,
)
from app.core.window_utils import get_centered_geometry
from app.core.database_connection import (
    get_database_connection,
    close_database_connection
)

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self._build_ui()

        self.setWindowTitle(APP_TITLE)

        x, y, w, h = get_centered_geometry(
            app,
            DEFAULT_WIDTH,
            DEFAULT_HEIGHT
        )
        self.setGeometry(x, y, w, h)
        self.setMinimumSize(QSize(MIN_WIDTH, MIN_HEIGHT))

        logging.debug("MainWindow initialized.")

        conn = get_database_connection()
        close_database_connection(conn)

    def _build_ui(self):
        uic.loadUi("app/ui/layout/dashboard.ui", self)

        logging.debug("UI components built.")