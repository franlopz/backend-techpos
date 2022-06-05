from peewee import *
from .Base import BaseModel

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