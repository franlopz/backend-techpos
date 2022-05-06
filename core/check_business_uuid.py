from models.company import Company
from fastapi import HTTPException
from models.company_account import Company_account


def valid_uuid(user, uuid):

    if user.id is not None:
        company_account = Company_account.get_or_none(
            Company_account.userId == user.id)
        company = Company.get_or_none(Company.id == company_account.companyId)
        if company.uuid == uuid:
            return True
        else:
            raise HTTPException(status_code=400, detail="uuid not valid")

    if user.app_id is not None and user.uuid == uuid:
        return True
    else:
        raise HTTPException(status_code=400, detail="uuid not valid")
