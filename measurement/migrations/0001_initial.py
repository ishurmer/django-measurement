# encoding: utf8
from django.db import models, migrations
import measurement.fields


class Migration(migrations.Migration):
    
    dependencies = []

    operations = [
        migrations.CreateModel(
            name = 'TestDistanceModel',
            bases = (models.Model,),
            fields = [('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True),), ('distance', measurement.fields.DistanceField(),), ('distance_units', models.CharField(db_index=True, max_length=8),)],
            options = {},
        ),
    ]
