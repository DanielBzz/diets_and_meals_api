from django.db import models
from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder


class Meal(models.Model):
        name = models.CharField(max_length=25)
        appetizer = models.IntegerField()
        main = models.IntegerField()
        dessert = models.IntegerField()
        cal = models.FloatField()
        sodium = models.FloatField()
        sugar = models.FloatField()

        def to_json(self):
                data = model_to_dict(self)
                return_dict = dict()
                return_dict['ID'] = str(data.pop('id'))
                return_dict.update(data)
                return return_dict


        class MealEncoder(DjangoJSONEncoder):
                def default(self, obj):
                        if isinstance(obj, Meal):
                                return obj.to_json()
                        return super().default(obj)