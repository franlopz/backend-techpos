from peewee import *
from .Base import BaseModel

class Gasto(BaseModel):
    id = IntegerField()
    tipo = CharField(max_length=255)
    descripcion = CharField(max_length=255)
    guardado = DateTimeField()
    monto = FloatField()
    fecha = DateField()
    companyUuid = CharField(max_length=255)

    class Meta:
        db_table = 'gastos'