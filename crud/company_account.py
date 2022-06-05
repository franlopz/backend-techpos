from database import *
from models.company_account import Company_account

def create_company_account(company_account):

    companies_inserted = Company_account.insert_many(company_account).execute()

    return companies_inserted
