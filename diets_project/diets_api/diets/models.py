# from django.db import models
import json
from djongo import models

# Create your models here.


class Diet(models.Model):
    name = models.CharField(max_length=20,primary_key=True)
    cal = models.FloatField()
    sodium = models.FloatField()
    sugar = models.FloatField()

    @staticmethod
    def get_object_from_json(json_content):
        object_json = json.loads(json_content)
        diet = Diet()
        for attr in Diet._meta.get_fields():
            diet.__setattr__(attr.name, object_json[attr.name])

        return diet
