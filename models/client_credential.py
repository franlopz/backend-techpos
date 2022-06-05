from peewee import *
from .Base import BaseModel
from database import *

class Client_credential(BaseModel):
    id = AutoField()
    app_id = CharField(max_length=255)
    app_key = CharField(max_length=255)

    class Meta:
        db_table = 'client_credential'