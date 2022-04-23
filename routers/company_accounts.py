from models.company_account import create_company_account
from api import get_current_active_user
from routers.token import UserModel
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pydantic.utils import GetterDict
import peewee
from typing import Any, List
from models.token import User 

router_companies_accounts = APIRouter(
    prefix="/companiesaccounts",
    tags=["companiesaccounts"]
)


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class CompanyAccountModel(BaseModel):
    userId: int
    companyId: int
    

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


@router_companies_accounts.post("/")
async def create_companies(companies_account: List[CompanyAccountModel], current_user: User = Depends(get_current_active_user)):
    temp = []
    for account in companies_account:
        temp.append(account.dict())
    result = await create_company_account(temp)
    return result
