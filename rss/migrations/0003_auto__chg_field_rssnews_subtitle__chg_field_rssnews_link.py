# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'RssNews.subtitle'
        db.alter_column(u'rss_rssnews', 'subtitle', self.gf('django.db.models.fields.CharField')(max_length=80, null=True))

        # Changing field 'RssNews.link'
        db.alter_column(u'rss_rssnews', 'link', self.gf('django.db.models.fields.URLField')(max_length=512))

    def backwards(self, orm):

        # Changing field 'RssNews.subtitle'
        db.alter_column(u'rss_rssnews', 'subtitle', self.gf('django.db.models.fields.CharField')(default='', max_length=80))

        # Changing field 'RssNews.link'
        db.alter_column(u'rss_rssnews', 'link', self.gf('django.db.models.fields.URLField')(max_length=100))

    models = {
        u'rss.rssnews': {
            'Meta': {'object_name': 'RssNews'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '512'}),
            'pub_date_rss': ('django.db.models.fields.DateTimeField', [], {'unique': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '20000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['rss']