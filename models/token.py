from cmath import exp
from constants import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from database import *
from peewee import *
from .Base import BaseModel
from passlib.context import CryptContext
from models.company_account import Company_account
import models.company


class User(BaseModel):
    id = IntegerField()
    email = CharField(max_length=255)
    firstName = CharField(max_length=255)
    lastName = CharField(max_length=255)
    passwordSalt = CharField(max_length=255)
    passwordHash = CharField(max_length=255)
    createdDate = DateTimeField()
    status = CharField(max_length=255)
    loginTries = IntegerField()
    roleId = IntegerField()

    class Meta:
        db_table = 'users'


class Client_credential(BaseModel):
    id = IntegerField()
    app_id = CharField(max_length=255)
    app_key = CharField(max_length=255)

    class Meta:
        db_table = 'client_credential'


class UserInDB(User):
    passwordHash: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(email: str):
    if conn.is_closed():
        conn.connect()
    user = list(User.select().where(User.email == email))
    if not conn.is_closed():
        conn.close()
    if(user):
        return user[0]
    else:
        return


async def verify_password(password, hashed_password, password_salt):
    return pwd_context.verify(password+password_salt, hashed_password)


async def auth_app(app_id: str, app_key: str):

    data = {}

    company_account = None

    client = Client_credential.get_or_none(
        Client_credential.app_id == app_id,
        Client_credential.app_key == app_key
    )

    if client is None:
        return False

    company_account = Company_account.get_or_none(
        Company_account.appId == client.app_id)

    company = models.company.Company.get_or_none(
        models.company.Company.id == company_account.companyId
    )

    data.update({
        "app_id": client.app_id,
        "uuid": company.uuid
    })

    return data


async def auth_user(email: str, password: str):

    user = await get_user(email)
    if not user:
        return False
    if not await verify_password(password, user.passwordHash, user.passwordSalt):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    print(type(expire), expire)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encoded_jwt, "expire": expire, "expires_in": expires_delta}
