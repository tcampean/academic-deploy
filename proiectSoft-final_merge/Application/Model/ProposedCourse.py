#from Application.app import database
from app import database


class ProposedCourse(database.Model):
    __tablename__ = "ProposedCourse"
    __table_args__ = {'extend_existing': True}

    proposed_course_id = database.Column(database.Integer, primary_key=True)
    proposed_course_name = database.Column(database.String, nullable=False)
    proposed_course_description = database.Column(database.String, nullable=False)
    proposed_course_type = database.Column(database.Integer, nullable=False)  # obligatorii = 1/optionale = 0
    proposed_course_semester = database.Column(database.Integer, nullable=False)
    proposed_course_year = database.Column(database.Integer, nullable=False)
    teacher_id = database.Column(database.String, database.ForeignKey('Teacher.teacher_id'))
    proposed_course_max_number = database.Column(database.Integer, nullable=True)

    def __init__(self, proposed_course_id, proposed_course_name, proposed_course_description, proposed_course_type,
                 proposed_course_semester, proposed_course_year, teacher_id, proposed_course_max_number=None):
        self.proposed_course_id = proposed_course_id
        self.proposed_course_name = proposed_course_name
        self.proposed_course_description = proposed_course_description
        self.proposed_course_type = proposed_course_type
        self.proposed_course_semester = proposed_course_semester
        self.proposed_course_year = proposed_course_year
        self.teacher_id = teacher_id
        self.proposed_course_max_number = proposed_course_max_number

    def __str__(self):
        return str(
            self.proposed_course_id) + ":" + self.proposed_course_name + ":" + self.proposed_course_description + ":" + str(
            self.proposed_course_type) + ":" + str(self.proposed_course_semester) + ":" + str(
            self.proposed_course_year) + ":" + str(self.teacher_id) + ":" + str(self.proposed_course_max_number)

    def __repr__(self):
        return str(
            self.proposed_course_id) + ":" + self.proposed_course_name + ":" + self.proposed_course_description + ":" + str(
            self.proposed_course_type) + ":" + str(self.proposed_course_semester) + ":" + str(
            self.proposed_course_year) + ":" + str(self.teacher_id) + ":" + str(self.proposed_course_max_number)
