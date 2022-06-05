from peewee import *
from .Base import BaseModel

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