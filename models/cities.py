from peewee import *
from .Base import BaseModel

class Cities(BaseModel):
    id = AutoField()
    stateId = IntegerField()
    name = CharField(max_length=255)

    class Meta:
        db_table = 'cities'


