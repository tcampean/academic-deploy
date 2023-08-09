from wtforms import StringField, PasswordField, BooleanField, IntegerField, DateField, TextAreaField, RadioField, \
    HiddenField, FieldList, SelectField
from wtforms import FormField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp, Optional
from flask_login import current_user
from wtforms import ValidationError, validators
from Model import AccountsTable, StudentTable
from Model.AccountsTable import Account
from Model.StudentTable import Student
from Model.Course import Course
from Model.TeacherTable import Teacher
from app import create_app, database, login_manager

app = create_app()
app.app_context().push()


class grades_form_teacher(FlaskForm):
    coursez = Course.query.all()
    students = Student.query.all()

    last_name = SelectField(validators=[InputRequired()], choices=[student.last_name for student in students])
    course = SelectField(validators=[InputRequired()], choices=[course.course_name for course in coursez])
    grades = SelectField(validators=[InputRequired()], choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


class profile_form_teacher(FlaskForm):
    first_name = StringField(validators=[InputRequired(), Length(1, 64)])
    last_name = StringField(validators=[InputRequired(), Length(1, 64)])
    department = IntegerField(validators=[InputRequired()])
    chief = RadioField('Chief', choices=[(1, 'Chief'), (0, 'Not Chief')])


class profile_form_student(FlaskForm):
    first_name = StringField(validators=[InputRequired(), Length(1, 64)])
    last_name = StringField(validators=[InputRequired(), Length(1, 64)])


class profile_form_staff(FlaskForm):
    first_name = StringField(validators=[InputRequired(), Length(1, 64)])
    last_name = StringField(validators=[InputRequired(), Length(1, 64)])


class login_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=72)])
    username = StringField(validators=[Optional()])


class enrollment_form(FlaskForm):
    username = StringField(validators=[
        InputRequired(),
        Length(3, 20, message="Please provide a valid name"),
        Regexp("^[A-Za-z][A-Za-z0-9_.]*$", 0, "Usernames must  have only letters, " "number, dots or underscores", ),
    ])

    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    password = PasswordField(validators=[InputRequired(), Length(8, 72)])
    copypassword = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo('password', message="Passwords must match!")
        ]
    )

    access_level = RadioField('Access Level', choices=[('Teacher', 'Teacher account'), ('Staff', 'Staff account'),
                                                       ('Student', 'Student account')], default='Student')

    def validate_email(self, email):
        if Account.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered")

    def validate_username(self, username):
        if Account.query.filter_by(email=username.data).first():
            raise ValidationError("Username already taken")


class coursesForm(FlaskForm):
    course_id = HiddenField()
    want = BooleanField()


class coursesListForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(coursesListForm, self).__init__(*args, **kwargs)

        for item_form in self.items:
            for course in kwargs['data']['items']:
                if course.course_id == item_form.course_id.data:
                    item_form.want.label = ''
                    item_form.label = course.course_name

    items = FieldList(FormField(coursesForm))
