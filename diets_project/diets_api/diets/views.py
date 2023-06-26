from .models import Diet
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from http import HTTPStatus
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import json


@csrf_exempt
def diets_view(request):
    if request.method == 'GET':
        return get_diets()
    elif request.method == 'POST':
        return add_diet(request)


def diet_view(request, name):
    diet = Diet.objects.all().filter(name=name).first()
    if diet is None:
        return HttpResponse(str.format("Diet {0} not found", name), status=HTTPStatus.NOT_FOUND)

    return JsonResponse(model_to_dict(diet), safe=False)


def add_diet(request):
    try:
        if request.content_type != 'application/json':
            raise Exception()

        diet = Diet.get_object_from_json(request.body)
        diet.save(force_insert=True)
        msg= str.format('Diet {0} created successfully', diet.name)
    except IntegrityError:
        return HttpResponse(str.format('Diet with name {0} already exists',diet.name), status=HTTPStatus.UNPROCESSABLE_ENTITY)
    except (json.JSONDecodeError, KeyError):
        return HttpResponse("Incorrect POST format", status=HTTPStatus.UNPROCESSABLE_ENTITY)
    except Exception as e:
        return HttpResponse("POST expects content type to be application/json", status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    return HttpResponse(msg, status=HTTPStatus.CREATED)


def get_diets():
    return JsonResponse(list(Diet.objects.all().values()), safe=False)
