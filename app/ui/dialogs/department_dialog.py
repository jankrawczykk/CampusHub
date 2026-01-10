import logging
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QMessageBox
from app.core.loading_utils import show_loading_cursor
from app.core.loading_utils import show_loading_cursor
from app.settings import UI_DEPARTMENT_DIALOG
from app.models.department import Department


class DepartmentDialog(QDialog):
    def __init__(self, dept_id: int = None, parent=None):
        super().__init__(parent)
        
        uic.loadUi(UI_DEPARTMENT_DIALOG, self)
        
        self.dept_id = dept_id
        
        if self.dept_id:
            self.setWindowTitle("Edit Department")
            self.titleLabel.setText('<html><head/><body><p><span style="font-size:18pt; font-weight:600;">Edit Department</span></p></body></html>')
            self._load_department_data()
        else:
            self.setWindowTitle("Add Department")
            self.titleLabel.setText('<html><head/><body><p><span style="font-size:18pt; font-weight:600;">Add New Department</span></p></body></html>')
        
        self.buttonBox.accepted.connect(self._handle_save)
        self.buttonBox.rejected.connect(self.reject)
        
        logging.debug(f"DepartmentDialog initialized (dept_id: {dept_id})")
    
    def _load_department_data(self):
        department = Department.get_by_id(self.dept_id)
        
        if not department:
            QMessageBox.critical(self, "Error", "Failed to load department data")
            self.reject()
            return
        
        self.nameInput.setText(department.get('name', ''))
        self.codeInput.setText(department.get('code', ''))
        
        logging.debug(f"Loaded data for department {self.dept_id}")
    
    def _validate_form(self) -> tuple[bool, str]:
        if not self.nameInput.text().strip():
            return False, "Department name is required"
        
        if not self.codeInput.text().strip():
            return False, "Department code is required"
        
        code = self.codeInput.text().strip()
        if not code.replace(' ', '').isalnum():
            return False, "Department code should contain only letters and numbers"
        
        return True, ""
    
    def _get_form_data(self) -> dict:
        return {
            'name': self.nameInput.text().strip(),
            'code': self.codeInput.text().strip().upper()
        }
    
    def _handle_save(self):
        from app.core.loading_utils import show_loading_cursor

        self.errorLabel.setText("")
        
        is_valid, error_message = self._validate_form()
        
        if not is_valid:
            self.errorLabel.setText(error_message)
            return
        
        department_data = self._get_form_data()
        
        with show_loading_cursor():
            if self.dept_id:
                success = Department.update(self.dept_id, department_data)

                if success:
                    logging.info(f"Updated department {self.dept_id}")
                    QMessageBox.information(self, "Success", "Department updated successfully!")
                    self.accept()
                else:
                    self.errorLabel.setText("Failed to update department. Please check the logs.")
                    logging.error(f"Failed to update department {self.dept_id}")
            else:
                dept_id = Department.create(department_data)

                if dept_id:
                    logging.info(f"Created new department {dept_id}")
                    QMessageBox.information(self, "Success", "Department created successfully!")
                    self.accept()
                else:
                    self.errorLabel.setText("Failed to create department. Please check the logs.")
                    logging.error("Failed to create new department")