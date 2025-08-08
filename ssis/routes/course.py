from flask import Blueprint
from flask import current_app as app
from flask import render_template, request, redirect, jsonify, url_for

from ..models.Course import Course
from ..models.College import College

course_bp = Blueprint(
    "course_bp",
    __name__,
)

@course_bp.route("/course", methods=['GET', 'POST'])
def course():
    colleges = College.get_all()
    courses = Course.get_all()
    return render_template('course_home.html', colleges=colleges, courses=courses)


@course_bp.route("/course/add", methods=['GET', 'POST'])
def course_add():
    code = request.form.get('code')
    name = request.form.get('name')
    college_code = request.form.get('college_code')
    exist_course = Course.check_existing_code(code)
    if exist_course:
        error = f'Course Code: {code} is already taken'
        return jsonify({'error' : error})
    else:
        try:
            course = Course(code=code,name=name,college_code=college_code)
            course.add()
            return redirect(url_for("course_bp.course"))
        except Exception as e:
            return jsonify({'error' : e})
  

@course_bp.route("/course/delete", methods=['GET', 'POST'])
def course_delete():
    try:
        code = request.form.get('csasdsda')
        course = Course.get_one(code)
        course.delete()
        return redirect(url_for("course_bp.course"))

    except Exception as e:
        error = f"Error: {e}"
        return jsonify({
            'error' : error
        })


@course_bp.route("/course/edit", methods=['GET', 'POST'])
def course_edit():
    pastcode = request.form.get('code')
    code = request.form.get('edit_course_code')
    name = request.form.get('edit_course_name')
    college_code = request.form.get('edit_course_college')
    error = f"CODE: {pastcode} {code} {name} {college_code}"

    course = Course.get_one(pastcode)

    if code != pastcode:
        exist_course_code = Course.get_one(code)
        if exist_course_code:
            error = f'Course Code: {code} is already taken'
            return jsonify({'error' : error})
        else:
            try:
                course = Course(code=code,name=name,college_code=college_code) 
                course.update(pastcode)    
                return redirect(url_for("course_bp.course"))       
            except Exception as e:
                return jsonify({'error' : e})
    else:
        try:
            course.name = name
            course.college_code = college_code
            course.update(code)
            return redirect(url_for("course_bp.course"))  
        except Exception as e:
            return jsonify({
                'error' : e
            })

@course_bp.route("/course/search", methods=['GET','POST'])
def course_search():
    input = request.args.get("querycourse")
    filter = request.args.get("filter_course")
    if input:
        courses = Course.search(input,filter)
        if not courses:
            filter_message = ""
            if filter == "0":
                filter_message = "Course Code or Course name or Course College Code"
            elif filter == "1":
                filter_message = "Course Code"
            elif filter == "2":
                filter_message = "ourse name"
            elif filter == "3":
                filter_message = "Course College Code"
            return render_template('course_home.html', courseInput = input, search = True, hideAdd = True, filter_message=filter_message)
        else:
            return render_template('course_home.html', courses=courses, courseInput = input , hideAdd=True,search = True)
    return redirect(url_for('course_bp.course'))