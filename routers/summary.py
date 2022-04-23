from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
from pydantic.utils import GetterDict
import peewee
from typing import Any, List, Dict
from models.summary import get_summary
from datetime import date, time
from typing import Optional
from models.token import User
from api import get_current_active_user


router_summary = APIRouter(
    prefix="/summary",
    tags=["summary"]
)


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class summary(BaseModel):
    summary: Optional[List]
    bytype: Dict
    byhour: Dict
    bytypeporc: Dict
    bypayment: List
    byitem: List

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


@router_summary.get("/", response_model=summary, summary="List of tickets", description="Returns all tickets")
async def get_tickets(start: date, finish: date, current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    response = await get_summary(start, finish, current_user, uuid)
    return response
