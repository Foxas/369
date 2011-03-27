# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'CommentItem.content_length'
        db.add_column('a369_commentitem', 'content_length', self.gf('django.db.models.fields.IntegerField')(default=0, null=True), keep_default=False)

        # Adding field 'CommentItem.content_word_count'
        db.add_column('a369_commentitem', 'content_word_count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'CommentItem.content_length'
        db.delete_column('a369_commentitem', 'content_length')

        # Deleting field 'CommentItem.content_word_count'
        db.delete_column('a369_commentitem', 'content_word_count')


    models = {
        'a369.articleitem': {
            'Meta': {'object_name': 'ArticleItem'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'crawl_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'crawl_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'crawl_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'item_link': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'source_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'a369.commentitem': {
            'Meta': {'object_name': 'CommentItem'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_length': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'content_word_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'crawl_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'crawl_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'crawl_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'item_link': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'source_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'subject_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['a369']
