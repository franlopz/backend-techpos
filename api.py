
from typing import Optional
from pydantic import BaseModel
from crud.token import get_user
from routers.token import UserModel, Token
from constants import ALGORITHM, SECRET_KEY
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token/")


class TokenData(BaseModel):
    email: Optional[str] = None
    app_id: Optional[str] = None
    uuid: Optional[str] = None


def get_current_user(token: str = Depends(oauth2_scheme)):

    user = None

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        app_id: str = payload.get("app_id")
        uuid: str = payload.get("uuid")
        token_data = TokenData(email=email, app_id=app_id, uuid=uuid)

        if email is not None:
            if token_data.email is not None:
                user = get_user(token_data.email)
                return user

        if token_data.app_id is not None:
            return UserModel(status="active", app_id=token_data.app_id, uuid=token_data.uuid)

        raise credentials_exception

    except JWTError:
        raise credentials_exception


def get_current_active_user(current_user: UserModel = Depends(get_current_user)):

    if current_user.status == "inactive":
        raise HTTPException(status_code=400, detail="Inactive user")
    if current_user.status == "suspended":
        raise HTTPException(status_code=400, detail="Suspended user")
    return current_user
