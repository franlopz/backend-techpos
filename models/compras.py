from core.check_business_uuid import valid_uuid
from peewee import *
from .Base import BaseModel
from database import *
from .gasto import Gasto
from .ticket import Ticket


class Compra(BaseModel):
    id = IntegerField()
    fecha = DateField()
    documento = CharField(max_length=255)
    tipo = CharField(max_length=255)
    referencia = CharField(max_length=255)
    nrc = CharField(max_length=255)
    nombre = CharField(max_length=255)
    compra = FloatField()
    iva = FloatField()
    guardado = DateTimeField()
    documentoId = IntegerField()
    tipoId = IntegerField()
    dui = CharField(max_length=255)
    comInGra = FloatField()
    comInEx = FloatField()
    intExNoSuj = FloatField()
    imExNoSuj = FloatField()
    inGraBie = FloatField()
    imGravBie = FloatField()
    imGravSer = FloatField()
    attachmentId = IntegerField()
    companyUuid = CharField(max_length=255)

    class Meta:
        db_table = 'compras'


async def bulk_compra(items, current_user, uuid):
    if conn.is_closed():
        conn.connect()

    items_to_iterate = items
    new_items = []

    await valid_uuid(user=current_user, uuid=uuid)

    for item in items_to_iterate:
        temp_item = item
        temp_item['companyUuid'] = uuid
        new_items.append(temp_item)

    bulkcompra = Compra.insert_many(new_items).execute()
    if not conn.is_closed():
        conn.close()
    return bulkcompra


async def list_compras(start, finish, current_user, uuid):

    if conn.is_closed():
        conn.connect()

    await valid_uuid(user=current_user, uuid=uuid)

    listcompras = list(Compra
                       .select()
                       .where(
                           (Compra.fecha >= start) & (Compra.fecha <= finish) & (Compra.companyUuid == uuid))
                       .order_by(Compra.fecha.desc())
                       )
    if not conn.is_closed():
        conn.close()
    return listcompras


async def delete_compra(id, current_user, uuid):
    if conn.is_closed():
        conn.connect()

    compra = Compra.get(Compra.id == id, Compra.companyUuid == uuid)
    if not conn.is_closed():
        conn.close()
    return compra.delete_instance()


async def get_CompraReport(start, finish, current_user, uuid):
    dic = dict

    dic = {'gastos': {"Servicio": 0,
                      "Alquiler": 0,
                      "Salario": 0,
                      "Propina": 0,
                      "ISSS": 0,
                      "Publicidad": 0,
                      "Mantenimiento": 0,
                      "Comisión": 0,
                      "Otro": 0},
           'compras': {"compraTotal": 0,
                       "compraDeducible": 0},
           'tickets': {"total": 0,
                       "propina": 0},
           'iva': {"total": 0,
                   "deducible": 0}}

    if conn.is_closed():
        conn.connect()

    await valid_uuid(user=current_user, uuid=uuid)

    reporteCompras = list(Compra.select(fn.SUM(Compra.compra).alias('compraTotal')).where(
        (Compra.fecha >= start) & (Compra.fecha <= finish) & (Compra.companyUuid == uuid)).dicts())
    reporteComprasIVA = list(Compra.select(fn.SUM(Compra.compra).alias('compraDeducible')).where(
        (Compra.fecha >= start) & (Compra.fecha <= finish) & (Compra.documento != 'Consumidor Final') & (Compra.companyUuid == uuid)).dicts())
    reporteGastos = list(Gasto.select(Gasto.tipo, fn.SUM(Gasto.monto).alias('monto')).where(
        (Gasto.fecha >= start) & (Gasto.fecha <= finish) & (Gasto.companyUuid == uuid)).group_by(Gasto.tipo).dicts())
    reporteTickets = list(Ticket.select(fn.SUM(Ticket.total).alias('total'), fn.SUM(
        Ticket.propina).alias('propina')).where((Ticket.fecha >= start) & (Ticket.fecha <= finish) & (Ticket.companyUuid == uuid)).dicts())
    for rg in reporteGastos:
        dic['gastos'].update({rg['tipo']: rg['monto']})
        # dic['gastos'].append(rg)

    for rt in reporteTickets:
        for k, v in rt.items():
            if rt[k] is not None:
                dic['tickets'].update(rt)
                dic['iva'].update(
                    {"total": (rt['total']-rt['propina'] -
                               ((rt['total']-rt['propina'])/1.13))}
                )

    for rc in reporteCompras:
        if rc['compraTotal'] is not None:
            dic['compras'].update(rc)

    for rci in reporteComprasIVA:
        if rci['compraDeducible'] is not None:
            dic['compras'].update(rci)
            dic['iva'].update(
                {"deducible": (rci['compraDeducible'] -
                               (rci['compraDeducible']/1.13))}
            )

    if not conn.is_closed():
        conn.close()
    return dic
