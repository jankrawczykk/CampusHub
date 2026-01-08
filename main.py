from PyQt6.QtWidgets import QApplication
from app.ui.login_window import LoginWindow
from app.core.logging_config import setup_logging

def main():
    setup_logging()

    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()