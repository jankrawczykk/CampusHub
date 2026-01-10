# <img src="brand/campushub-high-resolution-logo-transparent.png" width="300" height="auto">

A university student management system built with PyQt6 and PostgreSQL. **Portfolio project only - not for production use.**

## About

CampusHub is a desktop application for managing student records, courses, and university administrative tasks. It features a modern PyQt6 GUI backed by a PostgreSQL database.

## Tech Stack

- **Frontend:** ![PyQt6](https://img.shields.io/badge/PyQt6-4B6F44?style=flat-square&logo=python&logoColor=white)
- **Backend:** ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
- **Package Manager:** ![uv](https://img.shields.io/badge/uv-4F9B45?style=flat-square&logo=python&logoColor=white)
- **Containerization:** ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) & ![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=flat-square&logo=docker&logoColor=white)


## Installation

### Prerequisites

- [Python 3.13](https://www.python.org/downloads/release/python-31311/) or higher
- [uv](https://github.com/astral-sh/uv) installed
- [Docker](https://docs.docker.com/desktop/) with [Compose plugin (v2+)](https://docs.docker.com/compose/install/linux/) for database

### Setup

1. **Clone the repository**
    ```bash
    gh repo clone jankrawczykk/CampusHub
    cd campushub
    ```

2. **Start the database**
    ```bash
    docker compose up
    ```

3. **Initialize the database**
    - Use `db-backups/campushub-empty.sql` for schema only
    - Use `db-backups/campushub-filled.sql` for schema with dummy data

4. **Install dependencies**
    - Project dependencies are declared in `pyproject.toml` (requires Python >= 3.13). Key packages include `argon2-cffi`, `psycopg[binary]`, and `pyqt6`.
    - Install dependencies using the included `uv` workflow:

    ```bash
    uv sync
    ```

5. **Run the application**
    ```bash
    uv run main.py
    ```

## Project Structure

- **`app/settings.py`** - Centralized configuration for database, logging, branding, and UI file paths.
- **`app/core/`** - Non-Qt utilities (authentication, database connection, logging, window utilities)
- **`app/ui/`** - PyQt6 GUI components only
- **`db-backups/`** - SQL backup files
- **`logs/`** - Application logs
- **`brand/`** - Logos and other brand assets

## Database

PostgreSQL runs in Docker on port `5432`. PgAdmin available at `http://localhost:5050`.

### Schema Overview

The database consists of the following core tables and relationships:

#### Core Tables

**`persons`** - Base person records
- `person_id` (PK) - Auto-incremented identifier
- `first_name`, `last_name` - Personal name
- `date_of_birth` - DOB
- `pesel` - Polish personal ID number (unique)
- `gender` - Enum: 'Male', 'Female', 'Other'
- `email` - Contact email
- `phone_number` - Phone contact
- `address` - Mailing address

**`students`** - Student records (extends persons)
- `student_id` (PK) - Auto-incremented identifier
- `person_id` (FK) - Reference to persons table
- `enrollment_date` - Date of enrollment
- `status` - Enum: 'Active', 'Inactive', 'Suspended', 'Graduated'

**`employees`** - Employee records (extends persons)
- `employee_id` (PK) - Auto-incremented identifier
- `person_id` (FK) - Reference to persons table
- `employment_date` - Date hired
- `status` - Enum: 'Active', 'Inactive', 'Suspended'

#### Academic Structure

**`departments`** - University departments
- `dept_id` (PK) - Auto-incremented identifier
- `name` - Department name
- `code` - Department code (e.g., "CS", "MATH")

**`department_heads`** - Department leadership assignments
- `dept_id` (FK) - Reference to departments
- `employee_id` (FK) - Reference to employees
- `start_date` - Leadership start date
- `end_date` - Leadership end date (nullable)

**`positions`** - Employee position titles
- `position_id` (PK) - Auto-incremented identifier
- `name` - Position name (e.g., "Professor", "Teaching Assistant")

**`employee_positions`** - Employee position assignments
- `employee_id` (FK) - Reference to employees
- `position_id` (FK) - Reference to positions
- `start_date` - Assignment start date
- `end_date` - Assignment end date (nullable)

**`majors`** - Academic degree programs
- `major_id` (PK) - Auto-incremented identifier
- `dept_id` (FK) - Reference to departments
- `name` - Major name
- `degree_level` - Enum: 'Bachelor', 'Master', 'PhD'

**`student_majors`** - Student major enrollments
- `student_id` (FK) - Reference to students
- `major_id` (FK) - Reference to majors
- `start_date` - Enrollment start date
- `end_date` - Graduation/end date (nullable)
- `is_primary` - Boolean indicating primary major

**`courses`** - Course offerings
- `course_id` (PK) - Auto-incremented identifier
- `dept_id` (FK) - Reference to departments
- `course_code` - Course code (e.g., "CS101")
- `title` - Course title
- `description` - Course description (nullable)
- `credits` - Credit hours (must be > 0)

#### User Management

**`users`** - System user accounts
- `user_id` (PK) - Auto-incremented identifier
- `employee_id` (FK) - Reference to employees (unique)
- `username` - Login username
- `password_hash` - Argon2id hashed password
- `created_at` - Account creation timestamp (default: current time)

**Note:** Default test accounts in `campushub-filled.sql` use the word "password" hashed with Argon2id.

---

#### Authentication

- **Hashing:** Passwords are hashed using Argon2id via the `argon2-cffi` library (see `pyproject.toml`).
- **Verification:** The app verifies credentials with `app.core.auth.verify_login()` and hashes new passwords with `app.core.auth.hash_password()`.
- **Test accounts:** The seeded data in `db-backups/campushub-filled.sql` contains sample users whose raw password is the word "password" (stored as Argon2id hashes). Example usernames include: `adam.kowalski`, `anna.nowak`, `piotr.zielinski`, `maria.wisniewska`, `tomasz.wojcik`, `katarzyna.lew`, `michal.kaminski`, `agnieszka.dab`, `pawel.kaczmarek`, `natalia.piotr`.

#### Environment & configuration (development)

- Default database connection values are set in `app/settings.py` for local development:
    - `DB_HOST=localhost`, `DB_PORT=5432`, `DB_NAME=campushub`, `DB_USER=root`, `DB_PASSWORD=root`.
- The Docker Compose setup (see `docker-compose.yml`) exposes Postgres on port `5432` and PgAdmin on port `5050`. PgAdmin default login is `admin@admin.com` / `root`.
- **Security note:** These defaults are for local development only. Store secrets in a `.env` file or a secure vault for production.

---

*Jan Krawczyk ([jankrawczykk](https://github.com/jankrawczykk))*
