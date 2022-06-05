from peewee import *
from .Base import BaseModel

class User(BaseModel):
    email = CharField(max_length=255)
    firstName = CharField(max_length=255)
    lastName = CharField(max_length=255)
    passwordSalt = CharField(max_length=255)
    passwordHash = CharField(max_length=255)
    createdDate = DateTimeField()
    status = CharField(max_length=255)
    loginTries = IntegerField()
    roleId = IntegerField()

    class Meta:
        db_table = 'users'