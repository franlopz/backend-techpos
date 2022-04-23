from core.check_business_uuid import valid_uuid
from table_objects import ProveedoresDB
from peewee import *
from .Base import BaseModel
import json
from database import *

class Proveedor(BaseModel):
    id = IntegerField()
    nrc = CharField(max_length=255)
    nombre = CharField(max_length=255)
    guardado = DateTimeField()
    companyUuid = CharField(max_length=255)

    class Meta:
        db_table = 'proveedores'

async def bulk_proveedores(items,current_user,uuid):
    if conn.is_closed():
        conn.connect()
        
    await valid_uuid(user=current_user,uuid=uuid)

    items_to_iterate = items
    new_items = []
    for item in items_to_iterate:
        temp_item = item
        temp_item['companyUuid'] = uuid
        new_items.append(temp_item)

    bulkproveedor = Proveedor.insert_many(new_items).execute()

    if not conn.is_closed():
        conn.close()
    return bulkproveedor



def list_proveedor(current_user,uuid):
    if conn.is_closed():
     conn.connect()
    listproveedores = list(Proveedor.select().where(Proveedor.companyUuid == uuid))
    if not conn.is_closed():
     conn.close()
    return listproveedores
