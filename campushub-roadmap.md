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
- [ ] Design dashboard UI in Qt Designer (tabs for each entity)
- [ ] Create `app/core/base_model.py` (reusable CRUD base class)
- [ ] Create `app/models/student.py` (Student model)
- [ ] Create `app/models/department.py` (Department model)
- [ ] Test models with simple queries in Python console
- [ ] Update dashboard_window.py to load tabs

**Deliverable:** ✓ Dashboard with tabs + working models

---

## Day 3 - Students Table View (2-3 hours)

**Goal:** Students display with search

### Tasks
- [ ] Create students tab UI in Qt Designer
- [ ] Create `app/ui/tabs/students_tab.py`
- [ ] Load students data into QTableWidget
- [ ] Add search box functionality
- [ ] Style the table (modern look)
- [ ] Add refresh button
- [ ] Test with dummy data

**Deliverable:** ✓ Students display with search

---

## Day 4 - Students CRUD - Part 1 (2-3 hours)

**Goal:** Can add and edit students

### Tasks
- [ ] Create add/edit student dialog UI in Qt Designer
- [ ] Create `app/ui/dialogs/student_dialog.py`
- [ ] Implement form validation (required fields, valid PESEL, etc.)
- [ ] Wire up "Add Student" button
- [ ] Wire up "Edit Student" button (double-click row or edit button)
- [ ] Test adding new students
- [ ] Test editing existing students

**Deliverable:** ✓ Can add and edit students

---

## Day 5 - Students CRUD - Part 2 & Departments (2-3 hours)

**Goal:** Students fully working + Departments basic CRUD

### Tasks
- [ ] Implement delete student (with confirmation dialog)
- [ ] Handle student-major relationship in add/edit dialog
- [ ] Test complete student workflow (add, edit, delete, search)
- [ ] Create departments tab UI (reuse student pattern)
- [ ] Implement departments CRUD (simpler than students)
- [ ] Test departments workflow

**Deliverable:** ✓ Students fully working + Departments basic CRUD

---

## Day 6 - Polish & Employees (2-3 hours)

**Goal:** Polished, bug-free core features

### Tasks
- [ ] Add loading indicators for database operations
- [ ] Improve error messages (user-friendly)
- [ ] Consistent styling across all screens
- [ ] Fix any bugs found during testing
- [ ] Add input validation feedback (red borders, tooltips)
- [ ] **IF TIME:** Start employees management (copy student pattern)
- [ ] **IF TIME:** Add employees tab

**Deliverable:** ✓ Polished, bug-free core features

---

## Day 7 - Final Polish & Testing (2-3 hours)

**Goal:** Production-ready app for submission

### Tasks
- [ ] End-to-end testing of all features
- [ ] Fix any remaining bugs
- [ ] Add finishing touches (icons, colors, spacing)
- [ ] Ensure consistent fonts and sizes
- [ ] Test on fresh database with dummy data
- [ ] Practice demo presentation
- [ ] Prepare demo script/notes
- [ ] Test worst-case scenarios (empty fields, invalid data)

**Deliverable:** ✓ Production-ready app for submission

---

## 🏗️ Project Architecture

```
app/
├── core/
│   ├── auth.py              # Password verification
│   ├── base_model.py        # Reusable CRUD base class
│   ├── database_connection.py (existing)
│   └── window_utils.py      (existing)
├── models/
│   ├── student.py           # Student database operations
│   ├── department.py        # Department database operations
│   └── employee.py          # (if time permits)
├── ui/
│   ├── dialogs/
│   │   ├── student_dialog.py
│   │   └── department_dialog.py
│   ├── tabs/
│   │   ├── students_tab.py
│   │   └── departments_tab.py
│   ├── login_window.py
│   └── dashboard_window.py
└── ui/layout/               # .ui files from Qt Designer
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

- [ ] Professional login screen
- [ ] Clean dashboard with navigation
- [ ] **Students**: View, search, add, edit, delete (with majors)
- [ ] **Departments**: Full CRUD
- [ ] Polished, consistent UI
- [ ] Error handling and user feedback
- [ ] Ready for demo

---

## 🌟 Bonus Features (If Ahead of Schedule)

- [ ] Employees management
- [ ] Courses management
- [ ] Advanced filtering
- [ ] Export to CSV
- [ ] Data statistics/reports

---

## 📝 Daily Notes

### Day 1 Notes:
Files `login_window.py`, `dashboard_window.py` when possible should be optimised to use .ui files and not manually adding pyqt widgets. Remember to add a 'logout' button in day 2!

### Day 2 Notes:


### Day 3 Notes:


### Day 4 Notes:


### Day 5 Notes:


### Day 6 Notes:


### Day 7 Notes:


---

**Remember:** It's better to have 3 features that work perfectly than 10 features that are half-broken. Focus on quality over quantity!