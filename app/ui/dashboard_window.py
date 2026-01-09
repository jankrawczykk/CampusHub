import logging
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from app.settings import APP_TITLE

class DashboardWindow(QMainWindow):
    def __init__(self, user_data: dict):
        super().__init__()
        
        self.user_data = user_data
        
        uic.loadUi("app/ui/layout/dashboard.ui", self)
        
        self.setWindowTitle(f"{APP_TITLE} - Dashboard")
        
        self._setup_header()
        
        self._setup_tabs()
        
        self.logoutButton.clicked.connect(self._handle_logout)
        
        logging.info(f"Dashboard opened for user: {user_data['username']}")
    
    def _setup_header(self):
        welcome_text = f"Welcome, {self.user_data['first_name']}!"
        self.headerLabel.setText(
            f'<html><head/><body><p><span style="font-size:24pt; font-weight:600;">{welcome_text}</span></p></body></html>'
        )
        
        user_info = f"{self.user_data['first_name']} {self.user_data['last_name']} ({self.user_data['email']})"
        self.userInfoLabel.setText(
            f'<html><head/><body><p><span style="font-size:11pt; color:#666666;">{user_info}</span></p></body></html>'
        )
    
    def _setup_tabs(self):
        self.mainTabMenu.clear()
        
        self.mainTabMenu.addTab(self._create_placeholder("Students"), "Students")
        self.mainTabMenu.addTab(self._create_placeholder("Departments"), "Departments")
        self.mainTabMenu.addTab(self._create_placeholder("Employees"), "Employees")
        self.mainTabMenu.addTab(self._create_placeholder("Courses"), "Courses")
        
        logging.debug("Dashboard tabs initialized")
    
    def _create_placeholder(self, name: str) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel(f"{name} management will be implemented soon...")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 14pt; color: #999;")
        
        layout.addWidget(label)
        widget.setLayout(layout)
        
        return widget
    
    def _handle_logout(self):
        reply = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            logging.info(f"User logged out: {self.user_data['username']}")
            
            from app.ui.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            
            self.close()