from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
from pydantic.utils import GetterDict
import peewee
from typing import Any, List, Optional
from models.proveedores import bulk_proveedores, list_proveedor
from datetime import date, datetime, time
from models.token import User
from api import get_current_active_user

router_proveedores = APIRouter(
    prefix="/proveedores",
    tags=["proveedores"]
)


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class ProveedorModel(BaseModel):
    nombre: str
    nrc: str
    guardado: datetime
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ProveedorBulkModel(BaseModel):
    proveedores: List[ProveedorModel]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


@router_proveedores.get("/", response_model=List[ProveedorModel], summary="List of proveedores", description="Returns all proveedores")
def get_proveedores(current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    return list_proveedor(current_user,uuid)


@router_proveedores.post("/", summary="Create a new proveedores")
async def create(proveedores: List[ProveedorModel], current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    temp = []
    for proveedor in proveedores:
        temp.append(proveedor.dict())
    #     print(producto.producto)
    return await bulk_proveedores(temp,current_user,uuid)
