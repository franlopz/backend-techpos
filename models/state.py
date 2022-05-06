from pydantic import parse_obj_as
from models.cities import Cities
from peewee import *
from .Base import BaseModel
from database import *
from typing import List


class State(BaseModel):
    id = IntegerField()
    name = CharField(max_length=255)

    class Meta:
        db_table = 'states'


def create_states(states):
    if conn.is_closed():
        conn.connect()
    result = State.insert_many(states).execute()
    if not conn.is_closed():
        conn.close()
    return result


def get_states():
    data = {}
    if conn.is_closed():
        conn.connect()
    states_result = list(State.select())

    for state in states_result:
        cities_result = list(Cities.select(Cities.name.alias(
            'name')).where(Cities.stateId == state.id))
        data[state.name] = [
            cities_result[i].name for i in range(len(cities_result))]
    print(data)
    if not conn.is_closed():
        conn.close()
    return data
