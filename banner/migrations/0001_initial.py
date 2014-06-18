# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Banner'
        db.create_table(u'banner_banner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('title_pl', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('description_pl', self.gf('django.db.models.fields.TextField')(max_length=1024)),
            ('description_en', self.gf('django.db.models.fields.TextField')(max_length=1024)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal(u'banner', ['Banner'])


    def backwards(self, orm):
        # Deleting model 'Banner'
        db.delete_table(u'banner_banner')


    models = {
        u'banner.banner': {
            'Meta': {'object_name': 'Banner'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description_en': ('django.db.models.fields.TextField', [], {'max_length': '1024'}),
            'description_pl': ('django.db.models.fields.TextField', [], {'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'title_pl': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['banner']