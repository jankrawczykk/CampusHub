import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from contextlib import contextmanager


@contextmanager
def show_loading_cursor():
    try:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        QApplication.processEvents()
        yield
    finally:
        QApplication.restoreOverrideCursor()
        QApplication.processEvents()


def disable_buttons_during_operation(buttons: list):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for button in buttons:
                if button:
                    button.setEnabled(False)
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                for button in buttons:
                    if button:
                        button.setEnabled(True)
        
        return wrapper
    return decorator