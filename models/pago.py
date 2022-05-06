from core.check_business_uuid import valid_uuid
from peewee import *
from .Base import BaseModel
from database import *


class Pago(BaseModel):
    fecha = DateField()
    hora = TimeField()
    tipoPago = CharField(max_length=255)
    pago = FloatField()
    caja = CharField(max_length=255)
    tid = IntegerField()
    iva = FloatField()
    id = IntegerField()
    usuario = CharField(max_length=255)
    correlativo = IntegerField()
    anulado = CharField(max_length=255)
    companyUuid = CharField(max_length=255)

    class Meta:
        db_table = 'pagos'


def bulk_pagos(items, current_user, uuid):
    if conn.is_closed():
        conn.connect()

    items_to_iterate = items
    new_items = []

    valid_uuid(user=current_user, uuid=uuid)

    for item in items_to_iterate:
        temp_item = item
        temp_item['companyUuid'] = uuid
        new_items.append(temp_item)

    bulkpagos = Pago.insert_many(new_items).execute()
    if not conn.is_closed():
        conn.close()
    return bulkpagos


def list_pagos(start, finish, current_user, uuid):
    if conn.is_closed():
        conn.connect()
    listPagos = list(Pago.select().where(
        (Pago.fecha >= start) & (Pago.fecha <= finish)))
    if not conn.is_closed():
        conn.close()
    return listPagos
