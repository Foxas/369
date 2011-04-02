# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'BaseWord.count'
        db.delete_column('web369_baseword', 'count')

        # Adding field 'Word.count'
        db.add_column('web369_word', 'count', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'BaseWord.count'
        db.add_column('web369_baseword', 'count', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Deleting field 'Word.count'
        db.delete_column('web369_word', 'count')


    models = {
        'web369.baseword': {
            'Meta': {'object_name': 'BaseWord'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stop_word': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'web369.scrappeddocument': {
            'Meta': {'object_name': 'ScrappedDocument'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_ascii': ('django.db.models.fields.TextField', [], {}),
            'content_length': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'content_word_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'crawl_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'crawl_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'crawl_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'document_type': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_id': ('django.db.models.fields.IntegerField', [], {}),
            'item_link': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'source_id': ('django.db.models.fields.IntegerField', [], {}),
            'subject_id': ('django.db.models.fields.IntegerField', [], {}),
            'subject_title': ('django.db.models.fields.CharField', [], {'max_length': '555', 'null': 'True'}),
            'subject_title_ascii': ('django.db.models.fields.CharField', [], {'max_length': '555', 'null': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'web369.word': {
            'Meta': {'object_name': 'Word'},
            'base': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'derivatives'", 'to': "orm['web369.BaseWord']"}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['web369']
