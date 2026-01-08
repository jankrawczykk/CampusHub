import logging
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from app.settings import APP_TITLE

class DashboardWindow(QMainWindow):
    def __init__(self, user_data: dict):
        super().__init__()
        
        self.user_data = user_data
        
        uic.loadUi("app/ui/layout/dashboard.ui", self)
        
        self.setWindowTitle(f"{APP_TITLE} - Dashboard")
        
        welcome_text = f"Welcome, {user_data['first_name']} {user_data['last_name']}!"
        self.header.setText(f'<html><head/><body><p align="center"><span style="font-size:36pt;">{welcome_text}</span></p></body></html>')
        
        self._setup_tabs()
        
        self._setup_menu()
        
        logging.info(f"Dashboard opened for user: {user_data['username']}")
    
    def _setup_tabs(self):
        self.mainTabMenu.clear()
        
        self.mainTabMenu.addTab(self._create_placeholder_widget("Students"), "Students")
        self.mainTabMenu.addTab(self._create_placeholder_widget("Departments"), "Departments")
        self.mainTabMenu.addTab(self._create_placeholder_widget("Employees"), "Employees")
        self.mainTabMenu.addTab(self._create_placeholder_widget("Courses"), "Courses")
        
        logging.debug("Dashboard tabs initialized")
    
    def _create_placeholder_widget(self, name: str):
        from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
        from PyQt6.QtCore import Qt
        
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel(f"{name} management coming soon...")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        widget.setLayout(layout)
        
        return widget
    
    def _setup_menu(self):
        from PyQt6.QtGui import QAction
        
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("&File")
        
        logout_action = QAction("&Logout", self)
        logout_action.setShortcut("Ctrl+L")
        logout_action.triggered.connect(self._handle_logout)
        file_menu.addAction(logout_action)
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
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