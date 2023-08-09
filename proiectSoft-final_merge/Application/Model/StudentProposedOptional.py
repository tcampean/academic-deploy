#from Application.app import database
from app import database


class StudentProposedOptional(database.Model):
    __tablename__ = "StudentProposedOptional"
    __table_args__ = {'extend_existing': True}

    student_optional_id = database.Column(database.Integer, primary_key=True)
    student_id = database.Column(database.String, database.ForeignKey('StudentTable.student_id'))
    optional_id = database.Column(database.String, database.ForeignKey('Course.course_id'))

    def __init__(self, student_optional_id, student_id, optional_id):
        self.student_id = student_id
        self.student_optional_id = student_optional_id
        self.optional_id = optional_id

    def __str__(self):
        return str(self.student_optional_id) + ":" + str(self.student_id) + ":" + str(self.optional_id)

    def __repr__(self):
        return str(self.student_optional_id) + ":" + str(self.student_id) + ":" + str(self.optional_id)
