#from Application.app import database
from app import database


class StudentCourse(database.Model):
    __tablename__ = "StudentCourse"
    __table_args__ = {'extend_existing': True}

    student_course_id = database.Column(database.Integer, primary_key=True)
    student_id = database.Column(database.String, database.ForeignKey('Student.student_id'))
    course_id = database.Column(database.String, database.ForeignKey('Course.course_id'))
    grade = database.Column(database.Integer, nullable=True)

    def __init__(self, student_course_id, student_id, course_id, grade):
        self.student_id = student_id
        self.student_course_id = student_course_id
        self.course_id = course_id
        self.grade = grade

    def __str__(self):
        return str(self.student_course_id) + ":" + str(self.student_id) + ":" + str(self.course_id) + ":" + str(self.grade)

    def __repr__(self):
        return str(self.student_course_id) + ":" + str(self.student_id) + ":" + str(self.course_id) + ":" + str(self.grade)
