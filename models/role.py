from models.users import Users
from peewee import *
from .Base import BaseModel
from database import *


class Role(BaseModel):
    id = IntegerField()
    roleName = CharField(max_length=255)

    class Meta:
        db_table = 'roles'


def create_role(role):
    if conn.is_closed():
        conn.connect()
    roles_inserted = Role.insert_many(role).execute()
    if not conn.is_closed():
        conn.close()
    return roles_inserted


def get_user_role(role_id):
    if conn.is_closed():
        conn.connect()
    role = Users.select().where(Users.roleId == role_id).get()
    if not conn.is_closed():
        conn.close()
    return role


def get_roles(userId):
    if conn.is_closed():
        conn.connect()
    roles_list = list(Role.select().where(Role.id <= userId))
    if not conn.is_closed():
        conn.close()
    return roles_list
