import logging
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog
from PyQt6.QtCore import Qt
from app.settings import UI_EMPLOYEES_TAB
from app.core.loading_utils import show_loading_cursor
from app.models.employee import Employee


class EmployeesTab(QWidget):
    def __init__(self):
        super().__init__()
        
        uic.loadUi(UI_EMPLOYEES_TAB, self)
        
        self._connect_signals()
        
        self._setup_table()
        
        self.load_employees()
        
        logging.debug("EmployeesTab initialized")
    
    def _connect_signals(self):
        self.searchButton.clicked.connect(self._handle_search)
        self.searchInput.returnPressed.connect(self._handle_search)
        self.refreshButton.clicked.connect(self.load_employees)
        self.addButton.clicked.connect(self._handle_add)
        self.editButton.clicked.connect(self._handle_edit)
        self.deleteButton.clicked.connect(self._handle_delete)
        self.employeesTable.itemSelectionChanged.connect(self._handle_selection_change)
        self.employeesTable.doubleClicked.connect(self._handle_edit)
    
    def _setup_table(self):
        header = self.employeesTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
        
        self.employeesTable.setColumnHidden(0, True)
    
    def load_employees(self, employees_data=None):
        from app.core.loading_utils import show_loading_cursor

        self.statusLabel.setText("Loading employees...")

        was_sorting = self.employeesTable.isSortingEnabled()
        sort_col = self.employeesTable.horizontalHeader().sortIndicatorSection()
        sort_order = self.employeesTable.horizontalHeader().sortIndicatorOrder()
        self.employeesTable.setSortingEnabled(False)

        with show_loading_cursor():
            if employees_data is None or employees_data is False:
                employees_data = Employee.get_all_with_details()
        
        if not isinstance(employees_data, list):
            self.employeesTable.setRowCount(0)
            self.statusLabel.setText("Error loading employees - check database connection")
            logging.error("Failed to load employees - invalid data returned")
            return
        
        self.employeesTable.setRowCount(0)
        
        for employee in employees_data:
            self._add_employee_to_table(employee)
        
        self.employeesTable.setSortingEnabled(was_sorting)
        if was_sorting:
            self.employeesTable.sortItems(sort_col, sort_order)
        
        count = len(employees_data)
        self.statusLabel.setText(f"Showing {count} employee{'s' if count != 1 else ''}")
        
        logging.debug(f"Loaded {count} employees into table")
    
    def _add_employee_to_table(self, employee: dict):
        row = self.employeesTable.rowCount()
        self.employeesTable.insertRow(row)
        
        self.employeesTable.setItem(row, 0, QTableWidgetItem(str(employee['employee_id'])))
        self.employeesTable.setItem(row, 1, QTableWidgetItem(employee.get('first_name', '')))
        self.employeesTable.setItem(row, 2, QTableWidgetItem(employee.get('last_name', '')))
        self.employeesTable.setItem(row, 3, QTableWidgetItem(employee.get('email', '')))
        
        phone = employee.get('phone_number', '') or ''
        self.employeesTable.setItem(row, 4, QTableWidgetItem(phone))
        
        position = employee.get('position_name', 'No position assigned')
        self.employeesTable.setItem(row, 5, QTableWidgetItem(position or 'No position assigned'))
        
        status = employee.get('status', '')
        status_item = QTableWidgetItem(status)
        
        if status == 'Active':
            status_item.setForeground(Qt.GlobalColor.darkGreen)
        elif status == 'Inactive':
            status_item.setForeground(Qt.GlobalColor.darkYellow)
        elif status == 'Suspended':
            status_item.setForeground(Qt.GlobalColor.red)
        
        self.employeesTable.setItem(row, 6, status_item)
        
        employment_date = employee.get('employment_date', '')
        if employment_date:
            employment_date = str(employment_date)
        self.employeesTable.setItem(row, 7, QTableWidgetItem(employment_date))
    
    def _handle_search(self):
        search_term = self.searchInput.text().strip()
        
        if not search_term:
            self.load_employees()
            return
        
        self.statusLabel.setText(f"Searching for '{search_term}'...")
        
        with show_loading_cursor():
            results = Employee.search_employees(search_term)
        
        self.load_employees(results)
        
        if not results:
            self.statusLabel.setText(f"No employees found matching '{search_term}'")

    def _handle_selection_change(self):
        has_selection = len(self.employeesTable.selectedItems()) > 0
        self.editButton.setEnabled(has_selection)
        self.deleteButton.setEnabled(has_selection)

    def _get_selected_employee_id(self):
        selected_rows = self.employeesTable.selectionModel().selectedRows()
        
        if not selected_rows:
            return None
        
        row = selected_rows[0].row()
        employee_id = int(self.employeesTable.item(row, 0).text())
        
        return employee_id

    def _handle_add(self):
        from app.ui.dialogs.employee_dialog import EmployeeDialog
        
        dialog = EmployeeDialog(parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_employees()
            logging.info("Employee added, table refreshed")

    def _handle_edit(self):
        from app.ui.dialogs.employee_dialog import EmployeeDialog
        
        employee_id = self._get_selected_employee_id()
        
        if not employee_id:
            return
        
        dialog = EmployeeDialog(employee_id=employee_id, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_employees()
            logging.info(f"Employee {employee_id} edited, table refreshed")

    def _handle_delete(self):
        from app.core.loading_utils import show_loading_cursor
        
        employee_id = self._get_selected_employee_id()
        
        if not employee_id:
            return
        
        row = self.employeesTable.currentRow()
        first_name = self.employeesTable.item(row, 1).text()
        last_name = self.employeesTable.item(row, 2).text()
        
        reply = QMessageBox.question(
            self,
            "Delete Employee",
            f"Are you sure you want to delete {first_name} {last_name}?\n\n"
            f"This will permanently delete:\n"
            f"- Employee record\n"
            f"- Person record\n"
            f"- All position assignments\n"
            f"- User account (if exists)\n\n"
            f"This action cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            with show_loading_cursor():
                success = Employee.delete(employee_id)
            
            if success:
                logging.info(f"Deleted employee {employee_id} ({first_name} {last_name})")
                QMessageBox.information(self, "Success", f"Employee {first_name} {last_name} deleted successfully!")
                
                self.load_employees()
            else:
                logging.error(f"Failed to delete employee {employee_id}")
                QMessageBox.critical(self, "Error", "Failed to delete employee. Please check the logs.")