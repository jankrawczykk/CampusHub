import logging
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog
from PyQt6.QtCore import Qt
from app.models.student import Student


class StudentsTab(QWidget):
    def __init__(self):
        super().__init__()
        
        uic.loadUi("app/ui/layout/students_tab.ui", self)
        
        self._connect_signals()
        
        self._setup_table()
        
        self.load_students()
        
        logging.debug("StudentsTab initialized")
    
    def _connect_signals(self):
        self.searchButton.clicked.connect(self._handle_search)
        self.searchInput.returnPressed.connect(self._handle_search)
        self.refreshButton.clicked.connect(self.load_students)
        self.addButton.clicked.connect(self._handle_add)
        self.editButton.clicked.connect(self._handle_edit)
        self.deleteButton.clicked.connect(self._handle_delete)
        
        self.studentsTable.itemSelectionChanged.connect(self._handle_selection_change)
        
        self.studentsTable.doubleClicked.connect(self._handle_edit)
    
    def _setup_table(self):
        header = self.studentsTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
        
        self.studentsTable.setColumnHidden(0, True)
    
    def load_students(self, students_data=None):
        self.statusLabel.setText("Loading students...")

        if students_data is None or students_data is False:
            students_data = Student.get_all_with_details()

        if not isinstance(students_data, list):
            self.studentsTable.setRowCount(0)
            self.statusLabel.setText("Error loading students - check database connection")
            logging.error("Failed to load students - invalid data returned")
            logging.debug(f"Students data: {students_data}")
            return

        self.studentsTable.setRowCount(0)

        for student in students_data:
            self._add_student_to_table(student)

        count = len(students_data)
        self.statusLabel.setText(f"Showing {count} student{'s' if count != 1 else ''}")

        logging.debug(f"Loaded {count} students into table")
    
    def _add_student_to_table(self, student: dict):
        row = self.studentsTable.rowCount()
        self.studentsTable.insertRow(row)
        
        self.studentsTable.setItem(row, 0, QTableWidgetItem(str(student['student_id'])))
        self.studentsTable.setItem(row, 1, QTableWidgetItem(student.get('first_name', '')))
        self.studentsTable.setItem(row, 2, QTableWidgetItem(student.get('last_name', '')))
        self.studentsTable.setItem(row, 3, QTableWidgetItem(student.get('email', '')))
        self.studentsTable.setItem(row, 4, QTableWidgetItem(student.get('pesel', '')))
        self.studentsTable.setItem(row, 5, QTableWidgetItem(student.get('status', '')))
        
        major = student.get('major_name', 'No major')
        if student.get('degree_level'):
            major += f" ({student['degree_level']})"
        self.studentsTable.setItem(row, 6, QTableWidgetItem(major))
        
        enrollment_date = student.get('enrollment_date', '')
        if enrollment_date:
            enrollment_date = str(enrollment_date)
        self.studentsTable.setItem(row, 7, QTableWidgetItem(enrollment_date))
    
    def _handle_search(self):
        search_term = self.searchInput.text().strip()
        
        if not search_term:
            self.load_students()
            return
        
        self.statusLabel.setText(f"Searching for '{search_term}'...")
        
        results = Student.search_students(search_term)
        
        self.load_students(results)
        
        if not results:
            self.statusLabel.setText(f"No students found matching '{search_term}'")
    
    def _handle_selection_change(self):
        has_selection = len(self.studentsTable.selectedItems()) > 0
        self.editButton.setEnabled(has_selection)
        self.deleteButton.setEnabled(has_selection)
    
    def _get_selected_student_id(self):
        selected_rows = self.studentsTable.selectionModel().selectedRows()
        
        if not selected_rows:
            return None
        
        row = selected_rows[0].row()
        student_id = int(self.studentsTable.item(row, 0).text())
        
        return student_id
    
    def _handle_add(self):
        from app.ui.dialogs.student_dialog import StudentDialog

        dialog = StudentDialog(parent=self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_students()
            logging.info("Student added, table refreshed")

    def _handle_edit(self):
        from app.ui.dialogs.student_dialog import StudentDialog

        student_id = self._get_selected_student_id()

        if not student_id:
            return

        dialog = StudentDialog(student_id=student_id, parent=self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_students()
            logging.info(f"Student {student_id} edited, table refreshed")
    
    def _handle_delete(self):
        student_id = self._get_selected_student_id()
        
        if not student_id:
            return
        
        QMessageBox.information(
            self,
            "Delete Student",
            f"Delete functionality for student ID {student_id} will be implemented in Day 5!"
        )
        logging.info(f"Delete student {student_id} clicked (not yet implemented)")