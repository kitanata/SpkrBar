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
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SpeakerProfile'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('abstract', self.gf('django.db.models.fields.CharField')(max_length=800)),
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

        # Adding M2M table for field endorsements on 'Talk'
        m2m_table_name = db.shorten_name(u'talks_talk_endorsements')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('talk', models.ForeignKey(orm['talks.talk'], null=False)),
            ('spkrbaruser', models.ForeignKey(orm['core.spkrbaruser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['talk_id', 'spkrbaruser_id'])

        # Adding model 'TalkComment'
        db.create_table(u'talks_talkcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('talk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['talks.Talk'])),
            ('commenter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SpkrbarUser'], null=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 18, 0, 0))),
        ))
        db.send_create_signal('talks', ['TalkComment'])

        # Adding model 'TalkRating'
        db.create_table(u'talks_talkrating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('talk', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ratings', to=orm['talks.Talk'])),
            ('rater', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SpkrbarUser'], null=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 18, 0, 0))),
            ('engagement', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('knowledge', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('professionalism', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('resources', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('discussion', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('talks', ['TalkRating'])

        # Adding model 'TalkLink'
        db.create_table(u'talks_talklink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('talk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['talks.Talk'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('talks', ['TalkLink'])

        # Adding model 'TalkPhoto'
        db.create_table(u'talks_talkphoto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('talk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['talks.Talk'])),
            ('width', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('talks', ['TalkPhoto'])

        # Adding model 'TalkSlideDeck'
        db.create_table(u'talks_talkslidedeck', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('talk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['talks.Talk'])),
            ('source', self.gf('django.db.models.fields.CharField')(default='SLIDESHARE', max_length=40)),
            ('data', self.gf('django.db.models.fields.CharField')(max_length=140)),
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
            ('talk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['talks.Talk'])),
            ('source', self.gf('django.db.models.fields.CharField')(default='YOUTUBE', max_length=40)),
            ('data', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('aspect', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('talks', ['TalkVideo'])


    def backwards(self, orm):
        # Deleting model 'Talk'
        db.delete_table(u'talks_talk')

        # Removing M2M table for field tags on 'Talk'
        db.delete_table(db.shorten_name(u'talks_talk_tags'))

        # Removing M2M table for field endorsements on 'Talk'
        db.delete_table(db.shorten_name(u'talks_talk_endorsements'))

        # Deleting model 'TalkComment'
        db.delete_table(u'talks_talkcomment')

        # Deleting model 'TalkRating'
        db.delete_table(u'talks_talkrating')

        # Deleting model 'TalkLink'
        db.delete_table(u'talks_talklink')

        # Deleting model 'TalkPhoto'
        db.delete_table(u'talks_talkphoto')

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
        'core.profiletag': {
            'Meta': {'object_name': 'ProfileTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'core.speakerprofile': {
            'Meta': {'object_name': 'SpeakerProfile'},
            'about_me': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.ProfileTag']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.SpkrbarUser']", 'unique': 'True'})
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
        'talks.talk': {
            'Meta': {'object_name': 'Talk'},
            'abstract': ('django.db.models.fields.CharField', [], {'max_length': '800'}),
            'endorsements': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'talks_endorsed'", 'symmetrical': 'False', 'to': "orm['core.SpkrbarUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SpeakerProfile']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['talks.TalkTag']", 'symmetrical': 'False'})
        },
        'talks.talkcomment': {
            'Meta': {'object_name': 'TalkComment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'commenter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SpkrbarUser']", 'null': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 18, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['talks.Talk']"})
        },
        'talks.talklink': {
            'Meta': {'object_name': 'TalkLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['talks.Talk']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'talks.talkphoto': {
            'Meta': {'object_name': 'TalkPhoto'},
            'height': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['talks.Talk']"}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'talks.talkrating': {
            'Meta': {'object_name': 'TalkRating'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 18, 0, 0)'}),
            'discussion': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'engagement': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'knowledge': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'professionalism': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'rater': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SpkrbarUser']", 'null': 'True'}),
            'resources': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': "orm['talks.Talk']"})
        },
        'talks.talkslidedeck': {
            'Meta': {'object_name': 'TalkSlideDeck'},
            'aspect': ('django.db.models.fields.FloatField', [], {}),
            'data': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "'SLIDESHARE'", 'max_length': '40'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['talks.Talk']"})
        },
        'talks.talktag': {
            'Meta': {'object_name': 'TalkTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'talks.talkvideo': {
            'Meta': {'object_name': 'TalkVideo'},
            'aspect': ('django.db.models.fields.FloatField', [], {}),
            'data': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "'YOUTUBE'", 'max_length': '40'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['talks.Talk']"})
        }
    }

    complete_apps = ['talks']