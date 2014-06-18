# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Banner.enabled'
        db.add_column(u'banner_banner', 'enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Banner.enabled'
        db.delete_column(u'banner_banner', 'enabled')


    models = {
        u'banner.banner': {
            'Meta': {'object_name': 'Banner'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description_en': ('django.db.models.fields.TextField', [], {'max_length': '1024'}),
            'description_pl': ('django.db.models.fields.TextField', [], {'max_length': '1024'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'title_pl': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['banner']