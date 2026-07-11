# Student Feedback System (Flask + SQLAlchemy + MySQL)

A simple CRUD web application for managing **Students**, **Courses**, and **Feedback**,
built with Flask, Flask-SQLAlchemy, and MySQL, styled with Bootstrap 5.

## Project Structure
```
webii_assignment/
├── app.py              # Flask app & all routes (CRUD logic)
├── config.py           # DB configuration
├── database.py         # SQLAlchemy models (Student, Course, Feedback)
├── schema.sql          # MySQL script to create DB + tables + sample data
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── students.html / student_form.html
│   ├── courses.html   / course_form.html
│   └── feedback.html
|   |___ course_form.html
|  / feedback_form.html
└── static/css/style.css
```

## Setup Instructions

### 1. Create the MySQL database
Make sure MySQL server is running, then run:
```bash
mysql -u root -p < schema.sql
```
This creates the `student_feedback_system` database with `students`, `courses`,
and `feedback` tables.

### 2. Create a virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure the database connection
Open `config.py` and update the connection string with your MySQL username/password:
```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:YOUR_PASSWORD@localhost/student_feedback_system"
```
Or set it as an environment variable instead:
```bash
export DATABASE_URL="mysql+pymysql://root:YOUR_PASSWORD@localhost/student_feedback_system"
```

### 4. Run the application
```bash
python app.py
```
Visit **http://127.0.0.1:5000/** in your browser.

## Features
- **Students / Courses / Feedback** — full Create, Read, Update, Delete
- Server-side validation on required fields
- Delete confirmation prompt (JS `confirm()`) before removing a record
- Feedback form links a Student and Course via dropdowns (foreign keys)
- Clean Bootstrap 5 UI with flash messages for success/error feedback

## Notes for the Assignment Write-up
- **Create**: `add_student`, `add_course`, `add_feedback` routes in `app.py`
- **Read**: `list_students`, `list_courses`, `list_feedback` routes render HTML tables
- **Update**: `edit_student`, `edit_course`, `edit_feedback` — pre-fill form with existing data
- **Delete**: `delete_student`, `delete_course`, `delete_feedback` — POST-only, guarded by
  a JavaScript confirmation dialog on the front end
- Relationships: `Feedback` has foreign keys to both `Student` and `Course`;
  deleting a Student or Course cascades and removes their related Feedback rows.
