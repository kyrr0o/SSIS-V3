# ssis/__init__.py

from flask import Flask
from .extension import mysql
from config import Config
import cloudinary

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)

    # ✅ Cloudinary configuration using app.config
    cloudinary.config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET'],
        secure=True
    )

    # ✅ Register routes
    from .routes import college, course, student
    app.register_blueprint(college.college_bp)
    app.register_blueprint(course.course_bp)
    app.register_blueprint(student.student_bp)

    return app
