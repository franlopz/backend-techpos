from core.check_business_uuid import valid_uuid
from peewee import *
from .Base import BaseModel
from database import *
from datetime import date, time, datetime, timedelta


class Ticket(BaseModel):
    id = IntegerField()
    fecha = DateField()
    hora = TimeField()
    total = FloatField()
    tipo = CharField(max_length=255)
    documento = CharField(max_length=255)
    tid = IntegerField()
    puntosLealtad = CharField(max_length=255)
    correlativo = IntegerField()
    descuentoTotal = FloatField()
    propina = FloatField()
    descuentoLealtad = FloatField()
    servicioDomicilio = FloatField()
    cliente = CharField(max_length=255)
    mesa = CharField(max_length=255)
    anulado = CharField(max_length=255)
    mesero = CharField(max_length=255)
    companyUuid = CharField(max_length=255)

    class Meta:
        db_table = 'tickets'


async def bulk_tickets(items, current_user, uuid):
    if conn.is_closed():
        conn.connect()

    items_to_iterate = items
    new_items = []

    await valid_uuid(user=current_user, uuid=uuid)

    for item in items_to_iterate:
        temp_item = item
        temp_item['companyUuid'] = uuid
        new_items.append(temp_item)

    bulktickets = Ticket.insert_many(new_items).execute()
    if not conn.is_closed():
        conn.close()
    return bulktickets


async def list_tickets(start, finish, current_user, uuid):
    if conn.is_closed():
        conn.connect()

    await valid_uuid(user=current_user, uuid=uuid)

    listickets = list(Ticket.select().where(
        (Ticket.fecha >= start) &
        (Ticket.fecha <= finish) &
        (Ticket.companyUuid == uuid)))

    if not conn.is_closed():
        conn.close()
    return listickets


async def summary(start, finish, current_user, uuid):
    if conn.is_closed():
        conn.connect()

    await valid_uuid(user=current_user, uuid=uuid)

    summary_result = list(Ticket
                          .select(
                              Ticket.fecha.alias('date'),
                              Ticket.tipo.alias('type'),
                              Ticket.documento.alias('document'),

                              fn.SUM(Ticket.total).alias('total'))
                          .where(
                              (Ticket.fecha >= start) &
                              (Ticket.fecha <= finish) &
                              (Ticket.companyUuid == uuid))
                          .group_by(Ticket.fecha, Ticket.documento))

    return summary_result
