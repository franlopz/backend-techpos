from cmath import exp
from crud.company import get_companies
from crud.token import auth_app, auth_user, create_access_token
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from pydantic.utils import GetterDict
import peewee
from typing import Any, Dict, List, Optional
from datetime import date, datetime, time, timedelta
from fastapi.param_functions import Form

router_token = APIRouter(
    prefix="/token",
    tags=["token"],
    include_in_schema=False,
    redirect_slashes=False
)


class OAuth2ClientCredentialsRequestForm:

    def __init__(
        self,
        username: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
        grant_type: Optional[str] = Form('password'),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        self.username = username
        self.password = password
        self.grant_type = grant_type
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class UserModel(BaseModel):
    id: Optional[int]
    email: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    passwordSalt: Optional[str]
    passwordHash: Optional[str]
    createdDate: Optional[datetime]
    status: Optional[str]
    loginTries: Optional[int]
    roleId: Optional[int]
    app_id: Optional[str]
    uuid: Optional[str]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


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


class Token(BaseModel):
    access_token: str
    token_type: str
    expire: datetime
    expires_in: timedelta
    companies: Optional[List[CompanyModel]]

    class Config:
        arbitrary_types_allowed = True


@router_token.post('/', response_model=Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends(),
def login(form_data: OAuth2ClientCredentialsRequestForm = Depends()):
    user = None

    print(form_data)

    if form_data.grant_type == "client_credentials":

        client_data = auth_app(form_data.client_id, form_data.client_secret)

        if not client_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        dataToken = create_access_token(
            data=client_data, expires_delta=timedelta(minutes=30))

        return {**dataToken, "token_type": "bearer"}

    if form_data.grant_type == "password":
        user = auth_user(form_data.username, form_data.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        companies = get_companies(user)
        dataToken = create_access_token(
            data={"email": user.email,
                  "roleId": user.roleId},
            expires_delta=timedelta(weeks=2)
        )

        return {**dataToken, "token_type": "bearer", "companies": companies["companies"]}
