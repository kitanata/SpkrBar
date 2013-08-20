# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'TalkComment.comment'
        db.delete_column(u'talks_talkcomment', 'comment')

        # Deleting field 'TalkComment.commenter'
        db.delete_column(u'talks_talkcomment', 'commenter_id')

        # Deleting field 'TalkComment.datetime'
        db.delete_column(u'talks_talkcomment', 'datetime')


        # Changing field 'TalkComment.new_comment'
        db.alter_column(u'talks_talkcomment', 'new_comment_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Comment']))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'TalkComment.comment'
        raise RuntimeError("Cannot reverse this migration. 'TalkComment.comment' and its values cannot be restored.")
        # Adding field 'TalkComment.commenter'
        db.add_column(u'talks_talkcomment', 'commenter',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SpkrbarUser'], null=True),
                      keep_default=False)

        # Adding field 'TalkComment.datetime'
        db.add_column(u'talks_talkcomment', 'datetime',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 19, 0, 0)),
                      keep_default=False)


        # Changing field 'TalkComment.new_comment'
        db.alter_column(u'talks_talkcomment', 'new_comment_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Comment'], null=True))

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
        'core.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 19, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['core.Comment']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SpkrbarUser']"})
        },
        'core.profiletag': {
            'Meta': {'object_name': 'ProfileTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'core.speakerprofile': {
            'Meta': {'object_name': 'SpeakerProfile'},
            'about_me': ('django.db.models.fields.CharField', [], {'max_length': '4000', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.ProfileTag']", 'symmetrical': 'False', 'blank': 'True'}),
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
            'user_type': ('django.db.models.fields.CharField', [], {'default': "'SPEAKER'", 'max_length': '10'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'talks.talk': {
            'Meta': {'object_name': 'Talk'},
            'abstract': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'endorsements': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'talks_endorsed'", 'symmetrical': 'False', 'to': "orm['core.SpkrbarUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SpeakerProfile']"})
        },
        'talks.talkcomment': {
            'Meta': {'object_name': 'TalkComment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_comment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Comment']"}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['talks.Talk']"})
        },
        'talks.talklink': {
            'Meta': {'object_name': 'TalkLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'to': "orm['talks.Talk']"}),
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
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 19, 0, 0)'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags'", 'to': "orm['talks.Talk']"})
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