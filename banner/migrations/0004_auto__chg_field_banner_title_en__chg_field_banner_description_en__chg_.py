# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Banner.title_en'
        db.alter_column(u'banner_banner', 'title_en', self.gf('django.db.models.fields.CharField')(max_length=40, null=True))

        # Changing field 'Banner.description_en'
        db.alter_column(u'banner_banner', 'description_en', self.gf('django.db.models.fields.TextField')(max_length=60, null=True))

        # Changing field 'Banner.description_pl'
        db.alter_column(u'banner_banner', 'description_pl', self.gf('django.db.models.fields.TextField')(max_length=60, null=True))

        # Changing field 'Banner.title_pl'
        db.alter_column(u'banner_banner', 'title_pl', self.gf('django.db.models.fields.CharField')(max_length=40, null=True))

    def backwards(self, orm):

        # Changing field 'Banner.title_en'
        db.alter_column(u'banner_banner', 'title_en', self.gf('django.db.models.fields.CharField')(max_length=80, null=True))

        # Changing field 'Banner.description_en'
        db.alter_column(u'banner_banner', 'description_en', self.gf('django.db.models.fields.TextField')(max_length=1024, null=True))

        # Changing field 'Banner.description_pl'
        db.alter_column(u'banner_banner', 'description_pl', self.gf('django.db.models.fields.TextField')(max_length=1024, null=True))

        # Changing field 'Banner.title_pl'
        db.alter_column(u'banner_banner', 'title_pl', self.gf('django.db.models.fields.CharField')(max_length=80, null=True))

    models = {
        u'banner.banner': {
            'Meta': {'object_name': 'Banner'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description_en': ('django.db.models.fields.TextField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'description_pl': ('django.db.models.fields.TextField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'title_pl': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['banner']