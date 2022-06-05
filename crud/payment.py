from database import *
from core.check_business_uuid import valid_uuid
from models.payment import Pago

def bulk_pagos(items, current_user, uuid):


    items_to_iterate = items
    new_items = []

    valid_uuid(user=current_user, uuid=uuid)

    for item in items_to_iterate:
        temp_item = item
        temp_item['companyUuid'] = uuid
        new_items.append(temp_item)

    bulkpagos = Pago.insert_many(new_items).execute()

    return bulkpagos


def list_pagos(start, finish, current_user, uuid):

    listPagos = list(Pago.select().where(
        (Pago.fecha >= start) & (Pago.fecha <= finish)))

    return listPagos
