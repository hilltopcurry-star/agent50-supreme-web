from extensions import db
from models import User, Project, File, ApiLog

class UserCRUD:
    @staticmethod
    def create_user(username, email, password, role='customer'):
        try:
            new_user = User(username=username, email=email, role=role)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(int(user_id))

class ProjectCRUD:
    @staticmethod
    def create_project(name, user_id, description=None):
        try:
            project = Project(name=name, user_id=user_id, description=description)
            db.session.add(project)
            db.session.commit()
            return project
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def add_file_to_project(project_id, filename, content):
        try:
            new_file = File(project_id=project_id, filename=filename, content=content)
            db.session.add(new_file)
            db.session.commit()
            return new_file
        except Exception as e:
            db.session.rollback()
            raise e

def get_database_stats():
    try:
        return {
            "users": User.query.count(),
            "projects": Project.query.count(),
            "logs": ApiLog.query.count()
        }
    except:
        return {"users": 0, "projects": 0, "logs": 0}