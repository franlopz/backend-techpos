from peewee import *
from .Base import BaseModel

class Proveedor(BaseModel):
    id = IntegerField()
    nrc = CharField(max_length=255)
    nombre = CharField(max_length=255)
    guardado = DateTimeField()
    companyUuid = CharField(max_length=255)

    class Meta:
        db_table = 'proveedores'