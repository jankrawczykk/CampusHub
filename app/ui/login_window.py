import logging
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from app.settings import APP_TITLE, UI_LOGIN, LOGO_FALLBACK_TEXT
from app.core.auth import verify_login
from app.core.theme_utils import get_logo_path

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        uic.loadUi(UI_LOGIN, self)
        
        self.setWindowTitle(f"{APP_TITLE} - Login")
        
        self._load_logo()
        
        self.loginButton.clicked.connect(self._handle_login)
        self.passwordInput.returnPressed.connect(self._handle_login)
        
        self.user_data = None
        
        logging.debug("LoginWindow initialized")
    
    def _load_logo(self):
        logo_path = get_logo_path("horizontal")
        pixmap = QPixmap(logo_path)
        
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaledToWidth(400, Qt.TransformationMode.SmoothTransformation)
            self.logoLabel.setPixmap(scaled_pixmap)
        else:
            logging.warning(f"Failed to load logo from: {logo_path}")
            self.logoLabel.setText(f'<html><head/><body><p align="center"><span style="font-size:36pt;">{LOGO_FALLBACK_TEXT}</span></p></body></html>')
    
    def _handle_login(self):
        from app.core.loading_utils import show_loading_cursor
        
        username = self.usernameInput.text().strip()
        password = self.passwordInput.text()
        
        self.errorLabel.setText("")
        
        if not username or not password:
            self._show_error("Please enter both username and password")
            return
        
        self.loginButton.setEnabled(False)
        self.loginButton.setText("Logging in...")
        
        with show_loading_cursor():
            success, user_data = verify_login(username, password)
        
        if success:
            logging.info(f"Login successful for: {username}")
            self.user_data = user_data
            
            self._open_dashboard()
        else:
            logging.warning(f"Login failed for: {username}")
            self._show_error("Invalid username or password")
            
            self.loginButton.setEnabled(True)
            self.loginButton.setText("Login")
            self.passwordInput.clear()
            self.passwordInput.setFocus()
    
    def _show_error(self, message: str):
        self.errorLabel.setText(message)
        self.errorLabel.setStyleSheet("color: #d32f2f; font-weight: bold;")
    
    def _open_dashboard(self):
        from app.ui.dashboard_window import DashboardWindow
        
        self.dashboard = DashboardWindow(self.user_data)
        self.dashboard.show()
        self.close()