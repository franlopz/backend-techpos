from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
from pydantic.utils import GetterDict
import peewee
from typing import Any, List, Optional
from datetime import date, datetime
from crud.expense import bulk_gastos, delete_gasto, list_gasto
from crud.token import User
from api import get_current_active_user


router_gastos = APIRouter(
    prefix="/gastos",
    tags=["gastos"]
)


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class GastoModel(BaseModel):
    fecha: date
    tipo: str
    monto: float
    descripcion: str
    id: int
    guardado: datetime

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class GastoBulkModel(BaseModel):
    gastos: List[GastoModel]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


@router_gastos.get("/", response_model=List[GastoModel], summary="List of gastos", description="Returns all gastos")
def get_gastos(start: date, finish: date, current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    return list_gasto(start, finish, current_user, uuid)


@router_gastos.post("/", summary="Create a new gastos")
def create(gastos: List[GastoModel], current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    temp = []
    for gasto in gastos:
        temp.append(gasto.dict())
    #     print(producto.producto)
    return bulk_gastos(temp, current_user, uuid)


@router_gastos.delete("/", summary="Delete gastos")
def delete(gastosId: int, current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    return delete_gasto(gastosId, current_user, uuid)
