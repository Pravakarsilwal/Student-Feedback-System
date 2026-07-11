from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash

from config import Config
from database import db, Student, Course, Feedback

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# ----------------------------------------------------------------------
# Helper functions (reusable)
# ----------------------------------------------------------------------
def parse_date(date_str):
    """Convert a 'YYYY-MM-DD' string from an HTML date input into a date object."""
    if not date_str:
        return None
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def get_or_404(model, pk_field, pk_value):
    """Fetch a record by primary key or raise a friendly error via flash + redirect."""
    return model.query.get(pk_value)


# ----------------------------------------------------------------------
# Home / Dashboard
# ----------------------------------------------------------------------
@app.route("/")
def home():
    counts = {
        "students": Student.query.count(),
        "courses": Course.query.count(),
        "feedback": Feedback.query.count(),
    }
    return render_template("index.html", counts=counts)


# ----------------------------------------------------------------------
# STUDENTS - CRUD
# ----------------------------------------------------------------------
@app.route("/students")
def list_students():
    students = Student.query.order_by(Student.student_id).all()
    return render_template("students.html", students=students)


@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        mobile = request.form.get("mobile", "").strip()
        gender = request.form.get("gender", "").strip()
        address = request.form.get("address", "").strip()
        birthday = request.form.get("birthday", "").strip()

        # ---- Validation ----
        if not name or not email:
            flash("Name and Email are required fields.", "danger")
            return render_template("student_form.html", student=request.form, action="Add")

        if Student.query.filter_by(email=email).first():
            flash("A student with this email already exists.", "danger")
            return render_template("student_form.html", student=request.form, action="Add")

        student = Student(
            name=name,
            email=email,
            mobile=mobile or None,
            gender=gender or None,
            address=address or None,
            birthday=parse_date(birthday),
        )
        db.session.add(student)
        db.session.commit()
        flash("Student added successfully!", "success")
        return redirect(url_for("list_students"))

    return render_template("student_form.html", student=None, action="Add")


@app.route("/students/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        mobile = request.form.get("mobile", "").strip()
        gender = request.form.get("gender", "").strip()
        address = request.form.get("address", "").strip()
        birthday = request.form.get("birthday", "").strip()

        if not name or not email:
            flash("Name and Email are required fields.", "danger")
            return render_template("student_form.html", student=request.form, action="Edit", student_id=student_id)

        existing = Student.query.filter_by(email=email).first()
        if existing and existing.student_id != student_id:
            flash("Another student is already using this email.", "danger")
            return render_template("student_form.html", student=request.form, action="Edit", student_id=student_id)

        student.name = name
        student.email = email
        student.mobile = mobile or None
        student.gender = gender or None
        student.address = address or None
        student.birthday = parse_date(birthday)

        db.session.commit()
        flash("Student updated successfully!", "success")
        return redirect(url_for("list_students"))

    return render_template("student_form.html", student=student, action="Edit", student_id=student_id)


@app.route("/students/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully!", "success")
    return redirect(url_for("list_students"))


# ----------------------------------------------------------------------
# COURSES - CRUD
# ----------------------------------------------------------------------
@app.route("/courses")
def list_courses():
    courses = Course.query.order_by(Course.course_id).all()
    return render_template("courses.html", courses=courses)


@app.route("/courses/add", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        course_name = request.form.get("course_name", "").strip()
        credits = request.form.get("credits", "").strip()
        

        if not course_name or not credits:
            flash("Course Name and Credits are required fields.", "danger")
            return render_template("course_form.html", course=request.form, action="Add")

        if not credits.isdigit():
            flash("Credits must be a whole number.", "danger")
            return render_template("course_form.html", course=request.form, action="Add")

        course = Course(course_name=course_name, credits=int(credits))
        db.session.add(course)
        db.session.commit()
        flash("Course added successfully!", "success")
        return redirect(url_for("list_courses"))

    return render_template("course_form.html", course=None, action="Add")


@app.route("/courses/edit/<int:course_id>", methods=["GET", "POST"])
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)

    if request.method == "POST":
        course_name = request.form.get("course_name", "").strip()
        credits = request.form.get("credits", "").strip()

        if not course_name or not credits:
            flash("Course Name and Credits are required fields.", "danger")
            return render_template("course_form.html", course=request.form, action="Edit", course_id=course_id)

        if not credits.isdigit():
            flash("Credits must be a whole number.", "danger")
            return render_template("course_form.html", course=request.form, action="Edit", course_id=course_id)

        course.course_name = course_name
        course.credits = int(credits)
        db.session.commit()
        flash("Course updated successfully!", "success")
        return redirect(url_for("list_courses"))

    return render_template("course_form.html", course=course, action="Edit", course_id=course_id)


@app.route("/courses/delete/<int:course_id>", methods=["POST"])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash("Course deleted successfully!", "success")
    return redirect(url_for("list_courses"))


# ----------------------------------------------------------------------
# FEEDBACK - CRUD
# ----------------------------------------------------------------------
@app.route("/feedback")
def list_feedback():
    feedbacks = Feedback.query.order_by(Feedback.feedback_id).all()
    return render_template("feedback.html", feedbacks=feedbacks)


@app.route("/feedback/add", methods=["GET", "POST"])
def add_feedback():
    students = Student.query.order_by(Student.name).all()
    courses = Course.query.order_by(Course.course_name).all()

    if request.method == "POST":
        student_id = request.form.get("student_id", "")
        course_id = request.form.get("course_id", "")
        feedback_text = request.form.get("feedback_text", "").strip()

        if not student_id or not course_id or not feedback_text:
            flash("Student, Course and Feedback text are all required.", "danger")
            return render_template(
                "feedback_form.html", feedback=request.form, students=students,
                courses=courses, action="Add"
            )

        feedback = Feedback(
            student_id=int(student_id),
            course_id=int(course_id),
            feedback_text=feedback_text,
        )
        db.session.add(feedback)
        db.session.commit()
        flash("Feedback submitted successfully!", "success")
        return redirect(url_for("list_feedback"))

    return render_template("feedback_form.html", feedback=None, students=students, courses=courses, action="Add")


@app.route("/feedback/edit/<int:feedback_id>", methods=["GET", "POST"])
def edit_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    students = Student.query.order_by(Student.name).all()
    courses = Course.query.order_by(Course.course_name).all()

    if request.method == "POST":
        student_id = request.form.get("student_id", "")
        course_id = request.form.get("course_id", "")
        feedback_text = request.form.get("feedback_text", "").strip()

        if not student_id or not course_id or not feedback_text:
            flash("Student, Course and Feedback text are all required.", "danger")
            return render_template(
                "feedback_form.html", feedback=request.form, students=students,
                courses=courses, action="Edit", feedback_id=feedback_id
            )

        feedback.student_id = int(student_id)
        feedback.course_id = int(course_id)
        feedback.feedback_text = feedback_text
        db.session.commit()
        flash("Feedback updated successfully!", "success")
        return redirect(url_for("list_feedback"))

    return render_template(
        "feedback_form.html", feedback=feedback, students=students,
        courses=courses, action="Edit", feedback_id=feedback_id
    )


@app.route("/feedback/delete/<int:feedback_id>", methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    flash("Feedback deleted successfully!", "success")
    return redirect(url_for("list_feedback"))


if __name__ == "__main__":
    app.run(debug=True)
