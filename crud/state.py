from database import *
from models.cities import Cities
from models.state import State

def create_states(states):

    result = State.insert_many(states).execute()

    return result

def get_states():
    data = {}

    states_result = list(State.select())

    for state in states_result:
        cities_result = list(Cities.select(Cities.name.alias(
            'name')).where(Cities.stateId == state.id))
        data[state.name] = [
            cities_result[i].name for i in range(len(cities_result))]
    return data