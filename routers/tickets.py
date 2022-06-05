from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, validator
from pydantic.utils import GetterDict
import peewee
from typing import Any, List
from datetime import date, datetime, time
from typing import Optional
from crud.ticket import bulk_tickets, list_tickets, non_tax_report, tax_payer_sales, voided_sales
from crud.token import User
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
    docTipo: Optional[str]
    docTipoId: Optional[int]
    docId: Optional[str]
    numResolucion: Optional[str]
    docSerie: Optional[str]
    venEx: Optional[float]
    venNoSuj: Optional[float]
    venGrabLoc: Optional[float]
    venCueTerNoDom: Optional[float]
    anexoNum: Optional[int]
    nrc: Optional[str]
    nombre: Optional[str]
    dui: Optional[str]
    maqNum: Optional[str]
    venIntExNoSujProp: Optional[float]
    expDenCA: Optional[float]
    expFueCA: Optional[float]
    expSer: Optional[float]
    venZoFra: Optional[float]
    tax: Optional[float]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

    @validator('descuentoTotal',
               'propina',
               'descuentoLealtad',
               'servicioDomicilio')
    def result_check(cls, v):
        ...
        return round(v, 2)


class nonTaxPayerSale(BaseModel):
    date: date
    type: int
    document: str
    resolution: str
    serie: str
    first_company_doc_number: int
    last_company_doc_number: int
    first_gob_doc_number: int
    last_gob_doc_number: int
    machine: str
    ex_sale: float
    int_ex_sale: float
    non_sub_sale: float
    taxed_sale: float
    exp_in_ca: float
    exp_out_ca: float
    exp_services: float
    imp_zone_sale: float
    third_sale: float
    total: float
    append: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

    @validator('ex_sale',
               'int_ex_sale',
               'non_sub_sale',
               'taxed_sale',
               'exp_in_ca',
               'exp_out_ca',
               'exp_services',
               'imp_zone_sale',
               'third_sale',
               'total'
               )
    def result_check(cls, v):
        ...
        return round(v, 2)

    @validator('date')
    def result_date(cls, v):
        year = v.strftime("%Y")
        day = v.strftime("%d")
        month = v.strftime("%m")
        return day + '/'+month+'/'+year


class taxPayerSales(BaseModel):
    date: date
    type: int
    document: str
    resolution: str
    serie: str
    gob_doc_number: int
    company_doc_number: int
    nrc: str
    name: str
    ex_sale: float
    non_sub_sale: float
    taxable_sale: float
    tax: float
    third_non_dom_sale: float
    third_non_dom_tax_sale: float
    total: float
    dui: str
    append: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

    @validator('ex_sale',
               'non_sub_sale',
               'taxable_sale',
               'third_non_dom_sale',
               'third_non_dom_tax_sale',
               )
    def result_check(cls, v):
        ...
        return round(v, 2)

    @validator('tax')
    def result_tax(cls, v):
        return round((1-1/1.13)*v, 2)

    @validator('date')
    def result_date(cls, v):
        year = v.strftime("%Y")
        day = v.strftime("%d")
        month = v.strftime("%m")
        return day + '/'+month+'/'+year

    @validator('total')
    def final_total(cls, v, values, **kwargs):
        return round(v+values['tax'], 2)

    @validator('nrc',
               'dui')
    def remove_string(cls, v):
        return v.replace("-", "")


class voidedSales(BaseModel):
    resolution: str
    type: str
    first_gob_doc_number: Optional[str] = ""
    last_gob_doc_number: Optional[str] = ""
    document: str
    detail: Optional[str] = "A"
    serie: str
    first_company_doc_number: int
    last_company_doc_number: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
        validate_assignment = True

    @validator('detail')
    def result_detail(cls, v):
        return v or 'A'

    @validator('first_gob_doc_number', 'last_company_doc_number')
    def result_doc_number(cls, v):
        return v or ''


class appendResult(BaseModel):
    non_tax_payer: List[nonTaxPayerSale]
    tax_payer: List[taxPayerSales]
    voided_sales: List[voidedSales]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


@router_tickets.get("/", response_model=List[TicketModel], summary="List of tickets", description="Returns all tickets")
def get_tickets(start: date, finish: date, current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    response = list_tickets(start, finish, current_user, uuid)
    return response


@router_tickets.post("/", summary="Create a new tickets")
def create(tickets: List[TicketModel], current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):
    temp = []
    for ticket in tickets:
        temp.append(ticket.dict())
    #     print(producto.producto)
    print(temp)
    response = bulk_tickets(temp, current_user, uuid)
    return response


@router_tickets.get("/taxappends/", response_model=appendResult)
def get(start: date, finish: date, current_user: User = Depends(get_current_active_user), uuid: Optional[str] = Header(None)):

    response_non_tax_payer = non_tax_report(start, finish, current_user, uuid)
    response_tax_payer = tax_payer_sales(start, finish, current_user, uuid)
    response_voided_sales = voided_sales(start, finish, current_user, uuid)
    return {'non_tax_payer': response_non_tax_payer, 'tax_payer': response_tax_payer, 'voided_sales': response_voided_sales}
