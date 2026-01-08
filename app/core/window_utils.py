import logging
from PyQt6.QtWidgets import QApplication

def get_centered_geometry(app: QApplication, width: int, height: int):
    screens = app.screens()
    if not screens:
        logging.warning("No screens found! Using default geometry.")
        return 100, 100, width, height

    screen = screens[0]
    geom = screen.availableGeometry()

    x = geom.x() + (geom.width() - width) // 2
    y = geom.y() + (geom.height() - height) // 2
    return x, y, width, height
