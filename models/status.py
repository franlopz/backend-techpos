from peewee import *
from .Base import BaseModel

class Status(BaseModel):
    id = IntegerField()
    name = CharField(max_length=45)

    class Meta:
        db_table = 'status'