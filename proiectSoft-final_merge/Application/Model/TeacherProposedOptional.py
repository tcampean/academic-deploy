#from Application.app import database
from app import database

class TeacherProposedOptional(database.Model):
    __tablename__ = "TeacherProposedOptional"
    __table_args__ = {'extend_existing': True}

    teacher_optional_id = database.Column(database.Integer, primary_key=True)
    teacher_id = database.Column(database.String, database.ForeignKey('TeacherTable.student_id'))
    optional_id = database.Column(database.String, database.ForeignKey('Course.course_id'))  # dummy value

    def __init__(self, teacher_optional_id, teacher_id, optional_id):
        self.teacher_id = teacher_id
        self.teacher_optional_id = teacher_optional_id
        self.optional_id = optional_id

    def __str__(self):
        return str(self.teacher_optional_id) + ":" + str(self.teacher_id) + ":" + str(self.optional_id)

    def __repr__(self):
        return str(self.teacher_optional_id) + ":" + str(self.teacher_id) + ":" + str(self.optional_id)
