# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IosDevice'
        db.create_table(u'push_notification_iosdevice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device_token', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 12, 0, 0))),
        ))
        db.send_create_signal(u'push_notification', ['IosDevice'])

        # Adding model 'AndroidDevice'
        db.create_table(u'push_notification_androiddevice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('registration_id', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 12, 0, 0))),
        ))
        db.send_create_signal(u'push_notification', ['AndroidDevice'])


    def backwards(self, orm):
        # Deleting model 'IosDevice'
        db.delete_table(u'push_notification_iosdevice')

        # Deleting model 'AndroidDevice'
        db.delete_table(u'push_notification_androiddevice')


    models = {
        u'push_notification.androiddevice': {
            'Meta': {'object_name': 'AndroidDevice'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 12, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_id': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'push_notification.iosdevice': {
            'Meta': {'object_name': 'IosDevice'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 12, 0, 0)'}),
            'device_token': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['push_notification']