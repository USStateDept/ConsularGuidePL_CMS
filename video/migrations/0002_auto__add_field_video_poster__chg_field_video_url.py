# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Video.poster'
        db.add_column(u'video_video', 'poster',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Video.url'
        db.alter_column(u'video_video', 'url', self.gf('django.db.models.fields.URLField')(max_length=100, null=True))

    def backwards(self, orm):
        # Deleting field 'Video.poster'
        db.delete_column(u'video_video', 'poster')


        # Changing field 'Video.url'
        db.alter_column(u'video_video', 'url', self.gf('django.db.models.fields.URLField')(default='None', max_length=100))

    models = {
        u'video.video': {
            'Meta': {'object_name': 'Video'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 4, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'poster': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video_type': ('django.db.models.fields.CharField', [], {'default': "'LC'", 'max_length': '2'})
        }
    }

    complete_apps = ['video']