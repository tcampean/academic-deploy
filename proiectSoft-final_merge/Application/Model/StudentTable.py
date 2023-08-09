#from Application.app import database
from app import database


class Student(database.Model):
    __tablename__ = "Student"
    __table_args__ = {'extend_existing': True}

    student_id = database.Column(database.Integer, primary_key=True)

    username = database.Column(database.String, database.ForeignKey('Account.username'))
    first_name = database.Column(database.String, nullable=False)
    last_name = database.Column(database.String, nullable=False)
    year = database.Column(database.Integer)
    group = database.Column(database.Integer)

    def __init__(self, username, first_name, last_name, year, group):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.year = year
        self.group = group

    def __str__(self):
        return str(self.student_id) + ":" + self.username + ":" + self.first_name + ":" + self.last_name + ":" + str(
            self.year) + str(self.group)

    def __repr__(self):
        return str(self.student_id) + ":" + self.username + ":" + self.first_name + ":" + self.last_name + ":" + str(
            self.year) + str(self.group)
