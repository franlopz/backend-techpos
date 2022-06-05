from constants import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from database import *
from peewee import *
from models.client_credential import Client_credential
from passlib.context import CryptContext
from models.company_account import Company_account
import models.company
from models.user import User

class UserInDB(User):
    passwordHash: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(email: str):

    user = list(User.select().where(User.email == email))

    if(user):
        return user[0]
    else:
        return


def verify_password(password, hashed_password, password_salt):
    return pwd_context.verify(password+password_salt, hashed_password)


def auth_app(app_id: str, app_key: str):

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


def auth_user(email: str, password: str):

    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.passwordHash, user.passwordSalt):
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
