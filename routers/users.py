from crud.token import User
from api import get_current_active_user
from fastapi import APIRouter, Depends 
from pydantic import BaseModel
from pydantic.utils import GetterDict
import peewee
from typing import Any, List, Optional

from crud.user import change_password, create_users, delete_users, get_app_credentials, get_users, modify_users

router_users = APIRouter(
    prefix="/users",
    tags=["users"],
    redirect_slashes=False
)

router_users.redirect_slashes = False


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class UsersModel(BaseModel):
    email: str
    lastName: str
    firstName: str
    role: str
    uuid: Optional[str]
    statusEn: Optional[str]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class Password_form(BaseModel):
    password: str
    newpassword: str
    passwordconfirm: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


@router_users.post("/")
def post_users(users: List[UsersModel], current_user: User = Depends(get_current_active_user)):
    result = create_users(users, current_user)
    return {"message": result}


@router_users.post("/changepassword/")
def post_users(form: Password_form, current_user: User = Depends(get_current_active_user)):

    result = change_password(form, current_user)

    return {"message": result}


@router_users.get("/")
def fetch_users(current_user: User = Depends(get_current_active_user)):
    response = get_users(current_user)
    return response


@router_users.get("/appcredential/")
def fetch(current_user: User = Depends(get_current_active_user)):
    response = get_app_credentials(current_user)
    return response


@router_users.patch("/")
def patch_users(users: List[UsersModel], current_user: User = Depends(get_current_active_user)):
    response = modify_users(users, current_user)
    return response


@router_users.delete("/")
def delete(users: List[UsersModel], current_user: User = Depends(get_current_active_user)):
    response = delete_users(users, current_user)
    return response
