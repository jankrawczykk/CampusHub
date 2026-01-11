import logging
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QMessageBox
from app.core.loading_utils import show_loading_cursor
from app.settings import UI_COURSE_DIALOG
from app.models.course import Course
from app.models.department import Department


class CourseDialog(QDialog):
    def __init__(self, course_id: int = None, parent=None):
        super().__init__(parent)
        
        uic.loadUi(UI_COURSE_DIALOG, self)
        
        self.course_id = course_id
        
        if self.course_id:
            self.setWindowTitle("Edit Course")
            self.titleLabel.setText('<html><head/><body><p><span style="font-size:18pt; font-weight:600;">Edit Course</span></p></body></html>')
        else:
            self.setWindowTitle("Add Course")
            self.titleLabel.setText('<html><head/><body><p><span style="font-size:18pt; font-weight:600;">Add New Course</span></p></body></html>')
        
        self._load_departments()
        
        if self.course_id:
            self._load_course_data()
        
        self.buttonBox.accepted.connect(self._handle_save)
        self.buttonBox.rejected.connect(self.reject)
        
        logging.debug(f"CourseDialog initialized (course_id: {course_id})")
    
    def _load_departments(self):
        """Load departments into dropdown"""
        departments = Department.get_all_for_dropdown()
        
        if not departments:
            QMessageBox.warning(self, "Warning", "No departments found. Please create departments first.")
            return
        
        for dept in departments:
            self.departmentCombo.addItem(dept['name'], dept['dept_id'])
        
        logging.debug("Loaded departments into dropdown")
    
    def _load_course_data(self):
        course = Course.get_by_id(self.course_id)
        
        if not course:
            QMessageBox.critical(self, "Error", "Failed to load course data")
            self.reject()
            return
        
        self.courseCodeInput.setText(course.get('course_code', ''))
        self.titleInput.setText(course.get('title', ''))
        self.creditsInput.setValue(course.get('credits', 3))
        self.descriptionInput.setPlainText(course.get('description', '') or '')
        
        # Set department dropdown
        dept_id = course.get('dept_id')
        index = self.departmentCombo.findData(dept_id)
        if index >= 0:
            self.departmentCombo.setCurrentIndex(index)
        
        logging.debug(f"Loaded data for course {self.course_id}")
    
    def _validate_form(self) -> tuple[bool, str]:
        course_code = self.courseCodeInput.text().strip()
        title = self.titleInput.text().strip()
        
        if not course_code:
            return False, "Course code is required"
        
        if not title:
            return False, "Course title is required"
        
        if not course_code.replace(' ', '').isalnum():
            return False, "Course code should contain only letters and numbers"
        
        if self.creditsInput.value() < 1:
            return False, "Credits must be at least 1"
        
        # Check if course code is unique (excluding current course if editing)
        if Course.check_course_code_exists(course_code, exclude_course_id=self.course_id):
            return False, "This course code already exists"
        
        return True, ""
    
    def _get_form_data(self) -> dict:
        return {
            'course_code': self.courseCodeInput.text().strip().upper(),
            'title': self.titleInput.text().strip(),
            'dept_id': self.departmentCombo.currentData(),
            'credits': self.creditsInput.value(),
            'description': self.descriptionInput.toPlainText().strip() or None
        }
    
    def _handle_save(self):
        self.errorLabel.setText("")
        
        is_valid, error_message = self._validate_form()
        
        if not is_valid:
            self.errorLabel.setText(error_message)
            return
        
        course_data = self._get_form_data()
        
        with show_loading_cursor():
            if self.course_id:
                success = Course.update(self.course_id, course_data)

                if success:
                    logging.info(f"Updated course {self.course_id}")
                    QMessageBox.information(self, "Success", "Course updated successfully!")
                    self.accept()
                else:
                    self.errorLabel.setText("Failed to update course. Please check the logs.")
                    logging.error(f"Failed to update course {self.course_id}")
            else:
                course_id = Course.create(course_data)

                if course_id:
                    logging.info(f"Created new course {course_id}")
                    QMessageBox.information(self, "Success", "Course created successfully!")
                    self.accept()
                else:
                    self.errorLabel.setText("Failed to create course. Please check the logs.")
                    logging.error("Failed to create new course")
