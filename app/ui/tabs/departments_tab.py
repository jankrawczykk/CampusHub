import logging
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog
from PyQt6.QtCore import Qt
from app.settings import UI_DEPARTMENTS_TAB
from app.models.department import Department


class DepartmentsTab(QWidget):
    
    def __init__(self):
        super().__init__()
        
        uic.loadUi(UI_DEPARTMENTS_TAB, self)
        
        self._connect_signals()
        
        self._setup_table()
        
        self.load_departments()
        
        logging.debug("DepartmentsTab initialized")
    
    def _connect_signals(self):
        self.searchButton.clicked.connect(self._handle_search)
        self.searchInput.returnPressed.connect(self._handle_search)
        self.refreshButton.clicked.connect(self.load_departments)
        self.addButton.clicked.connect(self._handle_add)
        self.editButton.clicked.connect(self._handle_edit)
        self.deleteButton.clicked.connect(self._handle_delete)
        self.departmentsTable.itemSelectionChanged.connect(self._handle_selection_change)
        self.departmentsTable.doubleClicked.connect(self._handle_edit)
        self.assignHeadButton.clicked.connect(self._handle_assign_head)
        self.manageMajorsButton.clicked.connect(self._handle_manage_majors)
    
    def _setup_table(self):
        header = self.departmentsTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        self.departmentsTable.setColumnHidden(0, True)
    
    def load_departments(self, departments_data=None):
        from app.core.loading_utils import show_loading_cursor
        
        self.statusLabel.setText("Loading departments...")
        
        was_sorting = self.departmentsTable.isSortingEnabled()
        sort_col = self.departmentsTable.horizontalHeader().sortIndicatorSection()
        sort_order = self.departmentsTable.horizontalHeader().sortIndicatorOrder()
        self.departmentsTable.setSortingEnabled(False)
        
        with show_loading_cursor():
            if departments_data is None or departments_data is False:
                departments_data = Department.get_all_with_details()
        
        if not isinstance(departments_data, list):
            self.departmentsTable.setRowCount(0)
            self.statusLabel.setText("Error loading departments - check database connection")
            logging.error("Failed to load departments - invalid data returned")
            return
        
        self.departmentsTable.setRowCount(0)
        
        for department in departments_data:
            self._add_department_to_table(department)
        
        self.departmentsTable.setSortingEnabled(was_sorting)
        if was_sorting:
            self.departmentsTable.sortItems(sort_col, sort_order)
        
        count = len(departments_data)
        self.statusLabel.setText(f"Showing {count} department{'s' if count != 1 else ''}")
        
        logging.debug(f"Loaded {count} departments into table")
    
    def _add_department_to_table(self, department: dict):
        row = self.departmentsTable.rowCount()
        self.departmentsTable.insertRow(row)
        
        self.departmentsTable.setItem(row, 0, QTableWidgetItem(str(department['dept_id'])))
        self.departmentsTable.setItem(row, 1, QTableWidgetItem(department.get('name', '')))
        self.departmentsTable.setItem(row, 2, QTableWidgetItem(department.get('code', '')))
        
        head_name = department.get('head_name', 'No head assigned')
        self.departmentsTable.setItem(row, 3, QTableWidgetItem(head_name or 'No head assigned'))
        
        head_since = department.get('head_since', '')
        if head_since:
            head_since = str(head_since)
        self.departmentsTable.setItem(row, 4, QTableWidgetItem(head_since))
    
    def _handle_search(self):
        from app.core.loading_utils import show_loading_cursor
        
        search_term = self.searchInput.text().strip()
        
        if not search_term:
            self.load_departments()
            return
        
        self.statusLabel.setText(f"Searching for '{search_term}'...")
        
        with show_loading_cursor():
            results = Department.search_departments(search_term)
        
        self.load_departments(results)
        
        if not results:
            self.statusLabel.setText(f"No departments found matching '{search_term}'")
    
    def _handle_selection_change(self):
        has_selection = len(self.departmentsTable.selectedItems()) > 0
        self.editButton.setEnabled(has_selection)
        self.deleteButton.setEnabled(has_selection)
        self.assignHeadButton.setEnabled(has_selection)
        self.manageMajorsButton.setEnabled(has_selection)  
    
    def _get_selected_department_id(self):
        selected_rows = self.departmentsTable.selectionModel().selectedRows()
        
        if not selected_rows:
            return None
        
        row = selected_rows[0].row()
        dept_id = int(self.departmentsTable.item(row, 0).text())
        
        return dept_id
    
    def _handle_add(self):
        from app.ui.dialogs.department_dialog import DepartmentDialog
        
        dialog = DepartmentDialog(parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_departments()
            logging.info("Department added, table refreshed")
    
    def _handle_edit(self):
        from app.ui.dialogs.department_dialog import DepartmentDialog
        
        dept_id = self._get_selected_department_id()
        
        if not dept_id:
            return
        
        dialog = DepartmentDialog(dept_id=dept_id, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_departments()
            logging.info(f"Department {dept_id} edited, table refreshed")
    
    def _handle_delete(self):
        from app.core.loading_utils import show_loading_cursor
        
        dept_id = self._get_selected_department_id()
        
        if not dept_id:
            return
        
        row = self.departmentsTable.currentRow()
        dept_name = self.departmentsTable.item(row, 1).text()
        dept_code = self.departmentsTable.item(row, 2).text()
        
        reply = QMessageBox.question(
            self,
            "Delete Department",
            f"Are you sure you want to delete {dept_name} ({dept_code})?\n\n"
            f"This will permanently delete:\n"
            f"- Department record\n"
            f"- All associated courses\n"
            f"- All associated majors\n\n"
            f"This action cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            with show_loading_cursor():
                success = Department.delete(dept_id)
            
            if success:
                logging.info(f"Deleted department {dept_id} ({dept_name})")
                QMessageBox.information(self, "Success", f"Department {dept_name} deleted successfully!")
                self.load_departments()
            else:
                logging.error(f"Failed to delete department {dept_id}")
                QMessageBox.critical(self, "Error", "Failed to delete department. Please check the logs.")
    
    def _handle_assign_head(self):
        from app.ui.dialogs.assign_head_dialog import AssignHeadDialog
        
        dept_id = self._get_selected_department_id()
        
        if not dept_id:
            return
        
        row = self.departmentsTable.currentRow()
        dept_name = self.departmentsTable.item(row, 1).text()
        
        dialog = AssignHeadDialog(dept_id=dept_id, dept_name=dept_name, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_departments()
            logging.info(f"Department head updated, table refreshed")

    def _handle_manage_majors(self):
        from app.ui.dialogs.manage_majors_dialog import ManageMajorsDialog

        dept_id = self._get_selected_department_id()

        if not dept_id:
            return

        row = self.departmentsTable.currentRow()
        dept_name = self.departmentsTable.item(row, 1).text()

        dialog = ManageMajorsDialog(dept_id=dept_id, dept_name=dept_name, parent=self)
        dialog.exec()