import logging
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt6.QtCore import Qt
from app.settings import UI_MANAGE_MAJORS_DIALOG
from app.models.major import Major


class ManageMajorsDialog(QDialog):
    def __init__(self, dept_id: int, dept_name: str, parent=None):
        super().__init__(parent)
        
        uic.loadUi(UI_MANAGE_MAJORS_DIALOG, self)
        
        self.dept_id = dept_id
        self.dept_name = dept_name
        
        self.departmentLabel.setText(f"Department: {dept_name}")
        
        self._connect_signals()
        
        self._setup_table()
        
        self.load_majors()
        
        logging.debug(f"ManageMajorsDialog initialized for department {dept_id}")
    
    def _connect_signals(self):
        self.addMajorButton.clicked.connect(self._handle_add)
        self.editButton.clicked.connect(self._handle_edit)
        self.deleteButton.clicked.connect(self._handle_delete)
        self.majorsTable.itemSelectionChanged.connect(self._handle_selection_change)
        self.majorsTable.doubleClicked.connect(self._handle_edit)
        self.buttonBox.rejected.connect(self.accept)
    
    def _setup_table(self):
        header = self.majorsTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        self.majorsTable.setColumnHidden(0, True)
    
    def load_majors(self):
        from app.core.loading_utils import show_loading_cursor

        self.statusLabel.setText("Loading majors...")
        
        was_sorting = self.majorsTable.isSortingEnabled()
        sort_col = self.majorsTable.horizontalHeader().sortIndicatorSection()
        sort_order = self.majorsTable.horizontalHeader().sortIndicatorOrder()
        self.majorsTable.setSortingEnabled(False)
        
        majors_data = Major.get_by_department(self.dept_id)
        
        self.majorsTable.setRowCount(0)
        
        with show_loading_cursor():
            for major in majors_data:
                self._add_major_to_table(major)
        
        self.majorsTable.setSortingEnabled(was_sorting)
        if was_sorting:
            self.majorsTable.sortItems(sort_col, sort_order)
        
        count = len(majors_data)
        self.statusLabel.setText(f"Showing {count} major{'s' if count != 1 else ''}")
        
        logging.debug(f"Loaded {count} majors for department {self.dept_id}")
    
    def _add_major_to_table(self, major: dict):
        row = self.majorsTable.rowCount()
        self.majorsTable.insertRow(row)

        self.majorsTable.setItem(row, 0, QTableWidgetItem(str(major['major_id'])))        
        self.majorsTable.setItem(row, 1, QTableWidgetItem(major.get('name', '')))
        self.majorsTable.setItem(row, 2, QTableWidgetItem(major.get('degree_level', '')))
        
        student_count = str(major.get('student_count', 0))
        self.majorsTable.setItem(row, 3, QTableWidgetItem(student_count))
    
    def _handle_selection_change(self):
        has_selection = len(self.majorsTable.selectedItems()) > 0
        self.editButton.setEnabled(has_selection)
        self.deleteButton.setEnabled(has_selection)
    
    def _get_selected_major_id(self):
        selected_rows = self.majorsTable.selectionModel().selectedRows()
        
        if not selected_rows:
            return None
        
        row = selected_rows[0].row()
        major_id = int(self.majorsTable.item(row, 0).text())
        
        return major_id
    
    def _handle_add(self):
        from app.ui.dialogs.major_dialog import MajorDialog
        
        dialog = MajorDialog(
            dept_id=self.dept_id,
            dept_name=self.dept_name,
            parent=self
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_majors()
            logging.info("Major added, table refreshed")
    
    def _handle_edit(self):
        from app.ui.dialogs.major_dialog import MajorDialog
        
        major_id = self._get_selected_major_id()
        
        if not major_id:
            return
        
        dialog = MajorDialog(
            dept_id=self.dept_id,
            dept_name=self.dept_name,
            major_id=major_id,
            parent=self
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_majors()
            logging.info(f"Major {major_id} edited, table refreshed")
    
    def _handle_delete(self):
        from app.core.loading_utils import show_loading_cursor

        major_id = self._get_selected_major_id()
        
        if not major_id:
            return
        
        row = self.majorsTable.currentRow()
        major_name = self.majorsTable.item(row, 1).text()
        degree_level = self.majorsTable.item(row, 2).text()
        student_count = int(self.majorsTable.item(row, 3).text())
        
        warning = f"Are you sure you want to delete {major_name} ({degree_level})?\n\n"
        
        if student_count > 0:
            warning += f"WARNING: {student_count} student{'s are' if student_count != 1 else ' is'} enrolled in this major!\n"
            warning += "Their major assignments will be deleted.\n\n"
        
        warning += "This action cannot be undone!"
        
        reply = QMessageBox.question(
            self,
            "Delete Major",
            warning,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = Major.delete(major_id)
            
            with show_loading_cursor():
                if success:
                    logging.info(f"Deleted major {major_id} ({major_name})")
                    QMessageBox.information(self, "Success", f"Major {major_name} deleted successfully!")

                    self.load_majors()
                else:
                    logging.error(f"Failed to delete major {major_id}")
                    QMessageBox.critical(self, "Error", "Failed to delete major. Please check the logs.")