from peewee import *

user = 'root'
password = 'Lopez_$2014'
db_name = 'reportes_ventas'

conn = MySQLDatabase(
    db_name, user=user,
    password=password,
    host='localhost'
)

class BaseModel(Model):
    class Meta:
        database = conn
