from datetime import datetime 
from models.token import User
from models.users import create_users, delete_users, generateFakePass, get_app_credentials, get_users, modify_users, change_password
from api import get_current_active_user
from routers.token import UserModel
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from pydantic.utils import GetterDict
import peewee
from typing import Any, List, Optional

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
async def post_users(users: List[UsersModel], current_user: User = Depends(get_current_active_user)):
    result = await create_users(users, current_user)
    return {"message": result}


@router_users.post("/changepassword/")
async def post_users(form: Password_form, current_user: User = Depends(get_current_active_user)):

    result = await change_password(form, current_user)

    return {"message": result}

@router_users.get("/")
async def fetch_users(current_user: User = Depends(get_current_active_user)):
    response = await get_users(current_user)
    return response

@router_users.get("/appcredential/")
async def fetch(current_user: User = Depends(get_current_active_user)):
    response = await get_app_credentials(current_user)
    return response

@router_users.patch("/")
async def patch_users(users: List[UsersModel], current_user: User = Depends(get_current_active_user)):
    response = await modify_users(users, current_user)
    return response


@router_users.delete("/")
async def delete(users: List[UsersModel], current_user: User = Depends(get_current_active_user)):
    response = await delete_users(users, current_user)
    return response
