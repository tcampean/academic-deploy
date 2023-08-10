import os
import pymysql

db_user = os.environ.get("CLOUD_SQL_USERNAME")
db_password = os.environ.get("CLOUD_SQL_PASSWORD")
db_name = os.environ.get("CLOUD_SQL_DATABASE_NAME")
db_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")


def open_connection():
    socket = '/cloudsql/{}'.format(db_connection_name)
    connection = ''
    try:
        if os.environ.get("GAE_ENV") == 'standard':
            connection = pymysql.connect(user=db_user,
                                         password=db_password,
                                         unix_socket=socket,
                                         db=db_name,
                                         cursorclass=pymysql.cursors.DictCursor
                                         )
    except pymysql.MySQLError as e:
        return e
    return connection


def register_student(new_user):
    conn = open_connection()
    insert_account = "INSERT INTO accounts (access_level, username, password, email) VALUES(%s, %s, %s, %s)"
    with conn.cursor() as cursor:
        cursor.execute(insert_account, (new_user.access_level, new_user.username, new_user.password, new_user.email))
    conn.commit()
    conn.close()


def complete_student(student):
    conn = open_connection()
    insert_student = "INSERT INTO students (username, first_name, last_name, student_year, student_group) VALUES(%s, %s, %s, %s, %s)"
    with conn.cursor() as cursor:
        cursor.execute(insert_student, (student.username, student.first_name, student.last_name, str(1), str(912)))
    conn.commit()
    conn.close()

def check_user(email):
    conn = open_connection()
    get_account = "SELECT * FROM accounts WHERE email = %s LIMIT 1"
    result = None
    with conn.cursor() as cursor:
        cursor.execute(get_account, email)
        result = cursor.fetchone()
    conn.commit()
    conn.close()
    return result


def get_student_info(username):
    conn = open_connection()
    get_account = "SELECT * FROM students WHERE username = %s LIMIT 1"
    result = None
    with conn.cursor() as cursor:
        cursor.execute(get_account, username)
        result = cursor.fetchone()
    conn.commit()
    conn.close()
    return result

def get_user_info(username):
    conn = open_connection()
    get_account = "SELECT * FROM accounts WHERE username = %s LIMIT 1"
    result = None
    with conn.cursor() as cursor:
        cursor.execute(get_account, username)
        result = cursor.fetchone()
    conn.commit()
    conn.close()
    return result
