# encoding: utf8
from django.db import models, migrations
import measurement.fields


class Migration(migrations.Migration):
    
    dependencies = []

    operations = [
        migrations.CreateModel(
            name = 'TestDistanceModel',
            options = {},
            fields = [('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False),), ('distance', measurement.fields.DistanceField(),), ('distance_units', models.CharField(max_length=8, db_index=True),)],
            bases = (models.Model,),
        ),
    ]
