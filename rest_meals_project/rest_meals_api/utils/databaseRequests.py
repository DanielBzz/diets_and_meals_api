from django.core.cache import cache
from dishes.models import Dish
from meals.models import Meal
from django.forms import model_to_dict
from django.db.models import Q
from .eReturnValue import eReturnValue

DISHES_LIST = Dish
MEALS_LIST = Meal


def get_list_from_db(model_attribute):
    return list(model_attribute.objects.all())


def add_to_db(model_inst):
    model_inst.save()


def delete_from_db(model_inst):
    model_inst.delete()


def is_object_already_in_db(name, model_attribute):
    if model_attribute.objects.all().filter(name=name).first() is not None:
        raise Exception(eReturnValue.EXIST_ALREADY.value)


def find_item_in_db_by_identify(model_attribute, identify):
    if identify.isdigit():
        attribute_to_look_for = 'id'
        identify = int(identify)
    else:
        attribute_to_look_for = 'name'

    filter_kwargs = {attribute_to_look_for: identify}

    return model_attribute.objects.all().filter(**filter_kwargs).first()


def get_meals_by_values(model_attribute, cal, sodium, sugar):
    return list(model_attribute.objects.filter(cal__lte=cal, sodium__lte=sodium, sugar__lte=sugar))