# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Page'
        db.create_table(u'page_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_page', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='child_page', null=True, to=orm['page.Page'])),
            ('page_type', self.gf('django.db.models.fields.CharField')(default='text', max_length=4)),
            ('title_pl', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('version', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 8, 0, 0))),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 8, 0, 0))),
            ('level', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('place', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('content_pl', self.gf('django.db.models.fields.TextField')()),
            ('content_en', self.gf('django.db.models.fields.TextField')()),
            ('additional_pl', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('additional_en', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('zoom', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'page', ['Page'])


    def backwards(self, orm):
        # Deleting model 'Page'
        db.delete_table(u'page_page')


    models = {
        u'page.page': {
            'Meta': {'object_name': 'Page'},
            'additional_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'additional_pl': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_en': ('django.db.models.fields.TextField', [], {}),
            'content_pl': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 8, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 8, 0, 0)'}),
            'page_type': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '4'}),
            'parent_page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_page'", 'null': 'True', 'to': u"orm['page.Page']"}),
            'place': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'title_pl': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'zoom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['page']