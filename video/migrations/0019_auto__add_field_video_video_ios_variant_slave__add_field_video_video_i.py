# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Video.video_ios_variant_slave'
        db.add_column(u'video_video', 'video_ios_variant_slave',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Video.video_ios_generated_on'
        db.add_column(u'video_video', 'video_ios_generated_on',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=120, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Video.video_ios_variant_slave'
        db.delete_column(u'video_video', 'video_ios_variant_slave')

        # Deleting field 'Video.video_ios_generated_on'
        db.delete_column(u'video_video', 'video_ios_generated_on')


    models = {
        u'video.video': {
            'Meta': {'object_name': 'Video'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'conversion': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poster': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'poster_time': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'sync_status': ('django.db.models.fields.CharField', [], {'default': "'waiting'", 'max_length': '16'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'title_pl': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'video_android1': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video_android2': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video_android3': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video_ios1': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video_ios2': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video_ios3': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video_ios_generated_on': ('django.db.models.fields.CharField', [], {'max_length': '120', 'blank': 'True'}),
            'video_ios_variant': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video_ios_variant_slave': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video_original': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video_type': ('django.db.models.fields.CharField', [], {'default': "u'LC'", 'max_length': '2'}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['video']