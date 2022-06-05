from database import *
from models.cities import Cities

def create_cities(cities):

    Cities.insert_many(cities).execute()

    return
