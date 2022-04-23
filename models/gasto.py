from core.check_business_uuid import valid_uuid
from table_objects import GastosDB
from peewee import *
from .Base import BaseModel
import json
from database import *


class Gasto(BaseModel):
    id = IntegerField()
    tipo = CharField(max_length=255)
    descripcion = CharField(max_length=255)
    guardado = DateTimeField()
    monto = FloatField()
    fecha = DateField()
    companyUuid = CharField(max_length=255)

    class Meta:
        db_table = 'gastos'


async def bulk_gastos(items, current_user, uuid):
    if conn.is_closed():
        conn.connect()

    items_to_iterate = items
    new_items = []

    await valid_uuid(user=current_user, uuid=uuid)

    for item in items_to_iterate:
        temp_item = item
        temp_item['companyUuid'] = uuid
        new_items.append(temp_item)

    bulkgasto = Gasto.insert_many(new_items).execute()
    if not conn.is_closed():
        conn.close()
    return bulkgasto


async def delete_gasto(id, current_user, uuid):
    if conn.is_closed():
        conn.connect()
    gasto = Gasto.get((Gasto.id == id), (Gasto.companyUuid == uuid))
    if not conn.is_closed():
        conn.close()
    return gasto.delete_instance()


def list_gasto(start, finish, current_user, uuid):
    if conn.is_closed():
        conn.connect()
    listgastos = list(Gasto.select().where((Gasto.fecha >= start) & (
        Gasto.fecha <= finish) & (Gasto.companyUuid == uuid)))
    if not conn.is_closed():
        conn.close()
    return listgastos
