import logging
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
from app.settings import APP_TITLE
from app.core.auth import verify_login

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        uic.loadUi("app/ui/layout/login.ui", self)
        
        self.setWindowTitle(f"{APP_TITLE} - Login")
        
        self.loginButton.clicked.connect(self._handle_login)
        self.passwordInput.returnPressed.connect(self._handle_login)
        
        self.user_data = None
        
        logging.debug("LoginWindow initialized")
    
    def _handle_login(self):
        username = self.usernameInput.text().strip()
        password = self.passwordInput.text()
        
        self.errorLabel.setText("")
        self.errorLabel.setStyleSheet("")
        
        if not username or not password:
            self._show_error("Please enter both username and password")
            return
        
        self.loginButton.setEnabled(False)
        self.loginButton.setText("Logging in...")
        
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