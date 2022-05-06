from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
from pydantic.utils import GetterDict
import peewee
from typing import Any, List, Optional
from models.producto import bulk_producto, list_productos
from datetime import date, time
from models.token import User
from api import get_current_active_user

router_productos = APIRouter(
    prefix="/productos",
    tags=["productos"]
)


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class ProductoModel(BaseModel):
    fecha: date
    hora: time
    producto: str
    porcion: str
    venta: str
    tid: int
    cantidad: float
    precio: float
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ProductoBulkModel(BaseModel):
    productos: List[ProductoModel]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


@router_productos.get("/", response_model=List[ProductoModel], summary="List of productos", description="Returns all productos")
def get_productos(start: date, finish: date, current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    return list_productos(start, finish, current_user, uuid)


@router_productos.post("/", summary="Create a new productos")
def create(productos: List[ProductoModel], current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    temp = []
    for producto in productos:
        temp.append(producto.dict())
    #     print(producto.producto)
    return bulk_producto(temp, current_user, uuid)
