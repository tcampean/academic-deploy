#from Application.app import database
from app import database


class Staff(database.Model):
    __tablename__ = "Staff"
    __table_args__ = {'extend_existing': True}

    staff_id = database.Column(database.Integer, primary_key=True)

    username = database.Column(database.String, database.ForeignKey('Account.username'))
    first_name = database.Column(database.String, nullable=False)
    last_name = database.Column(database.String, nullable=False)

    def __init__(self, username, first_name, last_name):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return self.username + ":" + self.first_name + ":" + self.last_name

    def __repr__(self):
        return self.username + ":" + self.first_name + ":" + self.last_name
