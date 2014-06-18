# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'File.name_pl'
        db.alter_column(u'file_manager_file', 'name_pl', self.gf('django.db.models.fields.CharField')(max_length=120))

        # Changing field 'File.name_en'
        db.alter_column(u'file_manager_file', 'name_en', self.gf('django.db.models.fields.CharField')(max_length=120))

    def backwards(self, orm):

        # Changing field 'File.name_pl'
        db.alter_column(u'file_manager_file', 'name_pl', self.gf('django.db.models.fields.CharField')(max_length=40))

        # Changing field 'File.name_en'
        db.alter_column(u'file_manager_file', 'name_en', self.gf('django.db.models.fields.CharField')(max_length=40))

    models = {
        u'file_manager.file': {
            'Meta': {'object_name': 'File'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'file_en': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_pl': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'name_pl': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sync_status': ('django.db.models.fields.CharField', [], {'default': "'waiting'", 'max_length': '16'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['file_manager']