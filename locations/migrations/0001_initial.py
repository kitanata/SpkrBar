# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'locations_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('locations', ['Location'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table(u'locations_location')


    models = {
        'locations.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        }
    }

    complete_apps = ['locations']