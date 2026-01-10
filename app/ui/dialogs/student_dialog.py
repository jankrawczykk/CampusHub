import logging
import re
from datetime import date
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import QDate
from app.models.student import Student
from app.models.major import Major


class StudentDialog(QDialog):
    def __init__(self, student_id: int = None, parent=None):
        super().__init__(parent)
        
        uic.loadUi("app/ui/layout/student_dialog.ui", self)
        
        self.student_id = student_id
        
        self._load_majors()
        
        self._set_default_dates()
        
        if self.student_id:
            self.setWindowTitle("Edit Student")
            self.titleLabel.setText('<html><head/><body><p><span style="font-size:18pt; font-weight:600;">Edit Student</span></p></body></html>')
            self._load_student_data()
        else:
            self.setWindowTitle("Add Student")
            self.titleLabel.setText('<html><head/><body><p><span style="font-size:18pt; font-weight:600;">Add New Student</span></p></body></html>')
        
        self.buttonBox.accepted.connect(self._handle_save)
        self.buttonBox.rejected.connect(self.reject)
        
        logging.debug(f"StudentDialog initialized (student_id: {student_id})")
    
    def _load_majors(self):
        majors = Major.get_all_for_dropdown()
        
        self.majorInput.clear()
        self.majorInput.addItem("No major assigned", None)
        
        for major in majors:
            display_text = f"{major['name']} ({major['degree_level']}) - {major['dept_name']}"
            self.majorInput.addItem(display_text, major['major_id'])
        
        logging.debug(f"Loaded {len(majors)} majors into dropdown")
    
    def _set_default_dates(self):
        today = QDate.currentDate()
        
        self.enrollmentDateInput.setDate(today)
        
        twenty_years_ago = today.addYears(-20)
        self.dateOfBirthInput.setDate(twenty_years_ago)
    
    def _load_student_data(self):
        student = Student.get_by_id_with_details(self.student_id)
        
        if not student:
            QMessageBox.critical(self, "Error", "Failed to load student data")
            self.reject()
            return
        
        self.firstNameInput.setText(student.get('first_name', ''))
        self.lastNameInput.setText(student.get('last_name', ''))
        self.peselInput.setText(student.get('pesel', ''))
        
        if student.get('date_of_birth'):
            dob = student['date_of_birth']
            self.dateOfBirthInput.setDate(QDate(dob.year, dob.month, dob.day))
        
        gender = student.get('gender')
        if gender:
            index = self.genderInput.findText(gender)
            if index >= 0:
                self.genderInput.setCurrentIndex(index)
        
        self.emailInput.setText(student.get('email', ''))
        self.phoneInput.setText(student.get('phone_number', '') or '')
        self.addressInput.setText(student.get('address', '') or '')
        
        enrollment_date = student.get('enrollment_date')
        if enrollment_date:
            self.enrollmentDateInput.setDate(QDate(enrollment_date.year, enrollment_date.month, enrollment_date.day))
        
        status = student.get('status', 'Active')
        index = self.statusInput.findText(status)
        if index >= 0:
            self.statusInput.setCurrentIndex(index)
        
        major_id = student.get('major_id')
        if major_id:
            for i in range(self.majorInput.count()):
                if self.majorInput.itemData(i) == major_id:
                    self.majorInput.setCurrentIndex(i)
                    break
        
        logging.debug(f"Loaded data for student {self.student_id}")
    
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
        
        enrollment_date = self.enrollmentDateInput.date().toPyDate()
        student_data = {
            'enrollment_date': enrollment_date,
            'status': self.statusInput.currentText()
        }
        
        major_id = self.majorInput.currentData()
        
        return person_data, student_data, major_id
    
    def _handle_save(self):
        self.errorLabel.setText("")
        
        is_valid, error_message = self._validate_form()
        
        if not is_valid:
            self.errorLabel.setText(error_message)
            return
        
        person_data, student_data, major_id = self._get_form_data()
        
        if self.student_id:
            success = Student.update_with_person(
                self.student_id,
                person_data,
                student_data,
                major_id
            )
            
            if success:
                logging.info(f"Updated student {self.student_id}")
                QMessageBox.information(self, "Success", "Student updated successfully!")
                self.accept()
            else:
                self.errorLabel.setText("Failed to update student. Please check the logs.")
                logging.error(f"Failed to update student {self.student_id}")
        else:
            student_id = Student.create_with_person(
                person_data,
                student_data,
                major_id
            )
            
            if student_id:
                logging.info(f"Created new student {student_id}")
                QMessageBox.information(self, "Success", "Student created successfully!")
                self.accept()
            else:
                self.errorLabel.setText("Failed to create student. Please check the logs.")
                logging.error("Failed to create new student")