# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Image.sync_status'
        db.add_column(u'images_image', 'sync_status',
                      self.gf('django.db.models.fields.CharField')(default='waiting', max_length=16),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Image.sync_status'
        db.delete_column(u'images_image', 'sync_status')


    models = {
        u'images.image': {
            'Meta': {'object_name': 'Image'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'sync_status': ('django.db.models.fields.CharField', [], {'default': "'waiting'", 'max_length': '16'})
        }
    }

    complete_apps = ['images']