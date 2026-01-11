import os
from pathlib import Path

# ============================================================================
# APPLICATION CONFIGURATION
# ============================================================================

APP_TITLE = "CampusHub"

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
# NOTE: Only for local development, should be stored in .env in production!

DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "campushub"
DB_HOST = "localhost"
DB_PORT = "5432"

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "campushub.log"
LOG_LEVEL = "DEBUG"
LOG_FORMAT = "%(asctime)s %(filename)s [%(levelname)s] %(message)s"

# ============================================================================
# UI/BRANDING CONFIGURATION
# ============================================================================

LOGO_HORIZONTAL_DARK = "brand/campushub-high-resolution-logo-transparent.png"
LOGO_HORIZONTAL_LIGHT = "brand/campushub-high-resolution-logo-grayscale-transparent.png"
LOGO_ICON_DARK = "brand/campushub-icon-transparent.png"
LOGO_ICON_LIGHT = "brand/campushub-icon-grayscale-transparent.png"

LOGO_FALLBACK_TEXT = "CampusHub"

# ============================================================================
# UI FILE PATHS
# ============================================================================

UI_LOGIN = "app/ui/layout/login.ui"
UI_DASHBOARD = "app/ui/layout/dashboard.ui"
UI_STUDENTS_TAB = "app/ui/layout/students_tab.ui"
UI_DEPARTMENTS_TAB = "app/ui/layout/departments_tab.ui"
UI_EMPLOYEES_TAB = "app/ui/layout/employees_tab.ui"
UI_STUDENT_DIALOG = "app/ui/layout/student_dialog.ui"
UI_DEPARTMENT_DIALOG = "app/ui/layout/department_dialog.ui"
UI_EMPLOYEE_DIALOG = "app/ui/layout/employee_dialog.ui"
UI_ASSIGN_HEAD_DIALOG = "app/ui/layout/assign_head_dialog.ui"
UI_MAJOR_DIALOG = "app/ui/layout/major_dialog.ui"
UI_MANAGE_MAJORS_DIALOG = "app/ui/layout/manage_majors_dialog.ui"
