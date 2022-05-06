from routers.roles import RolesModel
from models.token import User
from models.company import create_company, get_companies
from api import get_current_active_user
from routers.token import UserModel
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pydantic.utils import GetterDict
import peewee
from typing import Any, Dict, List, Optional
import uuid

router_companies = APIRouter(
    prefix="/companies",
    tags=["companies"]
)


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class CompanyModel(BaseModel):
    name: str
    address: str
    phone: str
    city: str
    state: str
    uuid: Optional[str]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class NewUserData(BaseModel):
    companies: List[CompanyModel]
    roles: List[RolesModel]


@router_companies.post("/")
def create_companies(companies: List[CompanyModel], current_user: User = Depends(get_current_active_user)):
    temp = []
    for company in companies:
        data = company.dict()
        data['uuid'] = uuid.uuid4()
        temp.append(data)

    result = create_company(temp, current_user)
    return result


@router_companies.get("/", response_model=NewUserData)
def fetch_companies(current_user: User = Depends(get_current_active_user)):
    result = get_companies(current_user)
    return result
