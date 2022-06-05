from peewee import *
from .Base import BaseModel

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