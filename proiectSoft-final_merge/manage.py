# def deploy():
#     from Application.Model.TeacherTable import Teacher
#     from Application.Model import AccountsTable
#     from Application.Model import Staff
#     from Application.Model.Department import Department
#     from Application.Model import StudentTable
#     from Application.Model import Course
#     from Application.Model import StudentCourse
#     from Application.app import create_app, database
#
#     app = create_app()
#     app.app_context().push()
#     database.create_all()
#
#     # mate_info = Department(department_id=1, department_name='Matematica-Informatica')
#     # psiho = Department(department_id=2, department_name='Psihologie')
#     # drept = Department(department_id=3, department_name='Drept')
#     # conta = Department(department_id=4, department_name='Contabilitate')
#     # info_economica = Department(department_id=5, department_name='Informatica-Economica')
#
#     # database.session.add(mate_info)
#     # database.session.add(psiho)
#     # database.session.add(drept)
#     # database.session.add(conta)
#     # database.session.add(info_economica)
#     # database.session.add(Teacher('username', 'Mihai', 'Mihai', 1, 1))
#     #
#     # database.session.add(Course.Course(1, "Software Engineering", "Creating a web app", 1, 1, 2, 4))
#     # database.session.add(Course.Course(2, "Databases", "Learning how to work with ssms", 1, 2, 2, 9))
#     #
#     # database.session.add(Course.Course(3, "Computer Network", "Send viruses ", 1, 2, 16, 9))
#     #
#     # database.session.add(Course.Course(4, "AMazing course", "grergerg", 1, 1, 2, 16, 10))
#     # database.session.add(Course.Course(5, "Grilling", "Amazing grilling", 1, 2, 2, 16, 10))
#
#     database.session.commit()
#
#
# deploy()
