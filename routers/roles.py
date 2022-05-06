from models.token import User
from models.role import create_role, get_roles, get_user_role
from api import get_current_active_user
from routers.token import UserModel
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pydantic.utils import GetterDict
import peewee
from typing import Any, List

router_roles = APIRouter(
    prefix="/roles",
    tags=["roles"]
)


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class RolesModel(BaseModel):
    id: int
    roleName: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


@router_roles.post("/")
def create_roles(roles: List[RolesModel], current_user: User = Depends(get_current_active_user)):
    temp = []
    for role in roles:
        temp.append(role.dict())
    #     print(producto.producto)
    print(temp)
    result = create_role(temp)
    return result


@router_roles.get("/", response_model=List[RolesModel])
def fetch_roles(userId: int, current_user: User = Depends(get_current_active_user)):
    result = get_roles(userId)
    return result


@router_roles.get("/user/", response_model=UserModel)
def fetch_roles(current_user: User = Depends(get_current_active_user)):
    result = get_user_role(current_user.roleId)
    return result
