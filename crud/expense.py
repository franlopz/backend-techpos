from database import *
from core.check_business_uuid import valid_uuid
from models.expense import Gasto

def bulk_gastos(items, current_user, uuid):


    items_to_iterate = items
    new_items = []

    valid_uuid(user=current_user, uuid=uuid)

    for item in items_to_iterate:
        temp_item = item
        temp_item['companyUuid'] = uuid
        new_items.append(temp_item)

    bulkgasto = Gasto.insert_many(new_items).execute()

    return bulkgasto


def delete_gasto(id, current_user, uuid):

    gasto = Gasto.get((Gasto.id == id), (Gasto.companyUuid == uuid))

    return gasto.delete_instance()


def list_gasto(start, finish, current_user, uuid):

    listgastos = list(Gasto.select().where((Gasto.fecha >= start) & (
        Gasto.fecha <= finish) & (Gasto.companyUuid == uuid)))

    return listgastos
