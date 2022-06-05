from fastapi import HTTPException
from database import *
import secrets
from models.client_credential import Client_credential
from models.company import Company
from models.company_account import Company_account
from models.role import Role

def create_company(companies, current_user):
    if current_user.roleId != 1:
        raise HTTPException(status_code=403, detail="Cannot create company")

    result = Company.insert_many(companies).execute()
    for company in companies:
        app_id = secrets.token_hex(16)
        app_key = secrets.token_urlsafe(16)
        Client_credential.insert(app_key=app_key, app_id=app_id).execute()
        current_company = Company.get_or_none(Company.uuid == company['uuid'])
        Company_account.insert(
            companyId=current_company.id, appId=app_id).execute()
        print(app_id, app_key, current_company.id)


    return result


def get_companies(current_user):

    data = {}
    companies = []
    roles_result = []



    if current_user.roleId == 1:
        companies_result = list(Company.select())
        roles_result = list(Role.select())
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
            roles_result = list(Role
                                .select()
                                .where(current_user.roleId <= Role.id))

            companies.append(result[0])

        data = {
            "companies": companies,
            "roles": roles_result
        }


    return data
