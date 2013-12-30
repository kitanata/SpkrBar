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
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=254)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('about_me', self.gf('django.db.models.fields.CharField')(max_length=4000, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
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

        # Adding M2M table for field tags on 'SpkrbarUser'
        m2m_table_name = db.shorten_name(u'core_spkrbaruser_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('spkrbaruser', models.ForeignKey(orm['core.spkrbaruser'], null=False)),
            ('usertag', models.ForeignKey(orm['core.usertag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['spkrbaruser_id', 'usertag_id'])

        # Adding model 'Notification'
        db.create_table(u'core_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications', to=orm['core.SpkrbarUser'])),
            ('title', self.gf('django.db.models.fields.CharField')(default='Notification', max_length=140)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('dismissed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 29, 0, 0))),
        ))
        db.send_create_signal('core', ['Notification'])

        # Adding model 'UserLink'
        db.create_table(u'core_userlink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='links', to=orm['core.SpkrbarUser'])),
            ('type_name', self.gf('django.db.models.fields.CharField')(default='TWI', max_length=40)),
            ('other_name', self.gf('django.db.models.fields.CharField')(default='Other Website', max_length=100)),
            ('url_target', self.gf('django.db.models.fields.URLField')(max_length=140)),
        ))
        db.send_create_signal('core', ['UserLink'])

        # Adding model 'UserTag'
        db.create_table(u'core_usertag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('core', ['UserTag'])

        # Adding model 'UserFollowing'
        db.create_table(u'core_userfollowing', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='following', to=orm['core.SpkrbarUser'])),
            ('following', self.gf('django.db.models.fields.related.ForeignKey')(related_name='followers', to=orm['core.SpkrbarUser'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('core', ['UserFollowing'])


    def backwards(self, orm):
        # Deleting model 'SpkrbarUser'
        db.delete_table(u'core_spkrbaruser')

        # Removing M2M table for field groups on 'SpkrbarUser'
        db.delete_table(db.shorten_name(u'core_spkrbaruser_groups'))

        # Removing M2M table for field user_permissions on 'SpkrbarUser'
        db.delete_table(db.shorten_name(u'core_spkrbaruser_user_permissions'))

        # Removing M2M table for field tags on 'SpkrbarUser'
        db.delete_table(db.shorten_name(u'core_spkrbaruser_tags'))

        # Deleting model 'Notification'
        db.delete_table(u'core_notification')

        # Deleting model 'UserLink'
        db.delete_table(u'core_userlink')

        # Deleting model 'UserTag'
        db.delete_table(u'core_usertag')

        # Deleting model 'UserFollowing'
        db.delete_table(u'core_userfollowing')


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
        'core.notification': {
            'Meta': {'object_name': 'Notification'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 29, 0, 0)'}),
            'dismissed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Notification'", 'max_length': '140'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': "orm['core.SpkrbarUser']"})
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
        'core.userfollowing': {
            'Meta': {'object_name': 'UserFollowing'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'following': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'followers'", 'to': "orm['core.SpkrbarUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'following'", 'to': "orm['core.SpkrbarUser']"})
        },
        'core.userlink': {
            'Meta': {'object_name': 'UserLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other_name': ('django.db.models.fields.CharField', [], {'default': "'Other Website'", 'max_length': '100'}),
            'type_name': ('django.db.models.fields.CharField', [], {'default': "'TWI'", 'max_length': '40'}),
            'url_target': ('django.db.models.fields.URLField', [], {'max_length': '140'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'to': "orm['core.SpkrbarUser']"})
        },
        'core.usertag': {
            'Meta': {'object_name': 'UserTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        }
    }

    complete_apps = ['core']