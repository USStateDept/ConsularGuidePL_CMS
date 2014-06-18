# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AndroidDevice'
        db.delete_table(u'push_notification_androiddevice')

        # Deleting model 'IosDevice'
        db.delete_table(u'push_notification_iosdevice')


    def backwards(self, orm):
        # Adding model 'AndroidDevice'
        db.create_table(u'push_notification_androiddevice', (
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 12, 0, 0))),
            ('registration_id', self.gf('django.db.models.fields.CharField')(max_length=200)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'push_notification', ['AndroidDevice'])

        # Adding model 'IosDevice'
        db.create_table(u'push_notification_iosdevice', (
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 12, 0, 0))),
            ('device_token', self.gf('django.db.models.fields.CharField')(max_length=80)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'push_notification', ['IosDevice'])


    models = {
        
    }

    complete_apps = ['push_notification']