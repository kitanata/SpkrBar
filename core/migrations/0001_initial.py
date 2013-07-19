# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SpkrbarUser'
        db.create_table(u'core_spkrbaruser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user_type', self.gf('django.db.models.fields.CharField')(default='SPEAKER', max_length=10)),
        ))
        db.send_create_signal('core', ['SpkrbarUser'])

        # Adding M2M table for field groups on 'SpkrbarUser'
        m2m_table_name = db.shorten_name(u'core_spkrbaruser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('spkrbaruser', models.ForeignKey(orm['core.spkrbaruser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['spkrbaruser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'SpkrbarUser'
        m2m_table_name = db.shorten_name(u'core_spkrbaruser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('spkrbaruser', models.ForeignKey(orm['core.spkrbaruser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['spkrbaruser_id', 'permission_id'])

        # Adding M2M table for field following on 'SpkrbarUser'
        m2m_table_name = db.shorten_name(u'core_spkrbaruser_following')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_spkrbaruser', models.ForeignKey(orm['core.spkrbaruser'], null=False)),
            ('to_spkrbaruser', models.ForeignKey(orm['core.spkrbaruser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_spkrbaruser_id', 'to_spkrbaruser_id'])

        # Adding model 'SpeakerProfile'
        db.create_table(u'core_speakerprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.SpkrbarUser'], unique=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('about_me', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('core', ['SpeakerProfile'])

        # Adding M2M table for field tags on 'SpeakerProfile'
        m2m_table_name = db.shorten_name(u'core_speakerprofile_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('speakerprofile', models.ForeignKey(orm['core.speakerprofile'], null=False)),
            ('profiletag', models.ForeignKey(orm['core.profiletag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['speakerprofile_id', 'profiletag_id'])

        # Adding model 'EventProfile'
        db.create_table(u'core_eventprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.SpkrbarUser'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=800)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('core', ['EventProfile'])

        # Adding M2M table for field tags on 'EventProfile'
        m2m_table_name = db.shorten_name(u'core_eventprofile_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('eventprofile', models.ForeignKey(orm['core.eventprofile'], null=False)),
            ('profiletag', models.ForeignKey(orm['core.profiletag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['eventprofile_id', 'profiletag_id'])

        # Adding model 'AttendeeProfile'
        db.create_table(u'core_attendeeprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.SpkrbarUser'], unique=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('about_me', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('core', ['AttendeeProfile'])

        # Adding M2M table for field tags on 'AttendeeProfile'
        m2m_table_name = db.shorten_name(u'core_attendeeprofile_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('attendeeprofile', models.ForeignKey(orm['core.attendeeprofile'], null=False)),
            ('profiletag', models.ForeignKey(orm['core.profiletag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['attendeeprofile_id', 'profiletag_id'])

        # Adding model 'Notification'
        db.create_table(u'core_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SpkrbarUser'])),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 18, 0, 0))),
        ))
        db.send_create_signal('core', ['Notification'])

        # Adding model 'SpeakerLink'
        db.create_table(u'core_speakerlink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SpeakerProfile'])),
            ('type_name', self.gf('django.db.models.fields.CharField')(default='TWITTER', max_length=40)),
            ('url_target', self.gf('django.db.models.fields.URLField')(max_length=140)),
        ))
        db.send_create_signal('core', ['SpeakerLink'])

        # Adding model 'ProfileTag'
        db.create_table(u'core_profiletag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('core', ['ProfileTag'])


    def backwards(self, orm):
        # Deleting model 'SpkrbarUser'
        db.delete_table(u'core_spkrbaruser')

        # Removing M2M table for field groups on 'SpkrbarUser'
        db.delete_table(db.shorten_name(u'core_spkrbaruser_groups'))

        # Removing M2M table for field user_permissions on 'SpkrbarUser'
        db.delete_table(db.shorten_name(u'core_spkrbaruser_user_permissions'))

        # Removing M2M table for field following on 'SpkrbarUser'
        db.delete_table(db.shorten_name(u'core_spkrbaruser_following'))

        # Deleting model 'SpeakerProfile'
        db.delete_table(u'core_speakerprofile')

        # Removing M2M table for field tags on 'SpeakerProfile'
        db.delete_table(db.shorten_name(u'core_speakerprofile_tags'))

        # Deleting model 'EventProfile'
        db.delete_table(u'core_eventprofile')

        # Removing M2M table for field tags on 'EventProfile'
        db.delete_table(db.shorten_name(u'core_eventprofile_tags'))

        # Deleting model 'AttendeeProfile'
        db.delete_table(u'core_attendeeprofile')

        # Removing M2M table for field tags on 'AttendeeProfile'
        db.delete_table(db.shorten_name(u'core_attendeeprofile_tags'))

        # Deleting model 'Notification'
        db.delete_table(u'core_notification')

        # Deleting model 'SpeakerLink'
        db.delete_table(u'core_speakerlink')

        # Deleting model 'ProfileTag'
        db.delete_table(u'core_profiletag')


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
        'core.attendeeprofile': {
            'Meta': {'object_name': 'AttendeeProfile'},
            'about_me': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.ProfileTag']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.SpkrbarUser']", 'unique': 'True'})
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
        'core.notification': {
            'Meta': {'object_name': 'Notification'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 18, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SpkrbarUser']"})
        },
        'core.profiletag': {
            'Meta': {'object_name': 'ProfileTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'core.speakerlink': {
            'Meta': {'object_name': 'SpeakerLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SpeakerProfile']"}),
            'type_name': ('django.db.models.fields.CharField', [], {'default': "'TWITTER'", 'max_length': '40'}),
            'url_target': ('django.db.models.fields.URLField', [], {'max_length': '140'})
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
        }
    }

    complete_apps = ['core']
