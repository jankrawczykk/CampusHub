import logging
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QMessageBox
from app.models.user import User
from app.models.employee import Employee
from app.settings import UI_USER_ACCOUNT_DIALOG


class UserAccountDialog(QDialog):
    def __init__(self, employee_id: int, employee_name: str, parent=None):
        super().__init__(parent)

        uic.loadUi(UI_USER_ACCOUNT_DIALOG, self)
        
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.user_data = None
        
        self.employeeLabel.setText(f"Employee: {employee_name}")
        
        self._load_user_account()
        
        self.buttonBox.accepted.connect(self._handle_save)
        self.buttonBox.rejected.connect(self.reject)
        self.deleteButton.clicked.connect(self._handle_delete)
        
        logging.debug(f"UserAccountDialog initialized for employee {employee_id}")
    
    def _load_user_account(self):
        from app.core.loading_utils import show_loading_cursor
        
        with show_loading_cursor():
            self.user_data = User.get_by_employee_id(self.employee_id)
        
        if self.user_data:
            self.statusLabel.setText(f"Status: ✓ Account exists (created {self.user_data['created_at'].strftime('%Y-%m-%d')})")
            self.statusLabel.setStyleSheet("color: green; font-weight: bold;")
            
            self.usernameInput.setText(self.user_data['username'])
            
            self.passwordHintLabel.setVisible(True)
            self.passwordLabel.setText("New Password:")
            self.confirmPasswordLabel.setText("Confirm New Password:")
            
            self.deleteButton.setEnabled(True)
        else:
            self.statusLabel.setText("Status: ✗ No account exists")
            self.statusLabel.setStyleSheet("color: #d32f2f; font-weight: bold;")
            
            self.passwordHintLabel.setVisible(False)
            
            self.deleteButton.setEnabled(False)
    
    def _validate_form(self) -> tuple[bool, str]:
        username = self.usernameInput.text().strip()
        password = self.passwordInput.text()
        confirm_password = self.confirmPasswordInput.text()
        
        if not username:
            return False, "Username is required"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        user_id_to_exclude = self.user_data['user_id'] if self.user_data else None
        if User.username_exists(username, user_id_to_exclude):
            return False, f"Username '{username}' is already taken"
        
        if not self.user_data:
            if not password:
                return False, "Password is required"
        else:
            if password or confirm_password:
                if not password:
                    return False, "Password cannot be empty if you're changing it"
        
        if password:
            if len(password) < 6:
                return False, "Password must be at least 6 characters"
            
            if password != confirm_password:
                return False, "Passwords do not match"
        
        return True, ""
    
    def _handle_save(self):
        from app.core.loading_utils import show_loading_cursor
        
        self.errorLabel.setText("")
        
        is_valid, error_message = self._validate_form()
        
        if not is_valid:
            self.errorLabel.setText(error_message)
            return
        
        username = self.usernameInput.text().strip()
        password = self.passwordInput.text()
        
        with show_loading_cursor():
            if self.user_data:
                success = True
                
                if username != self.user_data['username']:
                    success = User.update_username(self.user_data['user_id'], username)
                
                if success and password:
                    success = User.update_password(self.user_data['user_id'], password)
                
                if success:
                    logging.info(f"Updated user account for employee {self.employee_id}")
                    QMessageBox.information(self, "Success", "User account updated successfully!")
                    self.accept()
                else:
                    self.errorLabel.setText("Failed to update user account")
                    logging.error(f"Failed to update user for employee {self.employee_id}")
            else:
                user_id = User.create_user(self.employee_id, username, password)
                
                if user_id:
                    logging.info(f"Created user account for employee {self.employee_id}")
                    QMessageBox.information(self, "Success", f"User account created successfully!\nUsername: {username}")
                    self.accept()
                else:
                    self.errorLabel.setText("Failed to create user account")
                    logging.error(f"Failed to create user for employee {self.employee_id}")
    
    def _handle_delete(self):
        from app.core.loading_utils import show_loading_cursor
        
        if not self.user_data:
            return
        
        reply = QMessageBox.question(
            self,
            "Delete User Account",
            f"Are you sure you want to delete the user account '{self.user_data['username']}'?\n\n"
            f"This will prevent {self.employee_name} from logging into the system.\n\n"
            f"This action cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            with show_loading_cursor():
                success = User.delete_user(self.user_data['user_id'])
            
            if success:
                logging.info(f"Deleted user account for employee {self.employee_id}")
                QMessageBox.information(self, "Success", "User account deleted successfully!")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete user account")