#from Application.app import database
from app import database
from flask_login import UserMixin


class Account(UserMixin, database.Model):
    __tablename__ = "Account"
    __table_args__ = {'extend_existing': True}

    id_user = database.Column(database.Integer, primary_key=True)
    access_level = database.Column(database.String, nullable=False)
    username = database.Column(database.String, unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    password = database.Column(database.String, nullable=False)

    def __init__(self, username, password, email, access_level):
        self.username = username
        self.password = password
        self.email = email
        self.access_level = access_level

    def __str__(self):
        return self.username + ":" + str(self.password)

    def __repr__(self):
        return self.username + ":" + str(self.password)

    def get_id(self):
        return self.id_user
