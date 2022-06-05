from peewee import *
from .Base import BaseModel

class Company(BaseModel):
    id = IntegerField()
    name = CharField(max_length=255)
    address = CharField(max_length=255)
    phone = CharField(max_length=255)
    uuid = CharField(max_length=255)
    city = CharField(max_length=255)
    state = CharField(max_length=255)

    class Meta:
        db_table = 'companies'