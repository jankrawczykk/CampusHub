import logging
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QMessageBox
from app.settings import UI_MAJOR_DIALOG
from app.models.major import Major


class MajorDialog(QDialog):
    def __init__(self, dept_id: int, dept_name: str, major_id: int = None, parent=None):
        super().__init__(parent)
        
        uic.loadUi(UI_MAJOR_DIALOG, self)
        
        self.dept_id = dept_id
        self.dept_name = dept_name
        self.major_id = major_id
        
        self.departmentLabel.setText(f"Department: {dept_name}")
        
        if self.major_id:
            self.setWindowTitle("Edit Major")
            self.titleLabel.setText('<html><head/><body><p><span style="font-size:18pt; font-weight:600;">Edit Major</span></p></body></html>')
            self._load_major_data()
        else:
            self.setWindowTitle("Add Major")
            self.titleLabel.setText('<html><head/><body><p><span style="font-size:18pt; font-weight:600;">Add New Major</span></p></body></html>')
        
        self.buttonBox.accepted.connect(self._handle_save)
        self.buttonBox.rejected.connect(self.reject)
        
        logging.debug(f"MajorDialog initialized (dept_id: {dept_id}, major_id: {major_id})")
    
    def _load_major_data(self):
        major = Major.get_by_id(self.major_id)
        
        if not major:
            QMessageBox.critical(self, "Error", "Failed to load major data")
            self.reject()
            return
        
        self.nameInput.setText(major.get('name', ''))
        
        degree_level = major.get('degree_level')
        if degree_level:
            index = self.degreeLevelInput.findText(degree_level)
            if index >= 0:
                self.degreeLevelInput.setCurrentIndex(index)
        
        logging.debug(f"Loaded data for major {self.major_id}")
    
    def _validate_form(self) -> tuple[bool, str]:
        if not self.nameInput.text().strip():
            return False, "Major name is required"
        
        if self.degreeLevelInput.currentIndex() == 0:
            return False, "Please select a degree level"
        
        return True, ""
    
    def _get_form_data(self) -> dict:
        return {
            'dept_id': self.dept_id,
            'name': self.nameInput.text().strip(),
            'degree_level': self.degreeLevelInput.currentText()
        }
    
    def _handle_save(self):
        from app.core.loading_utils import show_loading_cursor

        self.errorLabel.setText("")
        
        is_valid, error_message = self._validate_form()
        
        if not is_valid:
            self.errorLabel.setText(error_message)
            return
        
        major_data = self._get_form_data()
        
        with show_loading_cursor():
            if self.major_id:
                success = Major.update(self.major_id, major_data)

                if success:
                    logging.info(f"Updated major {self.major_id}")
                    QMessageBox.information(self, "Success", "Major updated successfully!")
                    self.accept()
                else:
                    self.errorLabel.setText("Failed to update major. Please check the logs.")
                    logging.error(f"Failed to update major {self.major_id}")
            else:
                major_id = Major.create(major_data)

                if major_id:
                    logging.info(f"Created new major {major_id}")
                    QMessageBox.information(self, "Success", "Major created successfully!")
                    self.accept()
                else:
                    self.errorLabel.setText("Failed to create major. Please check the logs.")
                    logging.error("Failed to create new major")