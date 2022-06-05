from peewee import *
from .Base import BaseModel

class Company_account(BaseModel):
    userId = IntegerField()
    companyId = IntegerField()
    appId = CharField(max_length=255)

    class Meta:
        db_table = 'companyaccount'
