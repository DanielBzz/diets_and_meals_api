import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import utils.databaseRequests as my_db
from utils.eReturnValue import eReturnValue
import utils.ThirdPartRequests
from http import HTTPStatus
import utils.Utils as my_utils
from .models import Dish


JSON_ATTRIBUTES = ['name']
CODE_SWITCHER = {
        eReturnValue.UNSUPPORTED.value : HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        eReturnValue.NOT_SPECIFIED_NAME.value: HTTPStatus.BAD_REQUEST,
        eReturnValue.EXIST_ALREADY.value : HTTPStatus.BAD_REQUEST,
        eReturnValue.API_NOT_RECOGNIZE.value : HTTPStatus.BAD_REQUEST,
        eReturnValue.INTERNAL_SERVER_ERROR.value : HTTPStatus.BAD_REQUEST,
    }

@csrf_exempt
def dishes_url_method(request):
    if request.method == 'GET':
        return get_dishes()
    elif request.method == 'POST':
        return add_dish(request)
    elif request.method == 'DELETE':
        return HttpResponse(eReturnValue.NOT_SPECIFIED_NAME.value, status=HTTPStatus.BAD_REQUEST)

def get_dishes():
    return JsonResponse(my_db.get_list_from_db(my_db.DISHES_LIST), safe=False, encoder=Dish.DishEncoder)

def add_dish(request):
    return_value = 1
    try:
        dish_name = my_utils.get_object_from_json_request(request, JSON_ATTRIBUTES)['name']
        my_db.is_object_already_in_db(dish_name, my_db.DISHES_LIST)
        return_value = utils.ThirdPartRequests.nutrition_api_request(dish_name)
    except json.JSONDecodeError:
        return_value = eReturnValue.NOT_SPECIFIED_NAME.value
    except Exception as e:
        return_value = e.args[0]

    return HttpResponse(return_value, status=CODE_SWITCHER.get(return_value, HTTPStatus.CREATED))

@csrf_exempt
def dish_url_method(request, id_or_name):
    dish = my_db.find_item_in_db_by_identify(my_db.DISHES_LIST, id_or_name)
    if dish is None:
        return HttpResponse(eReturnValue.NOT_EXIST.value, status=HTTPStatus.NOT_FOUND)
    elif request.method == 'GET':
        return JsonResponse(dish.to_json())
    elif request.method == 'DELETE':
        dish_id = dish.id
        my_db.delete_from_db(dish)
        return HttpResponse(dish_id)
