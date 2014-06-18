# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Page.longitude'
        db.delete_column(u'page_page', 'longitude')

        # Deleting field 'Page.zoom'
        db.delete_column(u'page_page', 'zoom')

        # Deleting field 'Page.latitude'
        db.delete_column(u'page_page', 'latitude')


    def backwards(self, orm):
        # Adding field 'Page.longitude'
        db.add_column(u'page_page', 'longitude',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.zoom'
        db.add_column(u'page_page', 'zoom',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.latitude'
        db.add_column(u'page_page', 'latitude',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)


    models = {
        u'page.page': {
            'Meta': {'object_name': 'Page'},
            'additional_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'additional_pl': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_en': ('django.db.models.fields.TextField', [], {}),
            'content_pl': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 8, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 8, 0, 0)'}),
            'page_type': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '4'}),
            'parent_page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_page'", 'null': 'True', 'to': u"orm['page.Page']"}),
            'place': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'title_pl': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['page']