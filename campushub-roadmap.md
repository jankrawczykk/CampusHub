# CampusHub 7-Day Development Roadmap

**Total Time:** 14-21 hours (2-3 hours per day)
**Start Date:** January 8, 2026
**Deadline:** January 15, 2026

---

## 📊 Project Scope

### PHASE 1 - Core (Must Have) ⭐
- [x] Login System
- [ ] Students Management (full CRUD + majors)
- [ ] Departments Management (simple CRUD)
- [ ] Dashboard Navigation

### PHASE 2 - Extended (If Time Permits)
- [ ] Employees Management (full CRUD + positions)
- [ ] Courses Management (full CRUD)

### PHASE 3 - Polish (Nice to Have)
- [ ] Users Management (admin accounts)
- [ ] Advanced search/filtering

---

## Day 1 - Foundation & Login (2-3 hours)

**Goal:** Working login that opens dashboard

### Tasks
- [x] Create `app/core/auth.py` for password verification
- [x] Wire up login button to authenticate users
- [x] Create `app/ui/dashboard_window.py` class
- [x] Implement window switching (login → dashboard)
- [x] Add logout functionality
- [x] Test login with existing users from database

**Deliverable:** ✓ Working login that opens dashboard

---

## Day 2 - Dashboard Layout & Database Models (2-3 hours)

**Goal:** Dashboard with tabs + working models

### Tasks
- [x] Design dashboard UI in Qt Designer (tabs for each entity)
- [x] Create `app/core/base_model.py` (reusable CRUD base class)
- [x] Create `app/models/student.py` (Student model)
- [x] Create `app/models/department.py` (Department model)
- [x] Test models with simple queries in Python console
- [x] Update dashboard_window.py to load tabs

**Deliverable:** ✓ Dashboard with tabs + working models

---

## Day 3 - Students Table View (2-3 hours)

**Goal:** Students display with search

### Tasks
- [x] Create students tab UI in Qt Designer
- [x] Create `app/ui/tabs/students_tab.py`
- [x] Load students data into QTableWidget
- [x] Add search box functionality
- [x] Style the table (modern look)
- [x] Add refresh button
- [x] Test with dummy data

**Deliverable:** ✓ Students display with search

---

## Day 4 - Students CRUD - Part 1 (2-3 hours)

**Goal:** Can add and edit students

### Tasks
- [x] Create add/edit student dialog UI in Qt Designer
- [x] Create `app/ui/dialogs/student_dialog.py`
- [x] Implement form validation (required fields, valid PESEL, etc.)
- [x] Wire up "Add Student" button
- [x] Wire up "Edit Student" button (double-click row or edit button)
- [x] Test adding new students
- [x] Test editing existing students

**Deliverable:** ✓ Can add and edit students

---

## Day 5 - Students CRUD - Part 2 & Departments (2-3 hours)

**Goal:** Students fully working + Departments basic CRUD

### Tasks
- [x] Implement delete student (with confirmation dialog)
- [x] Handle student-major relationship in add/edit dialog
- [x] Test complete student workflow (add, edit, delete, search)
- [x] Create departments tab UI (reuse student pattern)
- [x] Implement departments CRUD (simpler than students)
- [x] Test departments workflow

**Deliverable:** ✓ Students fully working + Departments basic CRUD

---

## Day 6 - Polish & Employees (2-3 hours)

**Goal:** Polished, bug-free core features

### Tasks
- [x] Add loading indicators for database operations
- [ ] Improve error messages (user-friendly)
- [x] Assigning and unassigng heads of departments
- [x] Fix any bugs found during testing
- [x] Add input validation feedback (red borders, tooltips)
- [x] Start employees management (copy student pattern)
- [x] Implement employees tab
- [ ] Managing 'users' with the employees tab -> Start of work for CRUD for users, we will finish in Day 7
- [x] Major CRUD (could be in the 'Departments' tab -> editing, adding, deleting majors and assigning them to departments. We can do it by showing the assigned majors for each department and control it that way). It was mentioned in the 'Bonus Features' - we have time for it so we will be doing that

**Deliverable:** ✓ Polished, bug-free core features

---

## Day 7 - Final Polish & Testing (2-3 hours)

**Goal:** Production-ready app for submission

### Tasks
- [ ] End-to-end testing of all features
- [ ] Fix any remaining bugs
- [ ] Finish 'users' CRUD fully
- [ ] Add finishing touches (icons, colors, spacing)
- [ ] Test on fresh database with dummy data
- [ ] Practice demo presentation
- [ ] Test worst-case scenarios (empty fields, invalid data)

**Deliverable:** ✓ Production-ready app for submission

---

## 🏗️ Project Architecture

```
app/
├── __init__.py
├── settings.py              # Application settings
├── core/
│   ├── auth.py              # Password verification
│   ├── base_model.py        # Reusable CRUD base class
│   ├── database_connection.py # Database connection
│   ├── logging_config.py    # Logging configuration
│   ├── loading_utils.py     # Loading indicator helpers
│   ├── theme_utils.py       # UI theming utilities
│   └── window_utils.py      # Window utilities
├── models/
│   ├── student.py           # ✓ Student database operations
│   ├── department.py        # ✓ Department database operations
│   ├── major.py             # ✓ Major database operations
│   └── employee.py          # ✓ Employee database operations
├── ui/
│   ├── dashboard_window.py  # Dashboard window
│   ├── login_window.py      # Login window
│   ├── tabs/                # ✓ Tab widgets
│   │   ├── students_tab.py  # ✓ Students table view with search
│   │   ├── departments_tab.py # ✓ Departments table view
│   │   └── employees_tab.py  # ✓ Employees table view
│   ├── dialogs/             # ✓ Dialog windows
│   │   ├── student_dialog.py # ✓ Add/edit student dialog
│   │   ├── department_dialog.py # ✓ Add/edit department dialog
│   │   ├── assign_head_dialog.py # ✓ Assign department head dialog
│   │   ├── major_dialog.py   # ✓ Add/edit major dialog
│   │   └── manage_majors_dialog.py # ✓ Manage majors dialog
│   └── layout/              # Qt Designer .ui files
│       ├── dashboard.ui
│       ├── login.ui
│       ├── students_tab.ui
│       ├── departments_tab.ui
│       ├── employees_tab.ui
│       ├── student_dialog.ui
│       ├── department_dialog.ui
│       ├── assign_head_dialog.ui
│       ├── major_dialog.ui
│       └── manage_majors_dialog.ui
```

---

## 🎨 UI Style Guide (Modern/Minimalist)

- **Colors:** Soft grays, white backgrounds, accent color (blue/green)
- **Typography:** Clean, readable fonts (11-12pt)
- **Spacing:** Generous padding (16-24px)
- **Tables:** Alternating row colors, hover effects
- **Buttons:** Rounded corners, subtle shadows
- **Forms:** Clear labels, proper alignment

---

## ✅ Minimum Success Criteria (Must Have by Day 7)

- [x] Professional login screen
- [ ] Clean dashboard with navigation
- [x] **Students**: View, search, add, edit, delete (with majors)
- [x] **Departments**: Full CRUD
- [x] Polished, consistent UI
- [x] Error handling and user feedback
- [ ] Courses management
- [ ] Ready for demo

---

## 🌟 Bonus Features (If Ahead of Schedule)

- [x] Majors managment (adding/removing/editing majors)
- [ ] Advanced user managment for employees
- [ ] Roles for employees and different access zones/permissions for each role
- [ ] Export to CSV
- [ ] Data statistics/reports

---

## 📝 Daily Notes

### Day 1 Notes:
Files `login_window.py`, `dashboard_window.py` when possible should be optimised to use .ui files and not manually adding pyqt widgets. Remember to add a 'logout' button in day 2!

### Day 2 Notes:
Full working models for students and departments and a base CRUD model. Added a functional logout button to the `dashboard.ui` layout. Created logos and placed them in `brand/`:
- `brand/campushub-high-resolution-logo-grayscale-transparent` - Black PNG horizontal logo (icon+text)
- `brand/campushub-high-resolution-logo-transparent` - White PNG horizontal logo (icon+text)
- `brand/campushub-icon-grayscale-transparent` - Black PNG icon
- `brand/campushub-icon-transparent` - White PNG icon

Remember to implement the logos in day 3 in places like the login screen (instead of the "CampusHub" text) and the dashboard (icon on the left-hand side of the welcome message).

### Day 3 Notes:
Completed the day with full searching abilities of students tab. Implemented logos in the login screen and the dashboard.


### Day 4 Notes:
Day 4 was great! We now have full students controls (adding, editing, searching) except removing students. It would be good to consider styling the 'Status' column in the 'Students' tab and assign colors to each status entry (active=green, graduated=grey, inactive=yellow, suspended=red). Other than that, work is going perfectly smooth for now!

### Day 5 Notes:
Added status color coding, implemented student delete and full departments tab. I have modified this roadmap a bit today with new tasks and I am leaning towards a more advanced system than previosly planned because of extra time on my hands. I have migrated some variables to a global `settings.py` for easier changes if needed.

### Day 6 Notes:
I encountered a bug regarding table sorting that would cause the table to loose sometimes even half of the data when refreshing after sorting the table. I've fixed the bug by adding a lock that would make it impossible to sort while populating the table.
- Added employee management scaffolding: `app/models/employee.py`, `app/ui/tabs/employees_tab.py`, and `app/ui/layout/employees_tab.ui`.
- Implemented dialogs for management flows: `assign_head_dialog.py`, `major_dialog.py`, `manage_majors_dialog.py` and corresponding `.ui` files.
- Added `app/core/loading_utils.py` to centralize loading indicators used across long-running DB operations.
- Expanded `ui/dialogs/` with department/major management dialogs and moved several hardcoded UI paths into `app/settings.py`.

### Day 7 Notes:


---

**Remember:** It's better to have 3 features that work perfectly than 10 features that are half-broken. Focus on quality over quantity!