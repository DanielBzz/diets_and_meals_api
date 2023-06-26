import itertools
import json
import requests as req
from dishes.models import Dish
from .eReturnValue import eReturnValue
import utils.databaseRequests as my_db

NAME='name'
CAL='calories'
SIZE_G='serving_size_g'
SUGAR='sugar_g'
SODIUM='sodium_mg'


def nutrition_api_request(query):
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
    response = req.get(api_url, headers={'X-Api-Key': 'jPdP8Gnobhq42ipFN9cXbw==UjeD0ycLpUmZNceL'})
    if response.status_code == req.codes.ok:
        return create_dish(query,response.text)
    else:
        print("Error:", response.status_code, response.text)
        return eReturnValue.INTERNAL_SERVER_ERROR.value


def create_dish(query, json_response):
    try:
        dish_receips = json.loads(json_response)
    except:
        raise Exception(eReturnValue.INTERNAL_SERVER_ERROR.value)

    if type(dish_receips) != list or len(dish_receips) == 0:
        raise Exception(eReturnValue.API_NOT_RECOGNIZE.value)

    dish = Dish(name=query,size=0,cal=0,sugar=0,sodium=0)
    for temp_dish in itertools.islice(dish_receips,2):
        dish.size += temp_dish[SIZE_G]
        dish.cal += temp_dish[CAL]
        dish.sugar += temp_dish[SUGAR]
        dish.sodium += temp_dish[SODIUM]

    my_db.add_to_db(dish)

    return dish.id
