from contextvars import ContextVar
import peewee
import os
from dotenv import load_dotenv
load_dotenv('.env')
import core.sql_queries as queries
import pymysql


class Envs:
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    

con = pymysql.connect(host='localhost',
                       user=Envs.DB_USER,
                       password=Envs.DB_PASSWORD)
con.cursor().execute('CREATE DATABASE IF NOT EXISTS ' + Envs.DB_NAME)
con.select_db(Envs.DB_NAME)
con.cursor().execute(queries.cities_table_create)
con.cursor().execute(queries.client_credentials_create)
con.cursor().execute(queries.companies_create)
con.cursor().execute(queries.company_account_create)
con.cursor().execute(queries.expenses_create)
con.cursor().execute(queries.products_create)
con.cursor().execute(queries.payments_create)
con.cursor().execute(queries.purchases_create)
con.cursor().execute(queries.roles_create)
con.cursor().execute(queries.users_create)
con.cursor().execute(queries.state_create)
con.cursor().execute(queries.status_create)
con.cursor().execute(queries.tickets_create)
con.cursor().execute(queries.suppliers_create)
con.close()

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())

class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]
    
conn = peewee.MySQLDatabase(
    Envs.DB_NAME, user=Envs.DB_USER,
    password=Envs.DB_PASSWORD,
    host='localhost',
)

conn._state = PeeweeConnectionState()

class BaseModel(peewee.Model):
    class Meta:
        database = conn
