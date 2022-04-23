from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
from pydantic.utils import GetterDict
import peewee
from typing import Any, List, Dict
from models.ticket import bulk_tickets, list_tickets, summary
from datetime import date, time
from typing import Optional
from models.token import User
from api import get_current_active_user


router_tickets = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class TicketModel(BaseModel):
    id: int
    fecha: date
    hora: time
    total: float
    tipo: str
    documento: str
    puntosLealtad: str
    correlativo: int
    descuentoTotal: float
    propina: float
    descuentoLealtad: float
    servicioDomicilio: float
    cliente: str
    mesa: str
    anulado: str
    mesero: str
    tid: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class TicketBulkModel(BaseModel):
    tickets: List[TicketModel]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


@router_tickets.get("/", response_model=List[TicketModel], summary="List of tickets", description="Returns all tickets")
async def get_tickets(start: date, finish: date, current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    response = await list_tickets(start, finish, current_user, uuid)
    return response


@router_tickets.post("/", summary="Create a new tickets")
async def create(tickets: List[TicketModel], current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    temp = []
    for ticket in tickets:
        temp.append(ticket.dict())
    #     print(producto.producto)
    response = await bulk_tickets(temp, current_user, uuid)
    return response


@router_tickets.get("/summary/", summary="Create a new tickets")
async def get(start: date, finish: date, current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):

    response = await summary(start, finish, current_user, uuid)

    return response
