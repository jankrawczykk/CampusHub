import logging
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog
from PyQt6.QtCore import Qt
from app.settings import UI_COURSES_TAB
from app.models.course import Course


class CoursesTab(QWidget):
    
    def __init__(self):
        super().__init__()
        
        uic.loadUi(UI_COURSES_TAB, self)
        
        self._connect_signals()
        
        self._setup_table()
        
        self.load_courses()
        
        logging.debug("CoursesTab initialized")
    
    def _connect_signals(self):
        self.searchButton.clicked.connect(self._handle_search)
        self.searchInput.returnPressed.connect(self._handle_search)
        self.refreshButton.clicked.connect(self.load_courses)
        self.addButton.clicked.connect(self._handle_add)
        self.editButton.clicked.connect(self._handle_edit)
        self.deleteButton.clicked.connect(self._handle_delete)
        self.coursesTable.itemSelectionChanged.connect(self._handle_selection_change)
        self.coursesTable.doubleClicked.connect(self._handle_edit)
    
    def _setup_table(self):
        header = self.coursesTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        
        self.coursesTable.setColumnHidden(0, True)
    
    def load_courses(self, courses_data=None):
        from app.core.loading_utils import show_loading_cursor
        
        self.statusLabel.setText("Loading courses...")
        
        was_sorting = self.coursesTable.isSortingEnabled()
        sort_col = self.coursesTable.horizontalHeader().sortIndicatorSection()
        sort_order = self.coursesTable.horizontalHeader().sortIndicatorOrder()
        self.coursesTable.setSortingEnabled(False)
        
        with show_loading_cursor():
            if courses_data is None or courses_data is False:
                courses_data = Course.get_all_with_details()
        
        if not isinstance(courses_data, list):
            self.coursesTable.setRowCount(0)
            self.statusLabel.setText("Error loading courses - check database connection")
            logging.error("Failed to load courses - invalid data returned")
            return
        
        self.coursesTable.setRowCount(0)
        
        for course in courses_data:
            self._add_course_to_table(course)
        
        self.coursesTable.setSortingEnabled(was_sorting)
        if was_sorting:
            self.coursesTable.sortItems(sort_col, sort_order)
        
        count = len(courses_data)
        self.statusLabel.setText(f"Showing {count} course{'s' if count != 1 else ''}")
        
        logging.debug(f"Loaded {count} courses into table")
    
    def _add_course_to_table(self, course: dict):
        row = self.coursesTable.rowCount()
        self.coursesTable.insertRow(row)
        
        self.coursesTable.setItem(row, 0, QTableWidgetItem(str(course['course_id'])))
        self.coursesTable.setItem(row, 1, QTableWidgetItem(course.get('course_code', '')))
        self.coursesTable.setItem(row, 2, QTableWidgetItem(course.get('title', '')))
        self.coursesTable.setItem(row, 3, QTableWidgetItem(course.get('department_name', '')))
        self.coursesTable.setItem(row, 4, QTableWidgetItem(str(course.get('credits', ''))))
        self.coursesTable.setItem(row, 5, QTableWidgetItem(course.get('description', '') or ''))
    
    def _handle_search(self):
        from app.core.loading_utils import show_loading_cursor
        
        search_term = self.searchInput.text().strip()
        
        if not search_term:
            self.load_courses()
            return
        
        self.statusLabel.setText(f"Searching for '{search_term}'...")
        
        with show_loading_cursor():
            results = Course.search_courses(search_term)
        
        self.load_courses(results)
        
        if not results:
            self.statusLabel.setText(f"No courses found matching '{search_term}'")
    
    def _handle_selection_change(self):
        has_selection = len(self.coursesTable.selectedItems()) > 0
        self.editButton.setEnabled(has_selection)
        self.deleteButton.setEnabled(has_selection)
    
    def _get_selected_course_id(self):
        selected_rows = self.coursesTable.selectionModel().selectedRows()
        
        if not selected_rows:
            return None
        
        row = selected_rows[0].row()
        course_id = int(self.coursesTable.item(row, 0).text())
        
        return course_id
    
    def _handle_add(self):
        from app.ui.dialogs.course_dialog import CourseDialog
        
        dialog = CourseDialog(parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_courses()
            logging.info("Course added, table refreshed")
    
    def _handle_edit(self):
        from app.ui.dialogs.course_dialog import CourseDialog
        
        course_id = self._get_selected_course_id()
        
        if not course_id:
            return
        
        dialog = CourseDialog(course_id=course_id, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_courses()
            logging.info(f"Course {course_id} edited, table refreshed")
    
    def _handle_delete(self):
        from app.core.loading_utils import show_loading_cursor
        
        course_id = self._get_selected_course_id()
        
        if not course_id:
            return
        
        row = self.coursesTable.currentRow()
        course_code = self.coursesTable.item(row, 1).text()
        title = self.coursesTable.item(row, 2).text()
        
        reply = QMessageBox.question(
            self,
            "Delete Course",
            f"Are you sure you want to delete {course_code}?\n\n"
            f"Course: {title}\n\n"
            f"This action cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            with show_loading_cursor():
                success = Course.delete(course_id)
            
            if success:
                logging.info(f"Deleted course {course_id} ({course_code})")
                QMessageBox.information(self, "Success", f"Course {course_code} deleted successfully!")
                
                self.load_courses()
            else:
                logging.error(f"Failed to delete course {course_id}")
                QMessageBox.critical(self, "Error", "Failed to delete course. Please check the logs.")
