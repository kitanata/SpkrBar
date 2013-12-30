# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Talk'
        db.create_table(u'talks_talk', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='talks', to=orm['core.SpkrbarUser'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('abstract', self.gf('django.db.models.fields.CharField')(max_length=4000)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('talks', ['Talk'])

        # Adding M2M table for field tags on 'Talk'
        m2m_table_name = db.shorten_name(u'talks_talk_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('talk', models.ForeignKey(orm['talks.talk'], null=False)),
            ('talktag', models.ForeignKey(orm['talks.talktag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['talk_id', 'talktag_id'])

        # Adding model 'TalkComment'
        db.create_table(u'talks_talkcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('talk', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['talks.Talk'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['talks.TalkComment'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SpkrbarUser'], null=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('talks', ['TalkComment'])

        # Adding model 'TalkEndorsement'
        db.create_table(u'talks_talkendorsement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='endorsements', to=orm['core.SpkrbarUser'])),
            ('talk', self.gf('django.db.models.fields.related.ForeignKey')(related_name='endorsements', to=orm['talks.Talk'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('talks', ['TalkEndorsement'])

        # Adding model 'TalkLink'
        db.create_table(u'talks_talklink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('talk', self.gf('django.db.models.fields.related.ForeignKey')(related_name='links', to=orm['talks.Talk'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('talks', ['TalkLink'])

        # Adding model 'TalkSlideDeck'
        db.create_table(u'talks_talkslidedeck', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('talk', self.gf('django.db.models.fields.related.ForeignKey')(related_name='slides', to=orm['talks.Talk'])),
            ('source', self.gf('django.db.models.fields.CharField')(default='SLIDESHARE', max_length=40)),
            ('embed_data', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('aspect', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('talks', ['TalkSlideDeck'])

        # Adding model 'TalkTag'
        db.create_table(u'talks_talktag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('talks', ['TalkTag'])

        # Adding model 'TalkVideo'
        db.create_table(u'talks_talkvideo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('talk', self.gf('django.db.models.fields.related.ForeignKey')(related_name='videos', to=orm['talks.Talk'])),
            ('source', self.gf('django.db.models.fields.CharField')(default='YOUTUBE', max_length=40)),
            ('embed_data', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('aspect', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('talks', ['TalkVideo'])


    def backwards(self, orm):
        # Deleting model 'Talk'
        db.delete_table(u'talks_talk')

        # Removing M2M table for field tags on 'Talk'
        db.delete_table(db.shorten_name(u'talks_talk_tags'))

        # Deleting model 'TalkComment'
        db.delete_table(u'talks_talkcomment')

        # Deleting model 'TalkEndorsement'
        db.delete_table(u'talks_talkendorsement')

        # Deleting model 'TalkLink'
        db.delete_table(u'talks_talklink')

        # Deleting model 'TalkSlideDeck'
        db.delete_table(u'talks_talkslidedeck')

        # Deleting model 'TalkTag'
        db.delete_table(u'talks_talktag')

        # Deleting model 'TalkVideo'
        db.delete_table(u'talks_talkvideo')


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
        'core.spkrbaruser': {
            'Meta': {'object_name': 'SpkrbarUser'},
            'about_me': ('django.db.models.fields.CharField', [], {'max_length': '4000', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.UserTag']", 'symmetrical': 'False', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'core.usertag': {
            'Meta': {'object_name': 'UserTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'talks.talk': {
            'Meta': {'object_name': 'Talk'},
            'abstract': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'talks'", 'to': "orm['core.SpkrbarUser']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'talks'", 'blank': 'True', 'to': "orm['talks.TalkTag']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'talks.talkcomment': {
            'Meta': {'object_name': 'TalkComment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['talks.TalkComment']"}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['talks.Talk']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SpkrbarUser']", 'null': 'True'})
        },
        'talks.talkendorsement': {
            'Meta': {'object_name': 'TalkEndorsement'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'endorsements'", 'to': "orm['talks.Talk']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'endorsements'", 'to': "orm['core.SpkrbarUser']"})
        },
        'talks.talklink': {
            'Meta': {'object_name': 'TalkLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'to': "orm['talks.Talk']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'talks.talkslidedeck': {
            'Meta': {'object_name': 'TalkSlideDeck'},
            'aspect': ('django.db.models.fields.FloatField', [], {}),
            'embed_data': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "'SLIDESHARE'", 'max_length': '40'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'slides'", 'to': "orm['talks.Talk']"})
        },
        'talks.talktag': {
            'Meta': {'object_name': 'TalkTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'talks.talkvideo': {
            'Meta': {'object_name': 'TalkVideo'},
            'aspect': ('django.db.models.fields.FloatField', [], {}),
            'embed_data': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "'YOUTUBE'", 'max_length': '40'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'videos'", 'to': "orm['talks.Talk']"})
        }
    }

    complete_apps = ['talks']