import logging
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from app.core.loading_utils import show_loading_cursor
from app.models.employee import Employee


class EmployeesTab(QWidget):
    def __init__(self):
        super().__init__()
        
        uic.loadUi("app/ui/layout/employees_tab.ui", self)
        
        self._connect_signals()
        
        self._setup_table()
        
        self.load_employees()
        
        logging.debug("EmployeesTab initialized")
    
    def _connect_signals(self):
        self.searchButton.clicked.connect(self._handle_search)
        self.searchInput.returnPressed.connect(self._handle_search)
        self.refreshButton.clicked.connect(self.load_employees)
    
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