# encoding: utf8
from django.db import models, migrations
import measurement.fields


class Migration(migrations.Migration):
    
    dependencies = []

    operations = [
        migrations.CreateModel(
            fields = [('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),), ('distance', measurement.fields.DistanceField(),), ('distance_units', models.CharField(max_length=8, db_index=True),)],
            bases = (models.Model,),
            options = {},
            name = 'TestDistanceModel',
        ),
    ]
