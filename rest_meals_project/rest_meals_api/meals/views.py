import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Meal
from dishes.models import Dish
import utils.databaseRequests as my_db
import utils.Utils as my_utils
import requests as req
from http import HTTPStatus
from utils.eReturnValue import eReturnValue
import socket

NAME = 'name'
APPETIZER = 'appetizer'
MAIN = 'main'
DESSERT ='dessert'
JSON_ATTRIBUTES = [NAME,APPETIZER,MAIN,DESSERT]
CODE_SWITCHER = {
        eReturnValue.UNSUPPORTED.value : HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        eReturnValue.NOT_SPECIFIED_NAME.value: HTTPStatus.BAD_REQUEST,
        eReturnValue.EXIST_ALREADY.value : HTTPStatus.BAD_REQUEST,
        eReturnValue.NOT_EXIST.value : HTTPStatus.BAD_REQUEST,
    }


@csrf_exempt
def meals_url_method(request):
    if request.method == 'GET':
        return get_meals(request.GET.get('diet',None))
    elif request.method == 'POST':
        return add_meal(request)
    elif request.method == 'DELETE':
        return HttpResponse(eReturnValue.NOT_SPECIFIED_NAME.value, status=HTTPStatus.BAD_REQUEST)

def get_meals(diet_name):
    try:
        if diet_name is None:
            return JsonResponse(my_db.get_list_from_db(my_db.MEALS_LIST), safe=False, encoder=Meal.MealEncoder)
        else:
            diet = get_diet(diet_name)
            return JsonResponse(my_db.get_meals_by_values(my_db.MEALS_LIST, diet['cal'],diet['sodium'], diet['sugar']),
                                safe=False,
                                encoder=Meal.MealEncoder)
    except Exception:
        return HttpResponse(str.format("Diet {0} not found", diet_name), status=HTTPStatus.NOT_FOUND)


def add_meal(request):
    meal_id = 1
    try:
        requested_meal = my_utils.get_object_from_json_request(request, JSON_ATTRIBUTES)
        my_db.is_object_already_in_db(requested_meal[NAME], my_db.MEALS_LIST)
        dishes_in_meal = __get_dishes_in_meal(requested_meal)
        meal = Meal(
            name=requested_meal[NAME],
            appetizer=requested_meal[APPETIZER],
            main=requested_meal[MAIN],
            dessert=requested_meal[DESSERT])
        __calculate_meal(meal,dishes_in_meal)
        my_db.add_to_db(meal)
        meal_id = meal.id
    except json.JSONDecodeError:
        meal_id = eReturnValue.NOT_SPECIFIED_NAME.value
    except Exception as e:
        meal_id = e.args[0]

    return HttpResponse(meal_id, status=CODE_SWITCHER.get(meal_id, HTTPStatus.CREATED))

@csrf_exempt
def meal_url_method(request, id_or_name):
    meal = my_db.find_item_in_db_by_identify(my_db.MEALS_LIST, id_or_name)
    if meal is None:
        return HttpResponse(eReturnValue.NOT_EXIST.value, status=HTTPStatus.NOT_FOUND)
    elif request.method == 'GET':
        return JsonResponse(meal.to_json())
    elif request.method == 'DELETE':
        meal_id = meal.id
        my_db.delete_from_db(meal)
        return HttpResponse(meal_id)
    elif request.method == 'PUT':
        return meal_put(request, meal)

def meal_put(request, meal):
    meal_id = meal.id
    try:
        requested_meal = my_utils.get_object_from_json_request(request, JSON_ATTRIBUTES)
        my_db.is_object_already_in_db(requested_meal[NAME], my_db.MEALS_LIST)
        dishes_in_meal = __get_dishes_in_meal(requested_meal)
        meal.name = requested_meal[NAME]
        meal.appetizer = requested_meal[APPETIZER]
        meal.main = requested_meal[MAIN]
        meal.dessert = requested_meal[DESSERT]
        __calculate_meal(meal, dishes_in_meal)
        my_db.add_to_db(meal)
    except json.JSONDecodeError:
        meal_id = eReturnValue.NOT_SPECIFIED_NAME.value
    except Exception as e:
        meal_id = e.args[0]

    return HttpResponse(meal_id, status=CODE_SWITCHER.get(meal_id, HTTPStatus.CREATED))

def __get_dishes_in_meal(meal):
    dishes_in_meal = []
    for dish_id in [meal[APPETIZER], meal[MAIN], meal[DESSERT]]:
        dish = my_db.find_item_in_db_by_identify(my_db.DISHES_LIST, str(dish_id))
        if dish is not None:
            dishes_in_meal.append(dish)

    if len(dishes_in_meal) != 3:
        raise Exception(eReturnValue.NOT_EXIST.value)

    return dishes_in_meal

def __calculate_meal(meal, dishes_in_meal):
    meal.cal = meal.sugar = meal.sodium = 0
    for dish in dishes_in_meal:
        meal.cal += dish.cal
        meal.sugar += dish.sugar
        meal.sodium += dish.sodium


def get_diet(diet_name):
    api_url = 'http://cloudproject-diets_api-1:5002/diets/{}'.format(diet_name)
    response = req.get(api_url, headers={"Host": "{}".format(socket.gethostname())})
    if response.status_code != req.codes.ok:
        raise Exception()

    return json.loads(response.text)