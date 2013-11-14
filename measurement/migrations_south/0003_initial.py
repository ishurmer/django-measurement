# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TestDistanceModel'
        db.create_table('measurement_testdistancemodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('distance', self.gf('measurement.fields.DistanceField')(default_unit='ft', unit_field='distance_units')),
            ('distance_units', self.gf('django.db.models.fields.CharField')(max_length=8, db_index=True)),
        ))
        db.send_create_signal('measurement', ['TestDistanceModel'])


    def backwards(self, orm):
        # Deleting model 'TestDistanceModel'
        db.delete_table('measurement_testdistancemodel')


    models = {
        'measurement.testdistancemodel': {
            'Meta': {'object_name': 'TestDistanceModel'},
            'distance': ('measurement.fields.DistanceField', [], {'default_unit': "'ft'", 'unit_field': "'distance_units'"}),
            'distance_units': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['measurement']