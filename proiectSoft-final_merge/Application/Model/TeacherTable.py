#from Application.app import database
from app import database

class Teacher(database.Model):
    __tablename__ = "Teacher"
    __table_args__ = {'extend_existing': True}
    teacher_id = database.Column(database.Integer, primary_key=True)

    username = database.Column(database.String, database.ForeignKey('Account.username'))
    first_name = database.Column(database.String, nullable=False)
    last_name = database.Column(database.String, nullable=False)
    department = database.Column(database.Integer, database.ForeignKey('Department.department_id'))
    chief_department = database.Column(database.Integer, nullable=False)  # true/false

    def __init__(self, username, first_name, last_name, chief, department):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.chief_department = chief
        self.department = department

    def __str__(self):
        return self.username + ":" + self.first_name + ":" + self.last_name + ":" + str(self.chief_department)

    def __repr__(self):
        return self.username + ":" + self.first_name + ":" + self.last_name + ":" + str(self.chief_department)
