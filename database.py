from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    mobile = db.Column(db.String(15))
    gender = db.Column(db.String(10))
    address = db.Column(db.String(255))
    birthday = db.Column(db.Date)

    feedbacks = db.relationship(
        "Feedback", backref="student", cascade="all, delete-orphan"
    )


class Course(db.Model):
    __tablename__ = "courses"

    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False)

    feedbacks = db.relationship(
        "Feedback", backref="course", cascade="all, delete-orphan"
    )


class Feedback(db.Model):
    __tablename__ = "feedback"

    feedback_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer, db.ForeignKey("students.student_id"), nullable=False
    )
    course_id = db.Column(
        db.Integer, db.ForeignKey("courses.course_id"), nullable=False
    )
    feedback_text = db.Column(db.Text, nullable=False)
