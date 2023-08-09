#from Application.app import database
from app import database


class Course(database.Model):
    __tablename__ = "Course"
    __table_args__ = {'extend_existing': True}

    course_id = database.Column(database.Integer, primary_key=True)
    course_name = database.Column(database.String, nullable=False)
    course_description = database.Column(database.String, nullable=False)
    course_type = database.Column(database.Integer, nullable=False)  # obligatorii = 1/optionale = 0
    course_semester = database.Column(database.Integer, nullable=False)
    course_year = database.Column(database.Integer, nullable=False)
    teacher_id = database.Column(database.String, database.ForeignKey('Teacher.teacher_id'))
    course_max_number = database.Column(database.Integer, nullable=True)

    def __init__(self, course_id, course_name, course_description, course_type, course_semester, course_year,
                 teacher_id, course_max_number=None):
        self.course_id = course_id
        self.course_name = course_name
        self.course_description = course_description
        self.course_type = course_type
        self.course_semester = course_semester
        self.course_year = course_year
        self.teacher_id = teacher_id
        self.course_max_number = course_max_number

    def __str__(self):
        return str(self.course_id) + ":" + self.course_name + ":" + self.course_description + ":" + \
               str(self.course_type) + ":" + str(self.course_semester) + ":" + str(self.course_year) + ":" \
               + str(self.teacher_id) + ":" + str(self.course_max_number)

    def __repr__(self):
        return str(self.course_id) + ":" + self.course_name + ":" + self.course_description + ":" + \
               str(self.course_type) + ":" + str(self.course_semester) + ":" + str(self.course_year) + ":" \
               + str(self.teacher_id) + ":" + str(self.course_max_number)