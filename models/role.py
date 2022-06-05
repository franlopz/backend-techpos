from peewee import *
from .Base import BaseModel

class Role(BaseModel):
    id = IntegerField()
    roleName = CharField(max_length=255)

    class Meta:
        db_table = 'roles'