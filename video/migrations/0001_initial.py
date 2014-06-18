# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Video'
        db.create_table(u'video_video', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video_type', self.gf('django.db.models.fields.CharField')(default='LC', max_length=2)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 27, 0, 0))),
            ('movie', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=100)),
        ))
        db.send_create_signal(u'video', ['Video'])


    def backwards(self, orm):
        # Deleting model 'Video'
        db.delete_table(u'video_video')


    models = {
        u'video.video': {
            'Meta': {'object_name': 'Video'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 27, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '100'}),
            'video_type': ('django.db.models.fields.CharField', [], {'default': "'LC'", 'max_length': '2'})
        }
    }

    complete_apps = ['video']