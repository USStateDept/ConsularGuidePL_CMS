# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'File'
        db.create_table(u'file_manager_file', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_pl', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 9, 0, 0))),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 9, 0, 0))),
            ('version', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('size', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('file_en', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('file_pl', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'file_manager', ['File'])


    def backwards(self, orm):
        # Deleting model 'File'
        db.delete_table(u'file_manager_file')


    models = {
        u'file_manager.file': {
            'Meta': {'object_name': 'File'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 9, 0, 0)'}),
            'file_en': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_pl': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 9, 0, 0)'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_pl': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['file_manager']