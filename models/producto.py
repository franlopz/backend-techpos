from core.check_business_uuid import valid_uuid
from table_objects import ProductoDB
from peewee import *
from .Base import BaseModel
import json
from database import *


class Producto(BaseModel):
    fecha = DateField()
    hora = TimeField()
    producto = CharField(max_length=255)
    porcion = CharField(max_length=255)
    venta = CharField(max_length=255)
    tid = IntegerField()
    cantidad = FloatField()
    precio = FloatField()
    id = IntegerField()
    companyUuid = CharField(max_length=255)

    class Meta:
        db_table = 'productos'


def create_producto(fecha: str, hora: str, producto: str, porcion: str, venta: str, tid: int, cantidad: float, precio: float):
    if conn.is_closed():
        conn.connect()

    producto_object = Producto(
        fecha=fecha,
        hora=hora,
        precio=precio,
        producto=producto,
        porcion=porcion,
        venta=venta,
        tid=tid,
        cantidad=cantidad,
    )
    producto_object.save()
    if not conn.is_closed():
        conn.close()
    return producto_object


def bulk_producto(items, current_user, uuid):
    if conn.is_closed():
        conn.connect()

    items_to_iterate = items
    new_items = []

    valid_uuid(user=current_user, uuid=uuid)

    for item in items_to_iterate:
        temp_item = item
        temp_item['companyUuid'] = uuid
        new_items.append(temp_item)

    bulkproducto = Producto.insert_many(new_items).execute()
    if not conn.is_closed():
        conn.close()
    return bulkproducto


def list_productos(start, finish, current_user, uuid):
    if conn.is_closed():
        conn.connect()
    listproductos = list(Producto.select().where(
        (Producto.fecha >= start) & (Producto.fecha <= finish)))
    if not conn.is_closed():
        conn.close()
    return listproductos
