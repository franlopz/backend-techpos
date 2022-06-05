from database import *
from core.check_business_uuid import valid_uuid
from models.product import Producto

def create_producto(fecha: str, hora: str, producto: str, porcion: str, venta: str, tid: int, cantidad: float, precio: float):


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

    return producto_object


def bulk_producto(items, current_user, uuid):


    items_to_iterate = items
    new_items = []

    valid_uuid(user=current_user, uuid=uuid)

    for item in items_to_iterate:
        temp_item = item
        temp_item['companyUuid'] = uuid
        new_items.append(temp_item)

    bulkproducto = Producto.insert_many(new_items).execute()

    return bulkproducto


def list_productos(start, finish, current_user, uuid):

    listproductos = list(Producto.select().where(
        (Producto.fecha >= start) & (Producto.fecha <= finish)))

    return listproductos
