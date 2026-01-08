from PyQt6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from app.core.logging_config import setup_logging

def main():
    setup_logging()

    app = QApplication([])
    window = MainWindow(app)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()