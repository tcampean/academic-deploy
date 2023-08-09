#from Application.app import database
from app import database


class Department(database.Model):
    __tablename__ = "Department"
    __table_args__ = {'extend_existing': True}
    department_id = database.Column(database.Integer, primary_key=True)
    department_name = database.Column(database.String, nullable=False)

    def __init__(self, department_id, department_name):
        self.department_id = department_id
        self.department_name = department_name

    def __str__(self):
        return str(self.department_id) + ":" + self.department_name

    def __repr__(self):
        return str(self.department_id) + ":" + self.department_name
