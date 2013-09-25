# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TestDistanceModel'
        db.create_table(u'measurement_testdistancemodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('distance', self.gf('measurement.fields.DistanceField')()),
            ('distance_units', self.gf('django.db.models.fields.CharField')(max_length=8, db_index=True)),
        ))
        db.send_create_signal(u'measurement', ['TestDistanceModel'])


    def backwards(self, orm):
        # Deleting model 'TestDistanceModel'
        db.delete_table(u'measurement_testdistancemodel')


    models = {
        u'measurement.testdistancemodel': {
            'Meta': {'object_name': 'TestDistanceModel'},
            'distance': ('measurement.fields.DistanceField', [], {}),
            'distance_units': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['measurement']