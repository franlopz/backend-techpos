from database import *
from core.check_business_uuid import valid_uuid
from models.supplier import Proveedor

def bulk_proveedores(items, current_user, uuid):


    valid_uuid(user=current_user, uuid=uuid)

    items_to_iterate = items
    new_items = []
    for item in items_to_iterate:
        temp_item = item
        temp_item['companyUuid'] = uuid
        new_items.append(temp_item)

    bulkproveedor = Proveedor.insert_many(new_items).execute()


    return bulkproveedor

def list_proveedor(current_user, uuid):

    listproveedores = list(Proveedor.select().where(
        Proveedor.companyUuid == uuid))

    return listproveedores
