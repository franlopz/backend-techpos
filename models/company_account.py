from peewee import *
from .Base import BaseModel
from database import *


class Company_account(BaseModel):
    userId = IntegerField()
    companyId = IntegerField()
    appId = CharField(max_length=255)

    class Meta:
        db_table = 'companyaccount'


async def create_company_account(company_account):
    if conn.is_closed():
        conn.connect()
    companies_inserted = Company_account.insert_many(company_account).execute()
    if not conn.is_closed():
        conn.close()
    return companies_inserted

