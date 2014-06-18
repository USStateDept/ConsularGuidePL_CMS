# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feedback'
        db.create_table(u'feedback_feedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['page.Page'], null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 9, 0, 0))),
        ))
        db.send_create_signal(u'feedback', ['Feedback'])


    def backwards(self, orm):
        # Deleting model 'Feedback'
        db.delete_table(u'feedback_feedback')


    models = {
        u'feedback.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 9, 0, 0)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'from_page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['page.Page']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'page.page': {
            'Meta': {'object_name': 'Page'},
            'additional_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'additional_pl': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_en': ('django.db.models.fields.TextField', [], {}),
            'content_pl': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 9, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 9, 0, 0)'}),
            'page_type': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '4'}),
            'parent_page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_page'", 'null': 'True', 'to': u"orm['page.Page']"}),
            'place': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'title_pl': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'zoom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['feedback']