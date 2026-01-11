import logging
from datetime import date
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import QDate
from app.settings import UI_ASSIGN_HEAD_DIALOG
from app.models.department import Department
from app.models.employee import Employee


class AssignHeadDialog(QDialog):
    def __init__(self, dept_id: int, dept_name: str, parent=None):
        super().__init__(parent)
        
        uic.loadUi(UI_ASSIGN_HEAD_DIALOG, self)
        
        self.dept_id = dept_id
        self.dept_name = dept_name
        
        self.departmentLabel.setText(f"Department: {dept_name}")
        
        self._load_employees()
        
        self.startDateInput.setDate(QDate.currentDate())
        
        self._load_current_head()
        
        self.buttonBox.accepted.connect(self._handle_assign)
        self.buttonBox.rejected.connect(self.reject)
        self.removeButton.clicked.connect(self._handle_remove)
        
        logging.debug(f"AssignHeadDialog initialized for department {dept_id}")
    
    def _load_employees(self):
        employees = Employee.get_all_for_dropdown()
        
        self.employeeInput.clear()
        self.employeeInput.addItem("Select an employee...", None)
        
        for emp in employees:
            display_text = emp['full_name']
            if emp.get('position_name'):
                display_text += f" ({emp['position_name']})"
            self.employeeInput.addItem(display_text, emp['employee_id'])
        
        logging.debug(f"Loaded {len(employees)} employees into dropdown")
    
    def _load_current_head(self):
        current_head = Department.get_current_head(self.dept_id)
        
        if current_head:
            head_text = f"{current_head['full_name']}"
            if current_head.get('position_name'):
                head_text += f" ({current_head['position_name']})"
            head_text += f"\nSince: {current_head['start_date']}"
            
            self.currentHeadLabel.setText(head_text)
            self.removeButton.setEnabled(True)
        else:
            self.currentHeadLabel.setText("No head currently assigned")
            self.removeButton.setEnabled(False)
    
    def _validate_form(self) -> tuple[bool, str]:
        if self.employeeInput.currentIndex() == 0:
            return False, "Please select an employee"
        
        return True, ""
    
    def _handle_assign(self):
        from app.core.loading_utils import show_loading_cursor

        self.errorLabel.setText("")
        
        is_valid, error_msg = self._validate_form()
        if not is_valid:
            self.errorLabel.setText(error_msg)
            return
        
        employee_id = self.employeeInput.currentData()
        start_date = self.startDateInput.date().toPyDate()
        
        success = Department.assign_head(self.dept_id, employee_id, start_date)
        
        with show_loading_cursor():
            if success:
                employee_name = self.employeeInput.currentText().split(' (')[0]
                logging.info(f"Assigned {employee_name} as head of {self.dept_name}")
                QMessageBox.information(
                    self,
                    "Success",
                    f"{employee_name} has been assigned as head of {self.dept_name}!"
                )
                self.accept()
            else:
                self.errorLabel.setText("Failed to assign department head")
                logging.error(f"Failed to assign head for department {self.dept_id}")
    
    def _handle_remove(self):
        from app.core.loading_utils import show_loading_cursor

        current_head = Department.get_current_head(self.dept_id)
        
        if not current_head:
            return
        
        reply = QMessageBox.question(
            self,
            "Remove Department Head",
            f"Are you sure you want to remove {current_head['full_name']} as head of {self.dept_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = Department.remove_head(self.dept_id, date.today())
            
            with show_loading_cursor():
                if success:
                    logging.info(f"Removed head from {self.dept_name}")
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Department head removed from {self.dept_name}!"
                    )
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "Failed to remove department head")