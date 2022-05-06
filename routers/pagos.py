from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
from pydantic.utils import GetterDict
import peewee
from typing import Any, List, Optional
from models.pago import bulk_pagos, list_pagos
from datetime import date, time
from models.token import User
from api import get_current_active_user


router_pagos = APIRouter(
    prefix="/pagos",
    tags=["pagos"]
)


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class PagoModel(BaseModel):
    fecha: date
    hora: time
    tipoPago: str
    pago: float
    caja: str
    usuario: str
    correlativo: int
    id: int
    anulado: str
    iva: float
    tid: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class PagoBulkModel(BaseModel):
    pagos: List[PagoModel]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


@router_pagos.get("/", response_model=List[PagoModel], summary="List of pagos", description="Returns all pagos")
def get_pagos(start: date, finish: date, current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    return list_pagos(start, finish, current_user, uuid)


@router_pagos.post("/", summary="Create a new pagos")
def create(pagos: List[PagoModel], current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    temp = []
    for pago in pagos:
        temp.append(pago.dict())
    #     print(producto.producto)
    return bulk_pagos(temp, current_user, uuid)
