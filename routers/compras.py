
from api import get_current_active_user
from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
from pydantic.utils import GetterDict
import peewee
from typing import Any, List, Optional
from models.compras import bulk_compra, list_compras, delete_compra, get_CompraReport
from datetime import date, datetime, time
from models.token import User
from api import get_current_active_user

router_compras = APIRouter(
    prefix="/compras",
    tags=["compras"]
)


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class CompraModel(BaseModel):
    id: int
    fecha: date
    documento: str
    tipo: str
    referencia: str
    nrc: str
    nombre: str
    compra: float
    iva: float
    guardado: datetime
    documentoId: int
    tipoId: int
    dui: str
    comInGra: float
    comInEx: float
    intExNoSuj: float
    imExNoSuj: float
    inGraBie: float
    imGravBie: float
    imGravSer: float
    attachmentId: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class CompraBulkModel(BaseModel):
    compras: List[CompraModel]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


@router_compras.get("/", response_model=List[CompraModel], summary="List of compras", description="Returns all compras")
async def get_compras(start: date, finish: date, current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    return await list_compras(start, finish, current_user, uuid)


@router_compras.get("/reporte/", summary="Resumen de compras", description="Returns all compras")
async def get_Report(start: date, finish: date, current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    return await get_CompraReport(start, finish, current_user, uuid)


@router_compras.post("/", summary="Create a new compras")
async def create(compras: List[CompraModel], current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    temp = []
    for compra in compras:
        temp.append(compra.dict())
    #     print(producto.producto)
    return await bulk_compra(items=temp, current_user=current_user, uuid=uuid)


@router_compras.delete("/", summary="Delete compras")
async def delete(comprasId: int, current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    return await delete_compra(comprasId, current_user, uuid)
