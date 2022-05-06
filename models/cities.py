from peewee import *
from .Base import BaseModel
from database import *


class Cities(BaseModel):
    id = IntegerField()
    stateId = IntegerField()
    name = CharField(max_length=255)

    class Meta:
        db_table = 'cities'


def create_cities(cities):
    if conn.is_closed():
        conn.connect()
    Cities.insert_many(cities).execute()
    if not conn.is_closed():
        conn.close()
    return
