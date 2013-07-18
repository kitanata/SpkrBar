# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'events_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.EventProfile'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Location'])),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('accept_submissions', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('events', ['Event'])

        # Adding M2M table for field attendees on 'Event'
        m2m_table_name = db.shorten_name(u'events_event_attendees')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['events.event'], null=False)),
            ('spkrbaruser', models.ForeignKey(orm['core.spkrbaruser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'spkrbaruser_id'])

        # Adding M2M table for field endorsements on 'Event'
        m2m_table_name = db.shorten_name(u'events_event_endorsements')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['events.event'], null=False)),
            ('spkrbaruser', models.ForeignKey(orm['core.spkrbaruser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'spkrbaruser_id'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'events_event')

        # Removing M2M table for field attendees on 'Event'
        db.delete_table(db.shorten_name(u'events_event_attendees'))

        # Removing M2M table for field endorsements on 'Event'
        db.delete_table(db.shorten_name(u'events_event_endorsements'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.eventprofile': {
            'Meta': {'object_name': 'EventProfile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '800'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.ProfileTag']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.SpkrbarUser']", 'unique': 'True'})
        },
        'core.profiletag': {
            'Meta': {'object_name': 'ProfileTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'core.spkrbaruser': {
            'Meta': {'object_name': 'SpkrbarUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'followers'", 'symmetrical': 'False', 'to': "orm['core.SpkrbarUser']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'user_type': ('django.db.models.fields.CharField', [], {'default': "'SPEAKER'", 'max_length': '7'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'accept_submissions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attendees': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'events_attending'", 'blank': 'True', 'to': "orm['core.SpkrbarUser']"}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'endorsements': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'events_endorsed'", 'symmetrical': 'False', 'to': "orm['core.SpkrbarUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.EventProfile']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        },
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

    complete_apps = ['events']