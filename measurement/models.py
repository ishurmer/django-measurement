from django.db import models
from .fields import DistanceField

class TestDistanceModel(models.Model):
    distance = DistanceField(unit_field='distance_units', unit='m')

    distance_units = models.CharField(max_length=8, db_index=True)

    def __unicode__(self):
        return str(self.distance)