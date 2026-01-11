import logging
import re
from datetime import date
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QMessageBox, QDialogButtonBox
from PyQt6.QtCore import QDate
from app.settings import UI_EMPLOYEE_DIALOG
from app.models.employee import Employee
from app.models.position import Position


class EmployeeDialog(QDialog):    
    def __init__(self, employee_id: int = None, parent=None):
        super().__init__(parent)
        
        uic.loadUi(UI_EMPLOYEE_DIALOG, self)
        
        self.employee_id = employee_id

        self.existing_person_id = None
        self.existing_person_roles = None
        
        self._load_positions()
        
        self._set_default_dates()
        
        if self.employee_id:
            self.setWindowTitle("Edit Employee")
            self.titleLabel.setText('<html><head/><body><p><span style="font-size:18pt; font-weight:600;">Edit Employee</span></p></body></html>')
            self._load_employee_data()
        else:
            self.setWindowTitle("Add Employee")
            self.titleLabel.setText('<html><head/><body><p><span style="font-size:18pt; font-weight:600;">Add New Employee</span></p></body></html>')
        
        self.buttonBox.accepted.connect(self._handle_save)
        self.buttonBox.rejected.connect(self.reject)
        self.peselInput.textChanged.connect(self._check_pesel)
        
        logging.debug(f"EmployeeDialog initialized (employee_id: {employee_id})")
    
    def _load_positions(self):
        positions = Position.get_all_for_dropdown()
        
        self.positionInput.clear()
        self.positionInput.addItem("No position assigned", None)
        
        for position in positions:
            self.positionInput.addItem(position['name'], position['position_id'])
        
        logging.debug(f"Loaded {len(positions)} positions into dropdown")
    
    def _set_default_dates(self):
        today = QDate.currentDate()
        
        self.employmentDateInput.setDate(today)
        
        thirty_years_ago = today.addYears(-30)
        self.dateOfBirthInput.setDate(thirty_years_ago)
    
    def _load_employee_data(self):
        employee = Employee.get_by_id_with_details(self.employee_id)
        
        if not employee:
            QMessageBox.critical(self, "Error", "Failed to load employee data")
            self.reject()
            return
        
        self.firstNameInput.setText(employee.get('first_name', ''))
        self.lastNameInput.setText(employee.get('last_name', ''))
        self.peselInput.setText(employee.get('pesel', ''))
        
        if employee.get('date_of_birth'):
            dob = employee['date_of_birth']
            self.dateOfBirthInput.setDate(QDate(dob.year, dob.month, dob.day))
        
        gender = employee.get('gender')
        if gender:
            index = self.genderInput.findText(gender)
            if index >= 0:
                self.genderInput.setCurrentIndex(index)
        
        self.emailInput.setText(employee.get('email', ''))
        self.phoneInput.setText(employee.get('phone_number', '') or '')
        self.addressInput.setText(employee.get('address', '') or '')
        
        employment_date = employee.get('employment_date')
        if employment_date:
            self.employmentDateInput.setDate(QDate(employment_date.year, employment_date.month, employment_date.day))
        
        status = employee.get('status', 'Active')
        index = self.statusInput.findText(status)
        if index >= 0:
            self.statusInput.setCurrentIndex(index)
        
        position_id = employee.get('position_id')
        if position_id:
            for i in range(self.positionInput.count()):
                if self.positionInput.itemData(i) == position_id:
                    self.positionInput.setCurrentIndex(i)
                    break
        
        logging.debug(f"Loaded data for employee {self.employee_id}")
    
    def _validate_form(self) -> tuple[bool, str]:
        if not self.firstNameInput.text().strip():
            return False, "First name is required"
        
        if not self.lastNameInput.text().strip():
            return False, "Last name is required"
        
        if not self.emailInput.text().strip():
            return False, "Email is required"
        
        if not self.peselInput.text().strip():
            return False, "PESEL is required"
        
        pesel = self.peselInput.text().strip()
        if not re.match(r'^\d{11}$', pesel):
            return False, "PESEL must be exactly 11 digits"
        
        email = self.emailInput.text().strip()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return False, "Invalid email format"
        
        if self.genderInput.currentIndex() == 0:
            return False, "Please select a gender"
        
        return True, ""
    
    def _get_form_data(self) -> tuple[dict, dict, int]:
        person_data = {
            'first_name': self.firstNameInput.text().strip(),
            'last_name': self.lastNameInput.text().strip(),
            'pesel': self.peselInput.text().strip(),
            'email': self.emailInput.text().strip(),
        }
        
        dob = self.dateOfBirthInput.date().toPyDate()
        person_data['date_of_birth'] = dob
        
        gender_index = self.genderInput.currentIndex()
        if gender_index > 0:
            person_data['gender'] = self.genderInput.currentText()
        else:
            person_data['gender'] = None
        
        phone = self.phoneInput.text().strip()
        person_data['phone_number'] = phone if phone else None
        
        address = self.addressInput.text().strip()
        person_data['address'] = address if address else None
        
        employment_date = self.employmentDateInput.date().toPyDate()
        employee_data = {
            'employment_date': employment_date,
            'status': self.statusInput.currentText()
        }
        
        position_id = self.positionInput.currentData()
        
        return person_data, employee_data, position_id
    
    def _handle_save(self):
        from app.core.loading_utils import show_loading_cursor
        
        if not self.existing_person_id:
            self.errorLabel.setText("")
        
        is_valid, error_message = self._validate_form()
        
        if not is_valid:
            self.errorLabel.setText(error_message)
            self.errorLabel.setStyleSheet("color: #d32f2f; font-weight: bold;")
            return
        
        person_data, employee_data, position_id = self._get_form_data()
        
        with show_loading_cursor():
            if self.employee_id:
                success = Employee.update_with_person(
                    self.employee_id,
                    person_data,
                    employee_data,
                    position_id
                )
                
                if success:
                    logging.info(f"Updated employee {self.employee_id}")
                    QMessageBox.information(self, "Success", "Employee updated successfully!")
                    self.accept()
                else:
                    self.errorLabel.setText("Failed to update employee. Please check the logs.")
                    self.errorLabel.setStyleSheet("color: #d32f2f; font-weight: bold;")
                    logging.error(f"Failed to update employee {self.employee_id}")
            else:
                employee_id = Employee.create_with_person(
                    person_data,
                    employee_data,
                    position_id,
                    existing_person_id=self.existing_person_id
                )
                
                if employee_id:
                    logging.info(f"Created new employee {employee_id}")
                    if self.existing_person_id:
                        QMessageBox.information(self, "Success", "Employee created successfully using existing person record!")
                    else:
                        QMessageBox.information(self, "Success", "Employee created successfully!")
                    self.accept()
                else:
                    self.errorLabel.setText("Failed to create employee. Please check the logs.")
                    self.errorLabel.setStyleSheet("color: #d32f2f; font-weight: bold;")
                    logging.error("Failed to create new employee")

    def _check_pesel(self):
        from app.models.person import Person
        
        pesel = self.peselInput.text().strip()
        
        if len(pesel) == 11 and pesel.isdigit() and not self.employee_id:
            person = Person.get_by_pesel(pesel)
            
            if person:
                roles = Person.check_roles(person['person_id'])
                
                warning = f"⚠️ This PESEL belongs to: {person['first_name']} {person['last_name']}\n"
                
                if roles['is_student']:
                    status = roles['student_info']['status']
                    warning += f"• Already a student (Status: {status})\n"
                
                if roles['is_employee']:
                    status = roles['employee_info']['status']
                    warning += f"• Already an employee (Status: {status})\n"
                
                if roles['is_employee']:
                    self.errorLabel.setText(warning + "\nCannot create duplicate employee record!")
                    self.buttonBox.button(QDialogButtonBox.StandardButton.Save).setEnabled(False)
                    self.existing_person_id = None
                elif roles['is_student']:
                    warning += "\nPerson data will be reused. Only update if needed."
                    self.errorLabel.setText(warning)
                    self.errorLabel.setStyleSheet("color: #ff9800; font-weight: bold;")  # Orange warning
                    self.existing_person_id = person['person_id']
                    self.existing_person_roles = roles
                    
                    self._prefill_person_data(person)
                    
                    self.buttonBox.button(QDialogButtonBox.StandardButton.Save).setEnabled(True)
                else:
                    warning += "\nPerson data will be reused."
                    self.errorLabel.setText(warning)
                    self.errorLabel.setStyleSheet("color: #ff9800; font-weight: bold;")
                    self.existing_person_id = person['person_id']
                    
                    self._prefill_person_data(person)
                    
                    self.buttonBox.button(QDialogButtonBox.StandardButton.Save).setEnabled(True)
            else:
                self.errorLabel.setText("")
                self.existing_person_id = None
                self.existing_person_roles = None
                self.buttonBox.button(QDialogButtonBox.StandardButton.Save).setEnabled(True)

    def _prefill_person_data(self, person: dict):
        self.firstNameInput.setText(person.get('first_name', ''))
        self.lastNameInput.setText(person.get('last_name', ''))
        self.emailInput.setText(person.get('email', ''))
        self.phoneInput.setText(person.get('phone_number', '') or '')
        self.addressInput.setText(person.get('address', '') or '')

        if person.get('date_of_birth'):
            from PyQt6.QtCore import QDate
            dob = person['date_of_birth']
            self.dateOfBirthInput.setDate(QDate(dob.year, dob.month, dob.day))
        
        gender = person.get('gender')
        if gender:
            index = self.genderInput.findText(gender)
            if index >= 0:
                self.genderInput.setCurrentIndex(index)