import models.role
from models.company_account import Company_account
from peewee import *
from .Base import BaseModel
from database import *
from fastapi import HTTPException
import secrets


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


class Client_credential(BaseModel):
    id = IntegerField()
    app_id = CharField(max_length=255)
    app_key = CharField(max_length=255)

    class Meta:
        db_table = 'client_credential'


def create_company(companies, current_user):
    if current_user.roleId != 1:
        raise HTTPException(status_code=403, detail="Cannot create company")
    if conn.is_closed():
        conn.connect()
    result = Company.insert_many(companies).execute()
    for company in companies:
        app_id = secrets.token_hex(16)
        app_key = secrets.token_urlsafe(16)
        Client_credential.insert(app_key=app_key, app_id=app_id).execute()
        current_company = Company.get_or_none(Company.uuid == company['uuid'])
        Company_account.insert(
            companyId=current_company.id, appId=app_id).execute()
        print(app_id, app_key, current_company.id)

    if not conn.is_closed():
        conn.close()
    return result


def get_companies(current_user):

    data = {}
    companies = []
    roles_result = []

    if conn.is_closed():
        conn.connect()

    if current_user.roleId == 1:
        companies_result = list(Company.select())
        roles_result = list(models.role.Role.select())
        companies = companies_result
        data = {
            "companies": companies_result,
            "roles": roles_result
        }
    else:
        company_accounts = list(
            Company_account
            .select(Company_account.companyId.alias('id'))
            .where(current_user.id == Company_account.userId)
        )

        for company_account in company_accounts:
            result = list(
                Company
                .select()
                .where(Company.id == company_account.id)
            )
            roles_result = list(models.role.Role
                                .select()
                                .where(current_user.roleId <= models.role.Role.id))

            companies.append(result[0])

        data = {
            "companies": companies,
            "roles": roles_result
        }

    if not conn.is_closed():
        conn.close()
    return data
