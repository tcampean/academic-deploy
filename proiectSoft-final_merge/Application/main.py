import os
import random
from random import randint

import flask
from flask import render_template, session, url_for, redirect, flash, request, make_response
from pdfkit import pdfkit
from sqlalchemy import func
from werkzeug.utils import secure_filename

import Model
from Model import AccountsTable, StudentTable, TeacherTable
from Model.AccountsTable import Account
from Model.StudentCourse import StudentCourse
from Model.StudentTable import Student
from Model.Department import Department
from Model.Staff import Staff
from Model.Course import Course
from Model.TeacherTable import Teacher
from Model.Database import *
from app import create_app, database, login_manager
from datetime import timedelta
from forms import login_form, enrollment_form, profile_form_teacher, profile_form_student, \
    profile_form_staff, grades_form_teacher
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError, DataError, DatabaseError, InterfaceError, InvalidRequestError
import pdfkit
from Model.ProposedCourse import ProposedCourse

app = create_app()

access_level1 = ""
username1 = ""

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))


@app.before_first_request
def session_handler():
    #database.create_all()
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


@app.route('/', methods=("GET", "POST"))
def index():
    return redirect(url_for('login'))


@app.route('/enroll/<selected_year>', methods=("GET", "POST"))
def enroll(selected_year):
    student = Student.query.filter_by(username=current_user.username).first()
    student.year = selected_year

    courses = Course.query.filter_by(course_year=selected_year, course_type=1).all()
    s_group = 0
    if int(selected_year) == 1:
        s_group = randint(911, 917)
    elif int(selected_year) == 2:
        s_group = randint(921, 927)
    elif int(selected_year) == 3:
        s_group = randint(931, 937)
    student.group = s_group
    database.session.commit()

    for course in courses:
        sc_id = database.session.query(func.max(StudentCourse.student_course_id)).scalar()
        if sc_id is None:
            sc_id = 0
        new_sc = StudentCourse(
            student_course_id=sc_id + 1,
            student_id=student.student_id,
            course_id=course.course_id,
            grade=None
        )
        database.session.add(new_sc)
        database.session.commit()

    database.session.commit()
    return redirect(url_for('curriculum'))


@app.route('/curriculum', methods=("GET", "POST"))
def curriculum():
    student = Student.query.filter_by(username=current_user.username).first()
    if student.year is None:
        return render_template("Student/StudentNotEnrolled.html")
    student_courses = StudentCourse.query.filter_by(student_id=student.student_id).all()
    courses = Course.query.filter_by(course_year=student.year)
    teacher = Teacher.query.all()
    return render_template('Student/StudentCurriculum.html', courses=courses, teachers=teacher,
                           student_courses=student_courses)


@app.route('/study_contract', methods=("GET", "POST"))
def study_contract():
    student = Student.query.filter_by(username=current_user.username).first()
    if student.year is None:
        return render_template("Student/StudentNotEnrolled.html")
    courses = Course.query.filter_by(course_year=student.year, course_type=1).all()
    optionals = Course.query.filter_by(course_type=0, course_year=student.year).all()
    student_courses = database.session.query(StudentCourse).filter_by(student_id=student.student_id).all()
    student_courses_id = []
    for student_course in student_courses:
        student_course = str(student_course)
        tokens = student_course.split(':')
        student_courses_id.append(int(tokens[2]))
    teacher = Teacher.query.all()
    return render_template('Student/StudentStudyContract.html', courses=courses, teachers=teacher, optionals=optionals,
                           student_courses=student_courses_id)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_documents', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        path = os.getcwd()
        UPLOAD_FOLDER = os.path.join(path, 'uploads')
        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)

        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        if 'file' not in request.files:
            print('No file part')
        file = request.files['file']
        if file.filename == '':
            print('No file selected for uploading')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('File successfully uploaded')
        else:
            print('Allowed file types are txt, pdf, png, jpg, jpeg, doc, docx')
    return render_template('Student/StudentUploadDocuments.html')


@app.route('/study_contract/pdf', methods=("GET", "POST"))
def study_contract_pdf():
    student = Student.query.filter_by(username=current_user.username).first()
    mandatory_courses = Course.query.filter_by(course_year=student.year, course_type=1).all()
    courses = Course.query.filter_by(course_year=student.year).all()
    for course in mandatory_courses:
        added = StudentCourse.query.filter_by(course_id=course.course_id, student_id=student.student_id).first()
        if added is None:
            sc_id = database.session.query(func.max(StudentCourse.student_course_id)).scalar()
            if sc_id is None:
                sc_id = 0
            new_sc = StudentCourse(
                student_course_id=sc_id + 1,
                student_id=student.student_id,
                course_id=course.course_id,
                grade=None
            )
            database.session.add(new_sc)
            database.session.commit()
    student_courses = StudentCourse.query.filter_by(student_id=student.student_id).all()

    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    rendered = render_template("Student/StudentContract.html", student_courses=student_courses, student=student,
                               courses=courses)
    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=contract.pdf'

    return response


'''
@app.route('/<access_level>/profile/student_grades', methods=("GET", "POST"))
@login_required
def grades():
    user = Student.query.filter_by(username=current_user.username).first()
    student_courses = StudentCourse.query.filter_by(student_id=user.student_id).all()
    courses = Course.query.all()

    return render_template('Student/StudentGrades.html',student_courses = student_courses, courses = courses)
'''


@app.route('/take_optional/<optional_course>', methods=("GET", "POST"))
def take_optional(optional_course):
    student = Student.query.filter_by(username=current_user.username).first()
    sc_id = database.session.query(func.max(StudentCourse.student_course_id)).scalar()
    tokens = optional_course.split(':')
    if sc_id is None:
        sc_id = 0
    new_sc = StudentCourse(
        student_course_id=sc_id + 1,
        student_id=student.student_id,
        course_id=tokens[0],
        grade=None
    )
    database.session.add(new_sc)
    database.session.commit()
    return redirect(url_for('study_contract'))


@app.route('/remove_optional/<optional_course>', methods=("GET", "POST"))
def remove_optional(optional_course):
    student = Student.query.filter_by(username=current_user.username).first()
    tokens = optional_course.split(':')
    StudentCourse.query.filter_by(student_id=student.student_id, course_id=tokens[0]).delete()

    database.session.commit()
    return redirect(url_for('study_contract'))


@app.route("/test", methods=['GET', 'POST'])
def test():
    select = request.form.get('year_select')
    return str(select)  # just to see what select is


@app.route('/<access_level>/profile/StudentInfo', methods=("GET", "POST"))
def student_info(access_level):
    if access_level == 'Staff':
        student_courses = StudentCourse.query.all()
        if request.form.get("year_select") is None:
            year = 1
        else:
            year = request.form.get("year_select")
        print(year)
        courses = Course.query.filter_by(course_year=year).all()
        students = Student.query.all()

        return render_template(f"{access_level}/StudentInfo.html", students=students, student_courses=student_courses,
                               courses=courses)


@app.route('/<access_level>/profile/pdf', methods=("GET", "POST"))
def generate_pdf(access_level):
    if access_level == 'Staff':
        students_gpa = database.session.query(Student.student_id, Student.first_name, Student.last_name,
                                              func.avg(StudentCourse.grade).label('GPA')) \
            .filter(Student.student_id == StudentCourse.student_id) \
            .group_by(Student.student_id, Student.first_name, Student.last_name) \
            .order_by('GPA') \
            .all()
        # print(students_gpa)
        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        rendered = render_template(f"{access_level}/StaffStudentPdf.html", studentsGPA=students_gpa)
        pdf = pdfkit.from_string(rendered, False, configuration=config)

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

        return response


@app.route('/<access_level>/profile/grades', methods=("GET", "POST"))
def grades(access_level):
    global access_level1
    access_level = access_level1
    if access_level == 'Teacher':
        user = Teacher.query.filter_by(username=current_user.username).first()
        courses = Course.query.filter_by(teacher_id=user.teacher_id).all()
        students = Student.query.all()
        student_courses = StudentCourse.query.all()

        return render_template(f"{access_level}/{access_level}Grades.html", user=user, courses=courses,
                               students=students, student_courses=student_courses)
    elif access_level == 'Student':
        user = Student.query.filter_by(username=current_user.username).first()
        student_courses = StudentCourse.query.filter_by(student_id=user.student_id).all()
        courses = Course.query.all()

        return render_template(f"{access_level}/{access_level}Grades.html", student_courses=student_courses,
                               courses=courses)


@app.route('/propose_optionals_accept/<accepted_course>', methods=("GET", "POST"))
def propose_optionals_accept(accepted_course):
    user = Teacher.query.filter_by(username=current_user.username).first()

    if user.chief_department:
        tokens = accepted_course.split(':')
        print(accepted_course)
        accepted_course = ProposedCourse(int(tokens[0]), tokens[1], tokens[2], int(tokens[3]),
                                         int(tokens[4]), int(tokens[5]), int(tokens[6]), int(tokens[7]))
        print(accepted_course)
        ProposedCourse.query.filter_by(proposed_course_id=accepted_course.proposed_course_id).delete()

        proposed = database.session.query(func.max(Course.course_id)).scalar()
        if proposed is None:
            proposed = 0
        new_course = Course(
            course_id=proposed + 1,
            course_name=accepted_course.proposed_course_name,
            course_description=accepted_course.proposed_course_description,
            course_type=accepted_course.proposed_course_type,
            course_semester=accepted_course.proposed_course_semester,
            course_year=accepted_course.proposed_course_year,
            teacher_id=int(accepted_course.teacher_id),
            course_max_number=accepted_course.proposed_course_max_number
        )
        database.session.add(new_course)
        database.session.commit()
    proposed_courses = ProposedCourse.query.all()
    return redirect(url_for('propose_optionals', proposed_courses=proposed_courses, limit=9001))


@app.route('/propose_optionals', methods=("GET", "POST"))
def propose_optionals():
    user = Teacher.query.filter_by(username=current_user.username).first()

    if user.chief_department:
        proposed_courses = ProposedCourse.query.all()
        optional_courses = Course.query.filter_by(course_type=0).all()
        return render_template('Teacher/ChiefTeacherOptionals.html', proposed_courses=proposed_courses,
                               optional_courses=optional_courses, limit=9001)
    else:
        if request.method == "POST":

            proposed = database.session.query(func.max(ProposedCourse.proposed_course_id)).scalar()
            if proposed is None:
                proposed = 0
            proposed_course = ProposedCourse(
                proposed_course_id=proposed + 1,
                proposed_course_name=request.form["name"],
                proposed_course_description=request.form["description"],
                proposed_course_type=0,
                proposed_course_semester=int(''.join(x for x in request.form["semester"] if x.isdigit())),
                proposed_course_year=int(''.join(x for x in request.form["year"] if x.isdigit())),
                teacher_id=int(user.teacher_id),
                proposed_course_max_number=int(request.form["maxnumber"])
            )

            database.session.add(proposed_course)
            database.session.commit()

        limit = database.session.query(func.count(ProposedCourse.teacher_id == user.teacher_id)).scalar()
        proposed_courses = ProposedCourse.query.all()
        return render_template('Teacher/TeacherOptionals.html', proposed_courses=proposed_courses, limit=limit)


@app.route('/submitGrade', methods=("GET", "POST"))
def submitGradesForm():
    # # stud = request.form.get('stud')
    # # print(stud)
    # user = Student.query.filter_by(last_name=stud).first()
    # #
    # # grades = StudentCourse.query.filter_by(student_id=user.student_id).all()
    # teacher = Teacher.query.filter_by(username=current_user.username).first()
    # # courses = Course.query.filter_by(teacher_id=teacher.teacher_id).all()
    # # take all courses a teacher teaches and enable him to add a grade for  that course + student selected ?

    form = grades_form_teacher()
    if form.validate_on_submit():
        try:

            last_name = form.last_name.data
            grade = form.grades.data
            course = form.course.data

            courss = Course.query.filter_by(course_name=course).first()
            student = Student.query.filter_by(last_name=last_name).first()

            aux = StudentCourse.query.all()

            id = len(aux) + 1

            g = StudentCourse(student_id=student.student_id, course_id=courss.course_id, grade=grade,
                              student_course_id=id)

            database.session.add(g)
            database.session.commit()

        except Exception as e:
            print(e)

    return render_template('Teacher/TeacherAddGradeForm.html', form=form, btn_action="SubmitData")


@app.route("/<access_level>/profile/<username>", methods=["GET", "POST"])
def profile(access_level, username):
    global access_level1, username1
    # if access_level == 'Teacher':
    #     user = Teacher.query.filter_by(username=username).first()
    #     print(user.first_name, user.last_name)
    #     department = Department.query.filter_by(department_id=user.department).first()
    #
    #     return render_template(f"{access_level}/{access_level}Profile.html", firstname=user.first_name,
    #                            lastname=user.last_name, department=department.department_name)
    if access_level == 'Student':
        user = get_student_info(username)

        return render_template(f"{access_level}/{access_level}Profile.html", firstname=user['first_name'],
                               lastname=user['last_name'], year=user['student_year'], group=user['student_group'], access_level= access_level1, username= access_level)
    else:
        return redirect(url_for('profile', access_level = access_level1, username=username1))
    # elif access_level == 'Staff':
    #     user = Staff.query.filter_by(username=current_user.username).first()
    #
    #     return render_template(f"{access_level}/{access_level}Profile.html", firstname=user.first_name,
    #                            lastname=user.last_name)

@app.route("/profile2", methods=["GET", "POST"])
def profile2():
    global access_level1, username1
    return redirect(url_for('profile', access_level=access_level1, username=username1))

@app.route('/dashboard/<username>', methods=['GET', 'POST'])
def dashboard(username):
    global access_level1, username1
    user = get_user_info(username)
    firstnames = ['Mihai', 'Tudor', 'Alex', 'Daniel', 'Andrei']
    lastnames = ['Alex','Campean', 'Dragus', 'Petrisor']
    student = get_student_info(username)
    #existsT = Teacher.query.filter_by(username=username).first()
    #existsStu = Student.query.filter_by(username=username).first()
    #existsSta = Staff.query.filter_by(username=username).first()
    # if existsT:
    #     return render_template(f"{user.access_level}/{user.access_level}Profile.html", firstname=existsT.first_name,
    #                            lastname=existsT.last_name)
    if student is None:
        t = Student(username=username, first_name=random.choice(firstnames), last_name=random.choice(lastnames), year=0, group=0)
        complete_student(t)
    access_level1 = user['access_level']
    username1 = username
    return redirect(url_for('profile', access_level=user['access_level'], username=username))
    # if existsSta:
    #     return render_template(f"{user.access_level}/{user.access_level}Profile.html", firstname=existsSta.first_name,
    #                            lastname=existsSta.last_name)
    # if user.access_level == "Teacher":
    #     form = profile_form_teacher()
    #     if form.validate_on_submit():
    #         try:
    #             first_name = form.first_name.data
    #             last_name = form.last_name.data
    #             depart = int(form.department.data)
    #             ch = form.chief.data
    #
    #             t = Teacher(username=username, first_name=first_name, last_name=last_name, chief=int(ch),
    #                         department=depart)
    #
    #             database.session.add(t)
    #             database.session.add(t)
    #             database.session.commit()
    #
    #             return redirect(url_for('profile', access_level=user.access_level, username=username))
    #
    #         except Exception as e:
    #             flash(e, "danger")
    #     return render_template('Login/index.html', form=form, btn_action="SubmitData")

    # if user['access_level'] == 'Student':
    #     form = profile_form_student()
    #     try:
    #         if form.validate_on_submit():
    #             try:
    #                 first_name = form.first_name.data
    #                 last_name = form.last_name.data
    #                 print(first_name, last_name)
    #                 t = Student(username=username, first_name=first_name, last_name=last_name, year=None, group=None)
    #
    #                 complete_student(t)
    #
    #                 return redirect(url_for('profile', access_level=user['access_level'], username=username))
    #
    #             except Exception as e:
    #                 flash(e, "danger")
    #
    #     except Exception as e:
    #         t = Student(username=username, first_name=usrt, last_name=usrt, year=None, group=None)
    #
    #         complete_student(t)
    #
    #         return redirect(url_for('profile', access_level=user['access_level'], username=username))
    #
    #
    #     return render_template('Login/index.html', is_authenticated = True, access_level= user['access_level'], username= username, form=form, btn_action="Submit Data")

    # if user.access_level == 'Staff':
    #     form = profile_form_staff()
    #     if form.validate_on_submit():
    #         try:
    #             first_name = form.first_name.data
    #             last_name = form.last_name.data
    #             print(first_name, last_name)
    #             t = Staff(username=username, first_name=first_name, last_name=last_name)
    #
    #             database.session.add(t)
    #             database.session.commit()
    #
    #             return redirect(url_for('profile', access_level=user.access_level, username=username))
    #
    #         except Exception as e:
    #             flash(e, "danger")
    #
    #     return render_template('Login/index.html', form=form, btn_action="SubmitData")


@app.route('/<access_level>/profile/<username>/edit_profile', methods=("GET", "POST"))
def edit_user(access_level, username):
    if request.method == "POST":
        if access_level == "Student":
            student = Student.query.filter_by(username=username).first()
            if (request.form["first_name"] != ""):
                student.first_name = request.form["first_name"]
            if (request.form["last_name"] != ""):
                student.last_name = request.form["last_name"]
            account = Account.query.filter_by(username=username).first()
            if (request.form["password"] != ""):
                account.password = generate_password_hash(request.form["password"])
            database.session.commit()

        elif access_level == "Teacher":
            teacher = Teacher.query.filter_by(username=username).first()
            if (request.form["first_name"] != ""):
                teacher.first_name = request.form["first_name"]
            if (request.form["last_name"] != ""):
                teacher.last_name = request.form["last_name"]
            account = Account.query.filter_by(username=username).first()
            if (request.form["password"] != ""):
                account.password = generate_password_hash(request.form["password"])
            database.session.commit()
        else:
            staff = Staff.query.filter_by(username=username).first()
            if (request.form["first_name"] != ""):
                staff.first_name = request.form["first_name"]
            if (request.form["last_name"] != ""):
                staff.last_name = request.form["last_name"]
            account = Account.query.filter_by(username=username).first()
            if (request.form["password"] != ""):
                account.password = generate_password_hash(request.form["password"])
            database.session.commit()
        return redirect(url_for("profile", access_level=access_level, username=username))

    if access_level == "Student":
        user = Student.query.filter_by(username=current_user.username).first()
    if access_level == "Teacher":
        user = Teacher.query.filter_by(username=current_user.username).first()
    if access_level == "Staff":
        user = Staff.query.filter_by(username=current_user.username).first()
    return render_template(f"{access_level}/{access_level}ProfileEdit.html", firstname=user.first_name,
                           lastname=user.last_name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = check_user(form.email.data)
            if user is None:
                flash("Invalid username or password!", "danger")

            elif check_password_hash(user['password'], form.password.data):
                curr_user = Account(user['username'], user['password'], user['email'], user['access_level'])
                login_user(curr_user, force=True)
                return redirect(url_for('dashboard', username=user['username']))
            else:
                flash("Invalid username or password!", "danger")

        except Exception as e:
            flash(e, "danger")

    return render_template(
        "Login/auth.html",
        form=form,
        text="Login",
        title="Login",
        btn_action="Login"
    )


@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = enrollment_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            password = form.password.data
            username = form.username.data
            access_level = form.access_level.data

            newuser = Account(access_level=access_level, username=username, email=email,
                              password=generate_password_hash(password))

            register_student(newuser)

            # if access_level == "Teacher":
            #     t = Teacher(username=username,first_name="Mihai",last_name="Tot Mihai",chief=1,department=1)
            #     print(t.username,"am ajuns aici")
            #     database.session.add(t)
            #     database.session.commit()

            flash(f"Account created sucessfully", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            database.session.rollback()
            flash(f"something went wrong", "danger")
        except IntegrityError:
            database.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            database.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            database.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            database.session.rollback()
            flash(f"Error connecting to the database", "danger")

    return render_template("Login/auth.html", form=form, text="Create account", title="Register",
                           btn_action="Register account")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


# @app.route('/datalist')
# def RetrieveDataList():
#     employees = AccountsTable.Account.query.all()
#     return render_template('datalist.html', employees=employees)
#
#
# @app.route('/StudentList')
# def studentData():
#     employees = StudentTable.Student.query.all()
#     return render_template('StudentList.html', employees=employees)
#
#
# @app.route('/TeacherList')
# def TeacherData():
#     employees = TeacherTable.Teacher.query.all()
#     return render_template('TeacherList.html', employees=employees)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
