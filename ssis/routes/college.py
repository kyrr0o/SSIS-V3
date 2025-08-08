from flask import Blueprint
from flask import current_app as app
from flask import render_template, request, redirect, jsonify, url_for
from ..models.College import College

college_bp = Blueprint(
    "college_bp",
    __name__,
)

@college_bp.route("/college", methods=['GET','POST'])
def college():
    colleges = College.get_all()
    return render_template('college_home.html', colleges=colleges)

@college_bp.route("/college/search", methods=['GET','POST'])
def college_search():
    input = request.args.get("querycollege")
    filter = request.args.get("filter_college")
    if input:
        colleges = College.search(input,filter)
        if not colleges:
            filter_message = ""
            if filter == "0":
                filter_message = "College Code or College name"
            elif filter == "1":
                filter_message = "College Code"
            elif filter == "2":
                filter_message = "College name"
            return render_template('college_home.html', collegeInput = input, search = True, hideAdd = True, filter_message=filter_message)
        else:
            return render_template('college_home.html', colleges=colleges, collegeInput = input , hideAdd=True,search = True)
    return redirect(url_for('college_bp.college'))


@college_bp.route("/college/add", methods=['GET', 'POST'])
def college_add():
    code = request.form.get('code')
    name = request.form.get('name')
    exist_college = College.check_existing_code(code)
    if exist_college:
        error = f"College Code: {code} is already taken"
        return jsonify({'error' : error})
    else:
        try:
            college = College(code=code,name=name)
            college.add()
            return redirect(url_for("college_bp.college"))
        except Exception as e:
            return jsonify({'error' : e})
        
@college_bp.route("/college/delete", methods=['POST'])
def college_delete():
    code = request.form.get("code")

    try:
        college = College.get_one(code)
        college.delete()
        return redirect(url_for("college_bp.college"))
        
    except Exception as e:
        error = f"Error: {e}"
        return jsonify({ 'error' : error})
    

@college_bp.route("/college/edit", methods=['POST'])
def college_edit():
    pastcode = request.form.get('code')
    code = request.form.get('edit_college_code')
    name = request.form.get('edit_college_name')

    error = f"CODE: {pastcode} {code} {name}"

    college = College.get_one(pastcode)

    if code != pastcode:
        exist_college = College.get_one(code)
        if exist_college:
            error = f"College COde: {code} already taken"
            return jsonify({'error' : error})
        else:
            college = College(code=code,name=name)
            college.update(pastcode)
            return redirect(url_for("college_bp.college"))
    else:
        try:
            college.name = name
            college.update(code)
            return redirect(url_for('college_bp.college'))
        except Exception as e:
            return jsonify({'error' : e})