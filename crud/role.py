from database import *
from models.role import Role
from models.user import User

def create_role(role):

    roles_inserted = Role.insert_many(role).execute()

    return roles_inserted

def get_user_role(role_id):

    role = User.select().where(User.roleId == role_id).get()

    return role

def get_roles(userId):

    roles_list = list(Role.select().where(Role.id <= userId))

    return roles_list