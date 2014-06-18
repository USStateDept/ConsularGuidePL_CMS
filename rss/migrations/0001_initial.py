# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RssNews'
        db.create_table(u'rss_rssnews', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('pub_date_rss', self.gf('django.db.models.fields.DateTimeField')(unique=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal(u'rss', ['RssNews'])


    def backwards(self, orm):
        # Deleting model 'RssNews'
        db.delete_table(u'rss_rssnews')


    models = {
        u'rss.rssnews': {
            'Meta': {'object_name': 'RssNews'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '100'}),
            'pub_date_rss': ('django.db.models.fields.DateTimeField', [], {'unique': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['rss']