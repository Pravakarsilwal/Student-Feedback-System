import os


class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/student_feedback_system"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-this")
