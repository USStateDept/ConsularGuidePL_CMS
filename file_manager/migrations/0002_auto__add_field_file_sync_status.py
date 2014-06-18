# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'File.sync_status'
        db.add_column(u'file_manager_file', 'sync_status',
                      self.gf('django.db.models.fields.CharField')(default='waiting', max_length=16),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'File.sync_status'
        db.delete_column(u'file_manager_file', 'sync_status')


    models = {
        u'file_manager.file': {
            'Meta': {'object_name': 'File'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 16, 0, 0)'}),
            'file_en': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_pl': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 16, 0, 0)'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_pl': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sync_status': ('django.db.models.fields.CharField', [], {'default': "'waiting'", 'max_length': '16'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['file_manager']