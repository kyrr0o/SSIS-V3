from flask import Blueprint
from flask import current_app as app
from flask import render_template, request, redirect, url_for, jsonify

from ..models.Course import Course
from ..models.College import College
from ..models.Student import Student

from cloudinary import uploader
from cloudinary.uploader import upload
from config import Config
from flask import flash
import re

student_bp = Blueprint(
    "student_bp",
    __name__,
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_public_id_from_url(url):
    match = re.search(r'/v\d+/(ssis/[^/]+)\.\w+', url)
    return match.group(1) if match else None

def check_file_size(picture):

    # image size
    maxsize = 1 * 1024 * 1024  

    picture.seek(0, 2)  
    size = picture.tell() 
    picture.seek(0) 
    print("Uploaded picture size:", size, "bytes")
    return size <= maxsize

@student_bp.route("/")
@student_bp.route("/student")
def student():
    colleges = College.get_all()
    courses = Course.get_all()

    # logic for pagination
    page = request.args.get('page', default=1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    # Get paginated student list and total count
    students = Student.get_paginated(limit=per_page, offset=offset)
    total_count = Student.get_total_count()
    total_pages = (total_count + per_page - 1) // per_page 

    return render_template(
        'student_home.html',
        colleges=colleges,
        courses=courses,
        students=students,
        page=page,
        total_pages=total_pages
    )

@student_bp.route("/student/add", methods=['POST'])
def student_add():
    print("Form Data Received:")
    print("Student ID:", request.form.get("student_id"))
    print("First Name:", request.form.get("student_first_name"))
    print("Last Name:", request.form.get("student_last_name"))
    print("Course Code:", request.form.get("student_course_code"))
    print("Year:", request.form.get("student_year"))
    print("Gender:", request.form.get("student_gender"))
    print("Student added successfully")

    id = request.form.get('student_id', '').strip()
    firstname = request.form.get('student_first_name')
    lastname = request.form.get('student_last_name')
    course_code = request.form.get('student_course_code')
    year = request.form.get('student_year')
    gender = request.form.get('student_gender')

    if not re.fullmatch(r"\d{4}-\d{4}", id):
        return jsonify({'error': 'Invalid Student ID format. Use xxxx-xxxx with only numbers.'})
    
    # Check if student ID is already taken
    exist_student = Student.check_existing_id(id)
    if exist_student:
        return jsonify({ 'error': f"Student ID: {id} is already taken" })

    # Handle optional image upload
    picture = request.files.get('formFile')
    image_url = None  # Default to None if no image

    if picture and picture.filename != '':
        if not allowed_file(picture.filename):
            return jsonify({'error': 'Image must be PNG, JPG, or JPEG'})
        if not check_file_size(picture):
            return jsonify({'error': 'Max file size is 1MB'})
        try:
            # Upload image to Cloudinary
            result = upload(picture, folder=Config.CLOUDINARY_FOLDER)
            image_url = result['secure_url']
        except Exception as e:
            return jsonify({'error': f"Image upload failed: {str(e)}"})
    
    # Create and save student
    student = Student(
        id=id,
        firstname=firstname,
        lastname=lastname,
        course_code=course_code,
        year=year,
        gender=gender,
        picture=image_url  # will be None if no image uploaded
    )
    student.add()

    return jsonify({'redirect': url_for("student_bp.student")})

@student_bp.route("/student/delete", methods=['POST'])
def student_delete():
    try:
        student_id = request.form.get('student_id')
        if not student_id:
            return """
                <script>
                    alert('Missing student ID');
                    window.location.href = '/student';
                </script>
            """

        student = Student.get_one(student_id)
        if not student:
            return """
                <script>
                    alert('Student not found');
                    window.location.href = '/student';
                </script>
            """

        if student.picture:
            public_id = get_public_id_from_url(student.picture)
            if public_id:
                uploader.destroy(public_id)

        student.delete()
        # Return a JavaScript alert and redirect instead of flash()
        return """
            <script>
                alert('Successfully deleted student');
                window.location.href = '/student';
            </script>
        """
    except Exception as e:
        return f"""
            <script>
                alert('Error deleting student: {str(e)}');
                window.location.href = '/student';
            </script>
        """


@student_bp.route("/student/edit", methods=['POST'])
def student_edit():
    pastid = request.form.get('pastid')
    id = request.form.get('edit_student_id')
    firstname = request.form.get('edit_student_first_name')
    lastname = request.form.get('edit_student_last_name')
    course_code = request.form.get('edit_student_course_code')
    year = request.form.get('edit_student_year')
    gender = request.form.get('edit_student_gender')

    picture = request.files.get('editFormFile') 

    student = Student.get_one(pastid)
    if not student:
        return jsonify({'error': 'Student not found'})

    # Check ID change
    if id != pastid:
        if Student.get_one(id):
            return jsonify({'error': f"Student ID: {id} is already taken"})
        student.id = id

    student.firstname = firstname
    student.lastname = lastname
    student.course_code = course_code
    student.year = year
    student.gender = gender

    # Only replace picture if a new one is uploaded
    if picture and picture.filename.strip() != "":
        if not allowed_file(picture.filename):
            return jsonify({'error': 'Image must be PNG, JPG, or JPEG'})
        if not check_file_size(picture):
            return jsonify({'error': 'Max file size is 1MB'})

        # Delete old image from Cloudinary if exists
        if student.picture:
            public_id = get_public_id_from_url(student.picture)
            if public_id:
                uploader.destroy(public_id)

        # Upload new image
        result = upload(picture, folder=Config.CLOUDINARY_FOLDER)
        student.picture = result['secure_url']

    student.update(pastid)
    return redirect(url_for("student_bp.student"))

@student_bp.route("/student/search", methods=['GET','POST'])
def student_search():
    input = request.args.get('querystudent')
    filter = request.args.get('filter_student')

    colleges = College.get_all()
    courses = Course.get_all()

    if input:
        students = Student.search(input, filter)
        if not students:
            filter_message = ""
            if filter == "0":
                filter_message = "Student ID or NAME or COURSE or YEAR or GENDER"
            elif filter == "1":
                filter_message = "Student ID"
            elif filter == "2":
                filter_message = "Student FirstName"
            elif filter == "3":
                filter_message = "Student Last Name"
            elif filter == "4":
                filter_message = "Student Course"
            elif filter == "5":
                filter_message = "Student Year"
            elif filter == "6":
                filter_message = "Student Gender"
            elif filter == "7":
                filter_message = "Student College"

            return render_template(
                'student_home.html',
                studentInput=input,
                search=True,
                hideAdd=True,
                filter_message=filter_message,
                colleges=colleges,
                courses=courses
            )
        else:
            return render_template(
                'student_home.html',
                students=students,
                hideAdd=True,
                search=True,
                studentInput=input,
                colleges=colleges,
                courses=courses
            )

    return redirect(url_for("student_bp.student"))
